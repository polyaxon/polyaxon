import argparse

from fastai.vision.all import *

from polyaxon.tracking.contrib.fastai import PolyaxonCallback

path = untar_data(URLs.CAMVID_TINY)
codes = np.loadtxt(path / 'codes.txt', dtype=str)
fnames = get_image_files(path / "images")


def label_func(fn):
    return path / "labels" / f"{fn.stem}_P{fn.suffix}"


dls = SegmentationDataLoaders.from_label_func(
    path, bs=8, fnames=fnames, label_func=label_func, codes=codes
)

learn = unet_learner(dls, resnet18, cbs=[PolyaxonCallback(log_model=True), SaveModelCallback()])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fit', type=int, default=2)
    args = parser.parse_args()
    learn.fit(args.fit)
