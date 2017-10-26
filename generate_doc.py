# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

import inspect
import os.path
import re
import shutil

from polyaxon import (
    activations,
    constraints,
    initializations,
    metrics,
    losses,
    regularizations,
    optimizers,
    explorations,
    variables)
from polyaxon import bridges

from polyaxon import models
from polyaxon.datasets import cifar10, flowers17, mnist
from polyaxon.datasets.converters import (
    ImageReader,
    PNGImageReader,
    PNGNumpyImageReader,
    JPGNumpyImageReader,
    JPEGImageReader,
    ImagesToTFExampleConverter
)
from polyaxon.estimators import estimator, agents, hooks
from polyaxon.experiments import experiment, rl_experiment, utils as experiment_utils
from polyaxon.layers import (
    advanced_activations,
    convolutional,
    convolutional_recurrent,
    core,
    embeddings,
    local,
    merge,
    noise,
    normalizations,
    pooling,
    recurrent,
    wrappers,
)
from polyaxon.libs import getters, utils
from polyaxon.models import summarizer
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
from polyaxon.rl.environments import EnvSpec, GymEnvironment
from polyaxon.rl.environments import Environment
from polyaxon.rl.memories import Memory, BatchMemory
from polyaxon.rl import utils as rl_utils

ROOT = 'http://polyaxon.com/docs/'

PAGES = [
    # Experiments
    {
        'page': 'experiments/experiment.md',
        'classes': [experiment.Experiment],
        'classes_functions': [
            experiment.Experiment.reset_export_strategies,
            experiment.Experiment.train,
            experiment.Experiment.evaluate,
            experiment.Experiment.continuous_eval,
            experiment.Experiment.continuous_eval_on_train_data,
            experiment.Experiment.train_and_evaluate,
            experiment.Experiment.continuous_train_and_eval,
            experiment.Experiment.run_std_server,
            experiment.Experiment.test
        ],
    },
    {
        'page': 'experiments/rl_experiment.md',
        'classes': [rl_experiment.RLExperiment],
        'classes_functions': [
            rl_experiment.RLExperiment.reset_export_strategies,
            rl_experiment.RLExperiment.train,
            rl_experiment.RLExperiment.evaluate,
            rl_experiment.RLExperiment.continuous_eval,
            rl_experiment.RLExperiment.continuous_eval_on_train_data,
            rl_experiment.RLExperiment.train_and_evaluate,
            rl_experiment.RLExperiment.continuous_train_and_eval,
            rl_experiment.RLExperiment.run_std_server,
            rl_experiment.RLExperiment.test
        ],
    },
    {
        'page': 'experiments/utils.md',
        'functions': [experiment_utils.run_experiment]
    },

    # Estimators
    {
        'page': 'estimators/estimator.md',
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
    # Agents
    {
        'page': 'agents/agent.md',
        'classes': [agents.Agent],
        'classes_functions': [
            agents.Agent.train,
            agents.Agent.run_episode,
        ]
    },
    {
        'page': 'agents/pg_agent.md',
        'classes': [agents.PGAgent],
        'classes_functions': [
            agents.PGAgent.train,
            agents.PGAgent.run_episode,
        ]
    },
    {
        'page': 'agents/trpo_agent.md',
        'classes': [agents.TRPOAgent],
        'classes_functions': [
            agents.TRPOAgent.train,
            agents.TRPOAgent.run_episode,
        ]
    },

    # Hooks
    {
        'page': 'hooks/general_hooks.md',
        'classes': hooks.GENERAL_HOOKS.values()
    },
    {
        'page': 'hooks/step_hooks.md',
        'classes': hooks.STEP_HOOKS.values()
    },
    {
        'page': 'hooks/episode_hooks.md',
        'classes': hooks.EPISODE_HOOKS.values()
    },

    # Models
    {
        'page': 'models/base_model.md',
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
    # RL Models
    {
        'page': 'models/base_rl_q_model.md',
        'classes': [models.BaseQModel],
        'classes_functions': [
            models.BaseQModel._build_exploration,
            models.BaseQModel._build_actions,
            models.BaseQModel._build_graph_fn,
            models.BaseQModel._call_graph_fn,
            models.BaseQModel._build_update_target_graph,
            models.BaseQModel._build_train_op,
            models.BaseQModel._preprocess,
        ]
    },
    {
        'page': 'models/base_rl_pg_model.md',
        'classes': [models.BasePGModel],
        'classes_functions': [
            models.BasePGModel._build_actions,
            models.BasePGModel._build_distribution,
            models.BasePGModel._build_graph_fn,
            models.BasePGModel._call_graph_fn,
            models.BasePGModel._preprocess,
        ]
    },
    {
        'page': 'models/models.md',
        'classes': [
            models.Regressor,
            models.Classifier,
            models.Generator,
        ],
    },
    {
        'page': 'models/rl_q_models.md',
        'classes': [
            models.DQNModel,
            models.DDQNModel,
            models.NAFModel,
        ],
    },
    {
        'page': 'models/rl_pg_models.md',
        'classes': [
            models.VPGModel,
            models.TRPOModel,
        ],
    },
    {
        'page': 'models/summarizer.md',
        'classes': [summarizer.SummaryOptions, summarizer.SummaryTypes],
        'functions': [
            summarizer.add_learning_rate_summaries,
            summarizer.add_loss_summaries,
            summarizer.add_activations_summary,
            summarizer.add_gradients_summary,
            summarizer.add_trainable_vars_summary,
        ],
    },

    # Layers
    {
        'page': 'layers/advanced_activations.md',
        'classes': [
            advanced_activations.LeakyReLU,
            advanced_activations.PReLU,
            advanced_activations.ELU,
            advanced_activations.ThresholdedReLU,
        ],
    },
    {
        'page': 'layers/core.md',
        'classes': [
            core.Masking,
            core.Dropout,
            core.SpatialDropout1D,
            core.SpatialDropout2D,
            core.SpatialDropout3D,
            core.Activation,
            core.Reshape,
            core.Permute,
            core.Flatten,
            core.RepeatVector,
            core.Lambda,
            core.Dense,
            core.ActivityRegularization,
            core.Cast,
        ],
    },
    {
        'page': 'layers/convolutional.md',
        'classes': [
            convolutional.Conv1D,
            convolutional.Conv2D,
            convolutional.Conv3D,
            convolutional.Conv2DTranspose,
            convolutional.Conv3DTranspose,
            convolutional.SeparableConv2D,
            convolutional.UpSampling1D,
            convolutional.UpSampling2D,
            convolutional.UpSampling3D,
            convolutional.ZeroPadding1D,
            convolutional.ZeroPadding2D,
            convolutional.ZeroPadding3D,
            convolutional.Cropping1D,
            convolutional.Cropping2D,
            convolutional.Cropping3D,
        ],
    },
    {
        'page': 'layers/convolutional_recurrent.md',
        'classes': [
            convolutional_recurrent.ConvRecurrent2D,
            convolutional_recurrent.ConvLSTM2D
        ]
    },
    {
        'page': 'layers/local.md',
        'classes': [
            local.LocallyConnected1D,
            local.LocallyConnected2D
        ]
    },
    {
        'page': 'layers/merge.md',
        'classes': [
            merge.Add,
            merge.Multiply,
            merge.Average,
            merge.Maximum,
            merge.Concatenate,
            merge.Dot,
        ]
    },
    {
        'page': 'layers/noise.md',
        'classes': [
            noise.GaussianNoise,
            noise.GaussianDropout,
            noise.AlphaDropout,
        ]
    },
    {
        'page': 'layers/pooling.md',
        'classes': [
            pooling.AveragePooling1D,
            pooling.MaxPooling1D,
            pooling.AveragePooling2D,
            pooling.MaxPooling2D,
            pooling.AveragePooling3D,
            pooling.MaxPooling3D,
            pooling.GlobalAveragePooling1D,
            pooling.GlobalMaxPooling1D,
            pooling.GlobalAveragePooling2D,
            pooling.GlobalMaxPooling2D,
            pooling.GlobalAveragePooling3D,
            pooling.GlobalMaxPooling3D,
        ]
    },
    {
        'page': 'layers/recurrent.md',
        'classes': [
            recurrent.Recurrent,
            recurrent.SimpleRNN,
            recurrent.LSTM,
            recurrent.GRU
        ],
    },
    {
        'page': 'layers/embeddings.md',
        'classes': [
            embeddings.Embedding,
        ],
    },
    {
        'page': 'layers/normalizations.md',
        'classes': [
            normalizations.BatchNormalization,
            # normalizations.LocalResponseNormalization,
            # normalizations.L2Normalization
        ],
    },
    {
        'page': 'layers/wrappers.md',
        'classes': [
            wrappers.Wrapper,
            wrappers.TimeDistributed,
            wrappers.Bidirectional,
        ]
    },

    # Bridges
    {
        'page': 'bridges/base_bridge.md',
        'classes': [bridges.BaseBridge],
        'classes_functions': [
            bridges.BaseBridge.encode,
            bridges.BaseBridge.decode,
            bridges.BaseBridge._get_decoder_shape,
            bridges.BaseBridge._build
        ]
    },
    {
        'page': 'bridges/bridges.md',
        'classes': [bridges.NoOpBridge, bridges.LatentBridge]
    },

    # Processing
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

    # Libs
    {
        'page': 'libs/getters.md',
        'all_module_functions': [getters]
    },
    {
        'page': 'libs/utils.md',
        'all_module_functions': [utils]
    },

    # Other modules
    {
        'page': 'activations.md',
        'all_module_functions': [activations],
    },
    {
        'page': 'initializers.md',
        'all_module_classes': [initializations],
    },
    {
        'page': 'constraints.md',
        'classes': list(constraints.CONSTRAINTS.values()),
    },
    {
        'page': 'metrics.md',
        'functions': list(metrics.METRICS.values()),
    },
    {
        'page': 'losses.md',
        'all_module_functions': [losses],
    },
    {
        'page': 'regularizers.md',
        'functions': list(regularizations.REGULARIZERS.values()),
    },
    {
        'page': 'optimizers.md',
        'all_module_functions': [optimizers],
    },
    {
        'page': 'variables.md',
        'functions': [variables.variable],
    },

    # RL
    {
        'page': 'rl/environments.md',
        'classes': [EnvSpec, Environment, GymEnvironment],
    },
    {
        'page': 'rl/explorations.md',
        'all_module_functions': [explorations],
    },
    {
        'page': 'rl/memories.md',
        'classes': [Memory, BatchMemory],
    },
    {
        'page': 'rl/utils.md',
        'all_module_functions': [rl_utils],
    },

    # Datasets
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

KEYWORDS = ['Examples', 'Args', 'Arguments', 'Attributes', 'Returns',
            'Raises', 'References', 'Links', 'Yields']

EXCLUDE = ['check_loss_data', 'built_loss']

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')


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
        class_signature = cls.__module__ + '.' + cls.__name__ + class_signature.split('__init__')[1]
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
    link = 'https://github.com/polyaxon/polyaxon-docs/blob/master/' + path + '#L' + str(line)
    return '[[source]](' + link + ')'


def code_snippet(snippet):
    result = '```python\n'
    result += snippet + '\n'
    result += '```\n'
    return result


def process_class(cls):

    def process_docstring(docstring):
        indet_levels = [l for l in [len(line) - len(line.lstrip()) for line in docstring.split('\n')]
                      if l > 0]
        indent = min(indet_levels) if indet_levels else 0
        if indent == 2:
            docstring = re.sub(r'  ([^\s\\\(]+):(.*)\n', r'    - __\1__:\2\n', docstring)
        else:
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
if os.path.exists(DOCS_DIR):
    shutil.rmtree(DOCS_DIR)

print('Populating sources directory with templates.')
for subdir, dirs, fnames in os.walk(TEMPLATES_DIR):
    for fname in fnames:
        new_subdir = subdir.replace(TEMPLATES_DIR, DOCS_DIR)
        if not os.path.exists(new_subdir):
            os.makedirs(new_subdir)
        if fname[-3:] == '.md':
            fpath = os.path.join(subdir, fname)
            new_fpath = fpath.replace(TEMPLATES_DIR, DOCS_DIR)
            shutil.copy(fpath, new_fpath)

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
    path = os.path.join(DOCS_DIR, page_name)
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

shutil.copyfile(os.path.join(BASE_DIR, 'CONTRIBUTING.md'),
                os.path.join(DOCS_DIR, 'contributing.md'))
shutil.rmtree(os.path.join(DOCS_DIR, 'images'))
shutil.copytree(os.path.join(TEMPLATES_DIR, 'images'),
                os.path.join(DOCS_DIR, 'images'))
shutil.rmtree(os.path.join(DOCS_DIR, 'css'))
shutil.copytree(os.path.join(TEMPLATES_DIR, 'css'),
                os.path.join(DOCS_DIR, 'css'))
