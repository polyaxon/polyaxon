import argparse

from fastai.vision.all import *
from fastai.basics import *

from polyaxon.tracking.contrib.fastai import PolyaxonCallback

path = untar_data(URLs.MNIST_SAMPLE)
items = get_image_files(path)
tds = Datasets(items, [PILImageBW.create, [parent_label, Categorize()]], splits=GrandparentSplitter()(items))
dls = tds.dataloaders(bs=32, after_item=[ToTensor(), IntToFloatTensor()])

# create a learner with gradient accumulation
learn = cnn_learner(
    dls,
    resnet18,
    loss_func=CrossEntropyLossFlat(),
    cbs=[PolyaxonCallback()]
)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fit', type=int, default=2)
    args = parser.parse_args()
    learn.fit(args.fit)
