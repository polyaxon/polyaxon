from __future__ import print_function

import os
from argparse import ArgumentParser
import random
import logging
from importlib import util

import numpy as np

from sklearn.metrics import classification_report

import torch
from torch.utils.data import DataLoader, Dataset
from torchvision.transforms import Compose, ToTensor, Normalize
from torchvision.datasets import CIFAR10

try:
    from tensorboardX import SummaryWriter
except ImportError:
    raise RuntimeError("No tensorboardX package is found. Please install with the command: \npip install tensorboardX")

from ignite.engine import Events, Engine
from ignite.handlers import Timer
from ignite._utils import convert_tensor


SEED = 12345
random.seed(SEED)
torch.manual_seed(SEED)


def get_test_data_loader(path, imgaugs, batch_size, num_workers, device='cpu'):

    # Load imgaugs module:
    this_dir = os.path.dirname(__file__)
    spec = util.spec_from_file_location("imgaugs", os.path.join(this_dir, imgaugs))
    custom_module = util.module_from_spec(spec)
    spec.loader.exec_module(custom_module)

    test_data_transform = getattr(custom_module, "test_data_transform")
    test_data_transform = Compose(test_data_transform)

    class IndexedDataset(Dataset):

        def __init__(self, ds):
            super(IndexedDataset, self).__init__()
            self.ds = ds

        def __getitem__(self, index):
            return self.ds[index], index

        def __len__(self):
            return len(self.ds)

    pin_memory = 'cuda' in device
    test_dataset = IndexedDataset(CIFAR10(path, train=False, transform=test_data_transform, download=True))
    test_loader = DataLoader(test_dataset, batch_size=batch_size,
                             shuffle=False, drop_last=False,
                             num_workers=num_workers, pin_memory=pin_memory)
    return test_loader


def setup_logger(logger, output, level=logging.INFO):
    logger.setLevel(level)
    # create file handler which logs even debug messages
    fh = logging.FileHandler(os.path.join(output, "eval.log"))
    fh.setLevel(level)
    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(level)
    # create formatter and add it to the handlers
    formatter = logging.Formatter("%(asctime)s|%(name)s|%(levelname)s| %(message)s")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)


def write_model_graph(writer, model, data_loader, device):
    data_loader_iter = iter(data_loader)
    (x, y), indices = next(data_loader_iter)
    x = convert_tensor(x, device=device)
    try:
        writer.add_graph(model, x)
    except Exception as e:
        print("Failed to save model graph: {}".format(e))


def create_inferencer(model, device='cpu'):

    def _prepare_batch(batch):
        (x, y), indices = batch
        x = convert_tensor(x, device=device)
        return x, y, indices

    def _update(engine, batch):
        x, y, indices = _prepare_batch(batch)
        y_pred = model(x)
        return {
            "x": convert_tensor(x, device='cpu'),
            "y_pred": convert_tensor(y_pred, device='cpu'),
            "y_true": y,
            "indices": indices
        }

    inferencer = Engine(_update)
    return inferencer


def save_conf(logger, writer, model_name, imgaugs,
        test_batch_size, num_workers,
        n_tta, output):
    conf_str = """        
        Training configuration:
            Model: {model}
            Image augs: {imgaugs}
            Test batch size: {test_batch_size}
            Number of workers: {num_workers}
            Number of TTA: {n_tta}
            Output folder: {output}        
    """.format(
        model=model_name,
        imgaugs=imgaugs,
        test_batch_size=test_batch_size,
        num_workers=num_workers,
        n_tta=n_tta,
        output=output
    )
    logger.info(conf_str)
    writer.add_text('Configuration', conf_str)


def run(checkpoint, dataset_path, imgaugs, batch_size, num_workers, n_tta, output, debug):

    print("--- Cifar10 Playground : Inference --- ")

    from datetime import datetime
    now = datetime.now()
    log_dir = os.path.join(output, "inference_%s" % (now.strftime("%Y%m%d_%H%M")))
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_level = logging.INFO
    if debug:
        log_level = logging.DEBUG
        print("Activated debug mode")

    logger = logging.getLogger("Cifar10 Playground: Inference")
    setup_logger(logger, log_dir, log_level)

    logger.debug("Setup tensorboard writer")
    writer = SummaryWriter(log_dir=os.path.join(log_dir, "tensorboard"))

    save_conf(logger, writer, checkpoint, imgaugs,
        batch_size, num_workers,
        n_tta, log_dir)

    device = 'cpu'
    if torch.cuda.is_available():
        logger.debug("CUDA is enabled")
        from torch.backends import cudnn
        cudnn.benchmark = True
        device = 'cuda'

    logger.debug("Setup model: {}".format(checkpoint))
    model = torch.load(checkpoint)
    if 'cuda' in device:
        model = model.cuda()

    logger.debug("Setup test dataloader")
    test_loader = get_test_data_loader(dataset_path, imgaugs, batch_size, num_workers, device=device)

    write_model_graph(writer, model, test_loader, device=device)

    logger.debug("Setup ignite trainer and evaluator")
    inferencer = create_inferencer(model, device=device)

    logger.debug("Setup handlers")
    # Setup timer to measure evaluation time
    timer = Timer(average=True)
    timer.attach(inferencer,
                 start=Events.STARTED,
                 resume=Events.ITERATION_STARTED,
                 pause=Events.ITERATION_COMPLETED)

    n_samples = len(test_loader.dataset)
    indices = np.zeros((n_samples, n_tta), dtype=np.int32)
    y_probas_tta = np.zeros((n_samples, 10, n_tta))
    y_true = np.zeros((n_samples, ), dtype=np.int32)

    @inferencer.on(Events.EPOCH_COMPLETED)
    def log_tta(engine):
        logger.debug("TTA {} / {}".format(engine.state.epoch, n_tta))

    @inferencer.on(Events.ITERATION_COMPLETED)
    def save_results(engine):
        output = engine.state.output
        tta_index = engine.state.epoch - 1
        start_index = ((engine.state.iteration - 1) % len(test_loader)) * batch_size
        batch_indices = output['indices'].numpy()
        batch_y_probas = output['y_pred'].detach().numpy()
        batch_y_true = output['y_true'].numpy()
        end_index = min(start_index + batch_size, len(indices))
        indices[start_index:end_index, tta_index] = batch_indices
        y_probas_tta[start_index:end_index, :, tta_index] = batch_y_probas
        if tta_index == 0:
            y_true[start_index:end_index] = batch_y_true

    logger.debug("Start inference")
    try:
        inferencer.run(test_loader, max_epochs=n_tta)
    except KeyboardInterrupt:
        logger.info("Catched KeyboardInterrupt -> exit")
    except Exception as e:  # noqa
        logger.exception("")
        if debug:
            try:
                # open an ipython shell if possible
                import IPython
                IPython.embed()  # noqa
            except ImportError:
                print("Failed to start IPython console")
        exit(1)

    writer.close()

    # Check indices:
    for i in range(n_tta - 1):
        ind1 = indices[:, i]
        ind2 = indices[:, i + 1]
        assert (ind1 == ind2).all()

    # Average probabilities:
    y_probas = np.mean(y_probas_tta, axis=-1)
    y_preds = np.argmax(y_probas, axis=-1)

    logger.info("\n" + classification_report(y_true, y_preds))


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument("checkpoint", type=str, help="Model checkpoint to load")
    parser.add_argument("--path", type=str, default=".",
                        help="Optional path to Cifar10 dataset")
    parser.add_argument('--n_tta', type=int, default=5,
                        help='Number of test time augmentations (default: 5)')
    parser.add_argument('--imgaugs', type=str, default="imgaugs/basic.py",
                        help='image augmentations module (default: imgaugs.py)')
    parser.add_argument('--batch_size', type=int, default=64,
                        help='input batch size for testing (default: 64)')
    parser.add_argument('--num_workers', type=int, default=8,
                        help='Number of workers in data loader(default: 8)')
    parser.add_argument("--output", type=str, default="output",
                        help="directory to store best models")
    parser.add_argument("--debug", action="store_true", default=0,
                        help="Enable debugging")
    args = parser.parse_args()

    run(args.checkpoint, args.path,
        args.imgaugs,
        args.batch_size, args.num_workers,
        args.n_tta,
        args.output, args.debug)
