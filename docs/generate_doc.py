import inspect
import os.path
import re
import shutil

from polyaxon_schemas import (
    constraints,
    initializations,
    metrics,
    losses,
    regularizations,
    optimizers, bridges)

from polyaxon_schemas import models
from polyaxon_schemas.layers import (
    advanced_activations,
    convolutional,
    convolutional_recurrent,
    core,
    embeddings,
    local,
    merge,
    noise,
    normalization,
    pooling,
    recurrent,
    wrappers,
)
from polyaxon_schemas.processing.image import (
    ResizeConfig,
    CentralCropConfig,
    RandomCropConfig,
    ExtractGlimpseConfig,
    ToBoundingBoxConfig,
    FlipConfig,
    TransposeConfig,
    Rotate90Config,
    ConvertColorSpaceConfig,
    ConvertImagesDtypeConfig,
    AdjustBrightnessConfig,
    AdjustContrastConfig,
    AdjustHueConfig,
    AdjustSaturationConfig,
    AdjustGammaConfig,
    StandardizationConfig,
    DrawBoundingBoxesConfig,
    TotalVariationConfig,
)
from polyaxon_schemas.processing.pipelines import (
    TFRecordImagePipelineConfig,
    TFRecordSequencePipelineConfig,
    ParallelTextPipelineConfig,
    TFRecordSourceSequencePipelineConfig,
    ImageCaptioningPipelineConfig,
)

ROOT = 'https://docs.polyaxon.com/'

LIB_URL = 'https://github.com/polyaxon/polyaxon/blob/master/'
SCHEMAS_URL = 'https://github.com/polyaxon/polyaxon-schemas/blob/master/'
CLI_URL = 'https://github.com/polyaxon/polyaxon-cli/blob/master/'

PAGES = []

PAGES.append(
    (LIB_URL, [
        # Models
        {
            'page': 'polyaxon_lib/models.md',
            'classes': [models.ClassifierConfig, models.RegressorConfig, models.GeneratorConfig],
        },
        # Layers
        {
            'page': 'polyaxon_lib/layers/advanced_activations.md',
            'classes': [
                advanced_activations.LeakyReLUConfig,
                advanced_activations.PReLUConfig,
                advanced_activations.ELUConfig,
                advanced_activations.ThresholdedReLUConfig,
            ],
        },
        {
            'page': 'polyaxon_lib/layers/core.md',
            'classes': [
                core.MaskingConfig,
                core.DropoutConfig,
                core.SpatialDropout1DConfig,
                core.SpatialDropout2DConfig,
                core.SpatialDropout3DConfig,
                core.ActivationConfig,
                core.ReshapeConfig,
                core.PermuteConfig,
                core.FlattenConfig,
                core.RepeatVectorConfig,
                core.DenseConfig,
                core.ActivityRegularizationConfig,
                core.CastConfig,
            ],
        },
        {
            'page': 'polyaxon_lib/layers/convolutional.md',
            'classes': [
                convolutional.Conv1DConfig,
                convolutional.Conv2DConfig,
                convolutional.Conv3DConfig,
                convolutional.Conv2DTransposeConfig,
                convolutional.Conv3DTransposeConfig,
                convolutional.SeparableConv2DConfig,
                convolutional.UpSampling1DConfig,
                convolutional.UpSampling2DConfig,
                convolutional.UpSampling3DConfig,
                convolutional.ZeroPadding1DConfig,
                convolutional.ZeroPadding2DConfig,
                convolutional.ZeroPadding3DConfig,
                convolutional.Cropping1DConfig,
                convolutional.Cropping2DConfig,
                convolutional.Cropping3DConfig,
            ],
        },
        {
            'page': 'polyaxon_lib/layers/convolutional_recurrent.md',
            'classes': [
                convolutional_recurrent.ConvLSTM2DConfig,
            ]
        },
        {
            'page': 'polyaxon_lib/layers/local.md',
            'classes': [
                local.LocallyConnected1DConfig,
                local.LocallyConnected2DConfig,
            ]
        },
        {
            'page': 'polyaxon_lib/layers/merge.md',
            'classes': [
                merge.AddConfig,
                merge.MultiplyConfig,
                merge.AverageConfig,
                merge.MaximumConfig,
                merge.ConcatenateConfig,
                merge.DotConfig,
            ]
        },
        {
            'page': 'polyaxon_lib/layers/noise.md',
            'classes': [
                noise.GaussianNoiseConfig,
                noise.GaussianDropoutConfig,
                noise.AlphaDropoutConfig,
            ]
        },
        {
            'page': 'polyaxon_lib/layers/pooling.md',
            'classes': [
                pooling.AveragePooling1DConfig,
                pooling.MaxPooling1DConfig,
                pooling.AveragePooling2DConfig,
                pooling.MaxPooling2DConfig,
                pooling.AveragePooling3DConfig,
                pooling.MaxPooling3DConfig,
                pooling.GlobalAveragePooling1DConfig,
                pooling.GlobalMaxPooling1DConfig,
                pooling.GlobalAveragePooling2DConfig,
                pooling.GlobalMaxPooling2DConfig,
                pooling.GlobalAveragePooling3DConfig,
                pooling.GlobalMaxPooling3DConfig,
            ]
        },
        {
            'page': 'polyaxon_lib/layers/recurrent.md',
            'classes': [
                recurrent.RecurrentConfig,
                recurrent.SimpleRNNConfig,
                recurrent.LSTMConfig,
                recurrent.GRUConfig,
            ],
        },
        {
            'page': 'polyaxon_lib/layers/embeddings.md',
            'classes': [
                embeddings.EmbeddingConfig,
            ],
        },
        {
            'page': 'polyaxon_lib/layers/normalizations.md',
            'classes': [
                normalization.BatchNormalizationConfig,
                # normalizations.LocalResponseNormalization,
                # normalizations.L2Normalization
            ],
        },
        {
            'page': 'polyaxon_lib/layers/wrappers.md',
            'classes': [
                wrappers.WrapperConfig,
                wrappers.TimeDistributedConfig,
                wrappers.BidirectionalConfig,
            ]
        },

        # Bridges
        {
            'page': 'polyaxon_lib/bridges.md',
            'classes': [
                bridges.NoOpBridgeConfig,
                bridges.LatentBridgeConfig,
            ]
        },

        # Processing
        {
            'page': 'polyaxon_lib/processing/image.md',
            'classes': [
                ResizeConfig,
                CentralCropConfig,
                RandomCropConfig,
                ExtractGlimpseConfig,
                ToBoundingBoxConfig,
                FlipConfig,
                TransposeConfig,
                Rotate90Config,
                ConvertColorSpaceConfig,
                ConvertImagesDtypeConfig,
                AdjustBrightnessConfig,
                AdjustContrastConfig,
                AdjustHueConfig,
                AdjustSaturationConfig,
                AdjustGammaConfig,
                StandardizationConfig,
                DrawBoundingBoxesConfig,
                TotalVariationConfig,
            ],
        },
        {
            'page': 'polyaxon_lib/processing/pipelines.md',
            'classes': [
                TFRecordImagePipelineConfig,
                TFRecordSequencePipelineConfig,
                ParallelTextPipelineConfig,
                TFRecordSourceSequencePipelineConfig,
                ImageCaptioningPipelineConfig,
            ]
        },
        {
            'page': 'polyaxon_lib/initializations.md',
            'classes': [
                initializations.ZerosInitializerConfig,
                initializations.OnesInitializerConfig,
                initializations.ConstantInitializerConfig,
                initializations.UniformInitializerConfig,
                initializations.NormalInitializerConfig,
                initializations.TruncatedNormalInitializerConfig,
                initializations.VarianceScalingInitializerConfig,
                initializations.IdentityInitializerConfig,
                initializations.OrthogonalInitializerConfig,
                initializations.GlorotUniformInitializerConfig,
                initializations.GlorotNormalInitializerConfig,
                initializations.HeUniformInitializerConfig,
                initializations.HeNormalInitializerConfig,
                initializations.LecunUniformInitializerConfig,
                initializations.LecunNormalInitializerConfig

            ],
        },
        {
            'page': 'polyaxon_lib/constraints.md',
            'classes': [
                constraints.MaxNormConfig,
                constraints.NonNegConfig,
                constraints.UnitNormConfig,
                constraints.MinMaxNormConfig,
            ],
        },
        {
            'page': 'polyaxon_lib/metrics.md',
            'classes': [
                metrics.TruePositivesConfig,
                metrics.TruePositivesConfig,
                metrics.TruePositivesConfig,
                metrics.TrueNegativesConfig,
                metrics.FalsePositivesConfig,
                metrics.FalseNegativesConfig,
                metrics.MeanConfig,
                metrics.MeanTensorConfig,
                metrics.AccuracyConfig,
                metrics.PrecisionConfig,
                metrics.RecallConfig,
                metrics.AUCConfig,
                metrics.SpecificityAtSensitivityConfig,
                metrics.SensitivityAtSpecificityConfig,
                metrics.PrecisionAtThresholdsConfig,
                metrics.RecallAtThresholdsConfig,
                metrics.SparseRecallAtKConfig,
                metrics.SparsePrecisionAtKConfig,
                metrics.MeanAbsoluteErrorConfig,
                metrics.MeanRelativeErrorConfig,
                metrics.MeanSquaredErrorConfig,
                metrics.RootMeanSquaredErrorConfig,
                metrics.CovarianceConfig,
                metrics.PearsonCorrelationConfig,
                metrics.MeanCosineDistanceConfig,
                metrics.PercentageLessConfig,
                metrics.MeanIOUConfig,
            ],
        },
        {
            'page': 'polyaxon_lib/losses.md',
            'classes': [
                losses.AbsoluteDifferenceConfig,
                losses.AbsoluteDifferenceConfig,
                losses.MeanSquaredErrorConfig,
                losses.LogLossConfig,
                losses.HuberLossConfig,
                losses.ClippedDeltaLossConfig,
                losses.SoftmaxCrossEntropyConfig,
                losses.SigmoidCrossEntropyConfig,
                losses.HingeLossConfig,
                losses.CosineDistanceConfig,
                losses.KullbackLeiberDivergenceConfig,
            ],
        },
        {
            'page': 'polyaxon_lib/regularizers.md',
            'classes': [
                regularizations.L1RegularizerConfig,
                regularizations.L2RegularizerConfig,
                regularizations.L1L2RegularizerConfig,
            ],
        },
        {
            'page': 'polyaxon_lib/optimizers.md',
            'classes': [
                optimizers.SGDConfig,
                optimizers.MomentumConfig,
                optimizers.NestrovConfig,
                optimizers.RMSPropConfig,
                optimizers.AdamConfig,
                optimizers.AdagradConfig,
                optimizers.AdadeltaConfig,
                optimizers.FtrlConfig,
            ],
        },
    ]))

KEYWORDS = ['Examples', 'Args', 'Arguments', 'Attributes', 'Returns',
            'Raises', 'References', 'Links', 'Yields', 'Programmatic usage',
            'Polyaxonfile usage', 'Input shape', 'Output shape']

EXCLUDE = ['check_loss_data', 'built_loss']

BASE_DIR = os.path.dirname(os.path.realpath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
DOCS_DIR = os.path.join(BASE_DIR, 'docs')


def is_polyaxon_lib_module(module_name):
    return module_name[:len('polyaxon.')] == 'polyaxon.'


def is_polyaxon_cli_module(module_name):
    return module_name[:len('polyaxon_cli.')] == 'polyaxon_cli.'


def is_polyaxon_schemas_module(module_name):
    return module_name[:len('polyaxon_schemas.')] == 'polyaxon_schemas.'


def is_polyaxon_module(module_name):
    return (is_polyaxon_lib_module(module_name) or
            is_polyaxon_cli_module(module_name) or
            is_polyaxon_schemas_module(module_name))


def get_module_name(module_name):
    if is_polyaxon_lib_module(module_name):
        return module_name[:len('polyaxon.')]
    if is_polyaxon_cli_module(module_name):
        return module_name[:len('polyaxon_cli.')]
    if is_polyaxon_schemas_module(module_name):
        return module_name[:len('polyaxon_schemas.')]

    raise "Got wrong module {}".format(module_name)


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


def obj_to_source_link(source_url, obj, obj_schema=None):
    def get_module_link(module, url):
        module_name = module.__module__
        get_module_name(module_name)
        path = module_name.replace('.', '/')
        path += '.py'
        line = inspect.getsourcelines(obj)[-1]
        return url + path + '#L' + str(line)

    obj_link = get_module_link(obj, source_url)
    link_template = '[[{}]]({})'

    obj_url = link_template.format('source', obj_link)
    if not obj_schema:
        return obj_url

    schema_link = get_module_link(obj_schema, SCHEMAS_URL)
    schema_url = link_template.format('schema source', schema_link)
    return '{} {}'.format(obj_url, schema_url)


def code_snippet(snippet):
    result = '```python\n'
    result += snippet + '\n'
    result += '```\n'
    return result


def process_docstring(docstring, line_processor):
    processed = []
    inside_snippet = False
    for line_string in docstring.split('\n'):
        if '```' in line_string:
            inside_snippet = not inside_snippet

        for keyword in KEYWORDS:
            line_string = re.sub(r'    ({})(\(.*\)):'.format(keyword),
                                 r'    - __\1__\2\n\n', line_string)

        if not inside_snippet:
            line_string = re.sub(r'    ([^\s\\\(]+):(.*)', r'    - __\1__:\2\n', line_string)

        processed.append(line_processor(line_string))

    return '\n'.join(processed)


def process_class(cls, source_url):
    def process_line_string(line_string):
        line_string = line_string.replace('    ' * 4, '\t\t\t')
        line_string = line_string.replace('    ' * 3, '\t\t')
        line_string = line_string.replace('    ' * 2, '\t')
        line_string = line_string.replace('    ', '')
        return line_string

    cls_schema = None
    if isinstance(cls, tuple):
        cls_schema = cls[1]
        cls = cls[0]

    subblocks = []
    signature = get_class_signature(cls)
    class_source_link = obj_to_source_link(source_url, cls, cls_schema)
    subblocks.append('<span style="float:right;">' + class_source_link + '</span>')
    subblocks.append('## ' + cls.__name__ + '\n')
    subblocks.append(code_snippet(signature))
    docstring = cls.__doc__ if not cls_schema else cls_schema.__doc__
    if docstring:
        subblocks.append(process_docstring(docstring, process_line_string))

    return subblocks


def process_function(function, source_url, class_function=False):
    def process_line_string(line_string):
        line_string = line_string.replace('    ' * (5 if class_function else 4), '\t\t')
        line_string = line_string.replace('    ' * (3 if class_function else 2), '\t')
        line_string = line_string.replace('    ', '')
        return line_string

    subblocks = []
    signature = get_function_signature(function, method=False)
    if not class_function and is_polyaxon_module(function.__module__):
        function_source_link = obj_to_source_link(source_url, function)
        subblocks.append('<span style="float:right;">' + function_source_link + '</span>')
    signature = signature.replace(function.__module__ + '.', '')
    subblocks.append(('### ' if class_function else '## ') + function.__name__ + '\n')
    subblocks.append(code_snippet(signature))
    docstring = function.__doc__
    if docstring:
        subblocks.append(process_docstring(docstring, process_line_string))
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


def process_pages(pages, source_url):
    for page_data in pages:
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
            blocks.append('\n'.join(process_class(cls, source_url)))

        functions = page_data.get('classes_functions', [])
        for function in functions:
            blocks.append('\n\n'.join(process_function(function, source_url, class_function=True)))

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
            blocks.append('\n\n'.join(process_function(function, source_url)))

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


for source_url, pages in PAGES:
    process_pages(pages, source_url)

shutil.copyfile(os.path.join(BASE_DIR, 'CONTRIBUTING.md'),
                os.path.join(DOCS_DIR, 'contributing.md'))
shutil.rmtree(os.path.join(DOCS_DIR, 'images'))
shutil.copytree(os.path.join(TEMPLATES_DIR, 'images'),
                os.path.join(DOCS_DIR, 'images'))
shutil.rmtree(os.path.join(DOCS_DIR, 'css'))
shutil.copytree(os.path.join(TEMPLATES_DIR, 'css'),
                os.path.join(DOCS_DIR, 'css'))
