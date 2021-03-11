import argparse

from fastai.tabular.all import *

from polyaxon.tracking.contrib.fastai import PolyaxonCallback

path = untar_data(URLs.ADULT_SAMPLE)
df = pd.read_csv(path / 'adult.csv')
dls = TabularDataLoaders.from_csv(
    path / 'adult.csv',
    path=path,
    y_names="salary",
    cat_names=['workclass', 'education', 'marital-status', 'occupation', 'relationship', 'race'],
    cont_names=['age', 'fnlwgt', 'education-num'],
    procs=[Categorify, FillMissing, Normalize]
)

# create a learner and train
learn = tabular_learner(dls, metrics=accuracy, cbs=[PolyaxonCallback()])

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--fit', type=int, default=2)
    args = parser.parse_args()
    learn.fit(args.fit)
