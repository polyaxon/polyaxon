# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import inspect
import os.path
import re
import shutil

import polyaxon
from polyaxon import (
    activations,
    initializations,
    metrics,
    losses,
    regularizations,
    optimizers,
    variables)
from polyaxon.datasets import cifar10, flowers17, mnist
from polyaxon.datasets.converters import (
    ImageReader,
    PNGImageReader,
    PNGNumpyImageReader,
    JPGNumpyImageReader,
    JPEGImageReader,
    ImagesToTFExampleConverter
)
from polyaxon.experiments import estimator, experiment, hooks, subgraph, summarizer
from polyaxon import models
from polyaxon.layers import convolutional, core, embedding, normalizations, recurrent
from polyaxon.libs import configs, getters, utils
from polyaxon.processing import (
    CategoricalVocabulary,
    CategoricalProcessor,
    create_input_data_fn,
    image,
    pipelines,
    VocabularyProcessor,
)
from polyaxon.processing.data_decoders import (
    DataDecoder,
    TFExampleDecoder,
    SplitTokensDecoder,
    TFSequenceExampleDecoder
)
from polyaxon.processing.data_providers import (
    Dataset,
    DataProvider,
    DatasetDataProvider,
    ParallelDatasetProvider
)

ROOT = 'http://polyaxon.com/docs/'

PAGES = [
    {
        'page': 'experiments/experiment.md',
        'classes': [experiment.Experiment],
        'classes_functions': [
            experiment.Experiment.reset_export_strategies,
            experiment.Experiment.extend_eval_hooks,
            experiment.Experiment.extend_eval_hooks,
            experiment.Experiment.train,
            experiment.Experiment.evaluate,
            experiment.Experiment.continuous_eval,
            experiment.Experiment.continuous_eval_on_train_data,
            experiment.Experiment.train_and_evaluate,
            experiment.Experiment.continuous_train_and_evaluate,
            experiment.Experiment.run_std_server,
            experiment.Experiment.test
        ],
        'functions': [
            experiment.create_experiment,
            experiment.run_experiment
        ],
    },
    {
        'page': 'experiments/estimator.md',
        'classes': [estimator.Estimator],
        'classes_functions': [
            estimator.Estimator.export_savedmodel,
            estimator.Estimator.train,
            estimator.Estimator.evaluate,
            estimator.Estimator.predict,
            estimator.Estimator.get_variable_value,
            estimator.Estimator.get_variable_names,
        ]
    },
    {
        'page': 'experiments/base_model.md',
        'classes': [models.BaseModel],
        'classes_functions': [
            models.BaseModel._clip_gradients_fn,
            models.BaseModel._build_optimizer,
            models.BaseModel._build_summary_op,
            models.BaseModel._build_loss,
            models.BaseModel._build_eval_metrics,
            models.BaseModel._build_train_op,
            models.BaseModel._preprocess,
            models.BaseModel._build_predictions,
            models.BaseModel._build,
            models.BaseModel.batch_size
        ]
    },
    {
        'page': 'experiments/models.md',
        'classes': [
            models.Regressor,
            models.Classifier,
            models.Generator
        ],
    },
    {
        'page': 'experiments/subgraph.md',
        'classes': [subgraph.SubGraph]
    },
    {
        'page': 'experiments/summarizer.md',
        'classes': [summarizer.SummaryOptions, summarizer.SummaryTypes],
        'functions': [
            summarizer.add_learning_rate_summaries,
            summarizer.add_loss_summaries,
            summarizer.add_activations_summary,
            summarizer.add_gradients_summary,
            summarizer.add_trainable_vars_summary,
        ],
    },
    {
        'page': 'experiments/hooks.md',
        'classes': hooks.HOOKS.values()
    },

    {
        'page': 'layers/core.md',
        'classes': [
            core.FullyConnected,
            core.Dropout,
            core.Reshape,
            core.Flatten,
            core.SingleUnit,
            core.Highway,
            core.OneHotEncoding,
            core.GaussianNoise,
            core.Merge,
            core.Slice
        ],
    },
    {
        'page': 'layers/convolutional.md',
        'classes': [
            convolutional.Conv2d,
            convolutional.Conv2dTranspose,
            convolutional.MaxPool2d,
            convolutional.AvgPool2d,
            convolutional.Upsample2d,
            convolutional.HighwayConv2d,
            convolutional.Upscore,
            convolutional.Conv1d,
            convolutional.MaxPool1d,
            convolutional.AvgPool1d,
            convolutional.HighwayConv1d,
            convolutional.Conv3d,
            convolutional.Conv3dTranspose,
            convolutional.MaxPool3d,
            convolutional.AvgPool3d,
            convolutional.GlobalMaxPool,
            convolutional.GlobalAvgPool,
            convolutional.ResidualBlock,
            convolutional.ResidualBottleneck,
        ],
    },
    {
        'page': 'layers/recurrent.md',
        'classes': [
            recurrent.SimpleRNN,
            recurrent.LSTM,
            recurrent.GRU,
            recurrent.BidirectionalRNN,
            recurrent.BasicRNNCell,
            recurrent.GRUCell,
            recurrent.BasicLSTMCell,
            recurrent.DropoutWrapper,
            recurrent.MultiRNNCell
        ],
    },
    {
        'page': 'layers/embeddings.md',
        'classes': [
            embedding.Embedding,
        ],
    },
    {
        'page': 'layers/normalizations.md',
        'classes': [
            normalizations.BatchNormalization,
            normalizations.LocalResponseNormalization,
            normalizations.L2Normalization
        ],
    },
    {
        'page': 'processing/categorical_vocabulary.md',
        'classes': [CategoricalVocabulary],
        'classes_functions': [
            CategoricalVocabulary.freeze,
            CategoricalVocabulary.get,
            CategoricalVocabulary.add,
            CategoricalVocabulary.trim,
            CategoricalVocabulary.reverse

        ]
    },
{
        'page': 'processing/categorical_processor.md',
        'classes': [CategoricalProcessor],
        'classes_functions': [
            CategoricalProcessor.freeze,
            CategoricalProcessor.fit,
            CategoricalProcessor.transform,
            CategoricalProcessor.fit_transform,

        ]
    },
    {
        'page': 'processing/vocabulary_processor.md',
        'classes': [VocabularyProcessor],
        'classes_functions': [
            VocabularyProcessor.fit,
            VocabularyProcessor.transform,
            VocabularyProcessor.fit_transform,
            VocabularyProcessor.reverse,
            VocabularyProcessor.save,
            VocabularyProcessor.restore,
        ]
    },
    {
        'page': 'processing/image.md',
        'all_module_functions': [image],
        'all_module_classes': [image],
    },
    {
        'page': 'processing/input_fn.md',
        'functions': [create_input_data_fn]
    },
    {
        'page': 'processing/pipelines.md',
        'classes': [
            pipelines.Pipeline,
            pipelines.TFRecordImagePipeline,
            pipelines.ParallelTextPipeline,
            pipelines.TFRecordSourceSequencePipeline,
            pipelines.ImageCaptioningPipeline
        ]
    },
    {
        'page': 'processing/data_decoders.md',
        'classes': [
            DataDecoder,
            TFExampleDecoder,
            SplitTokensDecoder,
            TFSequenceExampleDecoder
        ]
    },
    {
        'page': 'processing/data_providers.md',
        'classes': [
            Dataset,
            DataProvider,
            DatasetDataProvider,
            ParallelDatasetProvider
        ]
    },
    {
        'page': 'libs/configs.md',
        'all_module_classes': [configs],
        'all_module_functions': [configs]
    },
    {
        'page': 'libs/getters.md',
        'all_module_functions': [getters]
    },
    {
        'page': 'libs/utils.md',
        'all_module_functions': [utils]
    },

    {
        'page': 'activations.md',
        'all_module_functions': [activations],
    },
    {
        'page': 'initializations.md',
        'all_module_functions': [initializations],
    },
    {
        'page': 'metrics.md',
        'all_module_functions': [metrics],
    },
    {
        'page': 'losses.md',
        'all_module_functions': [losses],
    },
    {
        'page': 'regularizations.md',
        'all_module_functions': [regularizations],
    },
    {
        'page': 'optimizers.md',
        'all_module_functions': [optimizers],
    },
    {
        'page': 'variables.md',
        'all_module_functions': [variables],
    },
    {
        'page': 'datasets/converters.md',
        'classes': [
            ImageReader,
            PNGImageReader,
            PNGNumpyImageReader,
            JPGNumpyImageReader,
            JPEGImageReader,
            ImagesToTFExampleConverter
        ],
    },
    {
        'page': 'datasets/cifar10.md',
        'all_module_functions': [cifar10],
    },
    {
        'page': 'datasets/flowers17.md',
        'all_module_functions': [flowers17],
    },
    {
        'page': 'datasets/mnist.md',
        'all_module_functions': [mnist],
    },
]

KEYWORDS = ['Examples', 'Arguments', 'Attributes', 'Returns',
            'Raises', 'References', 'Links', 'Yields']

EXCLUDE = ['check_loss_data', 'built_loss']

DOC_DIR = os.path.dirname(os.path.realpath(__file__))
BASE_DIR = os.path.abspath(os.path.join(DOC_DIR, os.pardir))
TEMPLATES_DIR = os.path.join(DOC_DIR, 'templates')
SOURCES_DIR = os.path.join(DOC_DIR, 'sources')


def get_module_name(module_name):
    assert module_name[:len('polyaxon.')] == 'polyaxon.', "Got wrong module {}".format(module_name)
    return module_name[:len('polyaxon.')]


def get_earliest_class_that_defined_member(member, cls):
    ancestors = get_classes_ancestors([cls])
    result = None
    for ancestor in ancestors:
        if member in dir(ancestor):
            result = ancestor
    if not result:
        return cls
    return result


def get_classes_ancestors(classes):
    ancestors = []
    for cls in classes:
        ancestors += cls.__bases__
    filtered_ancestors = []
    for ancestor in ancestors:
        if ancestor.__name__ in ['object']:
            continue
        filtered_ancestors.append(ancestor)
    if filtered_ancestors:
        return filtered_ancestors + get_classes_ancestors(filtered_ancestors)
    else:
        return filtered_ancestors


def get_function_signature(function, method=True):
    signature = getattr(function, '_legacy_support_signature', None)
    if signature is None:
        signature = inspect.getargspec(function)
    defaults = signature.defaults
    if method:
        args = signature.args[1:]
    else:
        args = signature.args
    if defaults:
        kwargs = zip(args[-len(defaults):], defaults)
        args = args[:-len(defaults)]
    else:
        kwargs = []
    st = '%s.%s(' % (function.__module__, function.__name__)
    for a in args:
        st += str(a) + ', '
    for a, v in kwargs:
        if isinstance(v, str):
            v = '\'' + v + '\''
        st += str(a) + '=' + str(v) + ', '
    if kwargs or args:
        return st[:-2] + ')'
    else:
        return st + ')'


def get_class_signature(cls):
    try:
        class_signature = get_function_signature(cls.__init__)
        class_signature = class_signature.replace('__init__', cls.__name__)
    except:
        # in case the class inherits from object and does not
        # define __init__
        class_signature = cls.__module__ + '.' + cls.__name__ + '()'
    return class_signature


def class_to_docs_link(cls):
    module_name = cls.__module__
    module_name = get_module_name(module_name)
    link = ROOT + module_name.replace('.', '/') + '#' + cls.__name__.lower()
    return link


def class_to_source_link(cls):
    module_name = cls.__module__
    get_module_name(module_name)
    path = module_name.replace('.', '/')
    path += '.py'
    line = inspect.getsourcelines(cls)[-1]
    link = 'https://github.com/polyaxon/polyaxon/blob/master/' + path + '#L' + str(line)
    return '[[source]](' + link + ')'


def code_snippet(snippet):
    result = '```python\n'
    result += snippet + '\n'
    result += '```\n'
    return result


def process_class(cls):

    def process_docstring(docstring):
        docstring = re.sub(r'    ([^\s\\\(]+):(.*)\n', r'    - __\1__:\2\n', docstring)
        docstring = docstring.replace('    ' * 3, '\t\t')
        docstring = docstring.replace('    ' * 2, '\t')
        docstring = docstring.replace('    ', '')
        return docstring

    subblocks = []
    signature = get_class_signature(cls)
    subblocks.append('<span style="float:right;">' + class_to_source_link(cls) + '</span>')
    subblocks.append('## ' + cls.__name__ + '\n')
    subblocks.append(code_snippet(signature))
    docstring = cls.__doc__
    if docstring:
        subblocks.append(process_docstring(docstring))

    return subblocks


def process_function(function, class_function=False):

    def process_docstring(docstring):
        docstring = re.sub(r'    ([^\s\\\(]+):(.*)\n', r'    - __\1__:\2\n', docstring)

        docstring = docstring.replace('    ' * (5 if class_function else 4), '\t\t')
        docstring = docstring.replace('    ' * (3 if class_function else 2), '\t')
        docstring = docstring.replace('    ', '')
        return docstring

    subblocks = []
    signature = get_function_signature(function, method=False)
    signature = signature.replace(function.__module__ + '.', '')
    subblocks.append(('### ' if class_function else '## ') + function.__name__ + '\n')
    subblocks.append(code_snippet(signature))
    docstring = function.__doc__
    if docstring:
        subblocks.append(process_docstring(docstring))
    return subblocks


print('Cleaning up existing sources directory.')
if os.path.exists(SOURCES_DIR):
    shutil.rmtree(SOURCES_DIR)

print('Populating sources directory with templates.')
for subdir, dirs, fnames in os.walk(TEMPLATES_DIR):
    for fname in fnames:
        new_subdir = subdir.replace(TEMPLATES_DIR, SOURCES_DIR)
        if not os.path.exists(new_subdir):
            os.makedirs(new_subdir)
        if fname[-3:] == '.md':
            fpath = os.path.join(subdir, fname)
            new_fpath = fpath.replace(TEMPLATES_DIR, SOURCES_DIR)
            shutil.copy(fpath, new_fpath)

print('Starting autogeneration.')
for page_data in PAGES:
    blocks = []
    classes = page_data.get('classes', [])
    for module in page_data.get('all_module_classes', []):
        module_classes = []
        for name in dir(module):
            if name[0] == '_' or name in EXCLUDE:
                continue
            module_member = getattr(module, name)
            if inspect.isclass(module_member):
                cls = module_member
                if cls.__module__ == module.__name__:
                    if cls not in module_classes:
                        module_classes.append(cls)
        module_classes.sort(key=lambda x: id(x))
        classes += module_classes

    for cls in classes:
        blocks.append('\n'.join(process_class(cls)))

    functions = page_data.get('classes_functions', [])
    for function in functions:
        blocks.append('\n\n'.join(process_function(function, class_function=True)))

    functions = page_data.get('functions', [])
    for module in page_data.get('all_module_functions', []):
        module_functions = []
        for name in dir(module):
            if name[0] == '_' or name in EXCLUDE:
                continue
            module_member = getattr(module, name)
            if inspect.isfunction(module_member):
                function = module_member
                if module.__name__ in function.__module__:
                    if function not in module_functions:
                        module_functions.append(function)
        module_functions.sort(key=lambda x: id(x))
        functions += module_functions

    for function in functions:
        blocks.append('\n\n'.join(process_function(function)))

    if not blocks:
        raise RuntimeError('Found no content for page ' + page_data['page'])

    mkdown = '\n\n----\n\n'.join(blocks)
    # save module page.
    # Either insert content into existing page,
    # or create page otherwise
    page_name = page_data['page']
    path = os.path.join(SOURCES_DIR, page_name)
    if os.path.exists(path):
        template = open(path).read()
        assert '{{autogenerated}}' in template, ('Template found for ' + path +
                                                 ' but missing {{autogenerated}} tag.')
        mkdown = template.replace('{{autogenerated}}', mkdown)
        print('...inserting autogenerated content into template:', path)
    else:
        print('...creating new page with autogenerated content:', path)
    subdir = os.path.dirname(path)
    if not os.path.exists(subdir):
        os.makedirs(subdir)
    open(path, 'w').write(mkdown)

shutil.copyfile(os.path.join(BASE_DIR, 'README.md'),
                os.path.join(SOURCES_DIR, 'index.md'))
shutil.copyfile(os.path.join(BASE_DIR, 'CONTRIBUTING.md'),
                os.path.join(SOURCES_DIR, 'contributing.md'))
