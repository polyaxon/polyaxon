# -*- coding: utf-8 -*-
from __future__ import absolute_import, division, print_function

from tensorflow.contrib.learn.python.learn import export_strategy
from tensorflow.contrib.learn.python.learn.utils.saved_model_export_utils import (
    garbage_collect_exports
)


def make_export_strategy(serving_input_fn, assets_extra=None, as_text=False, exports_to_keep=5):
    """Create an ExportStrategy for use with Experiment.
        Args:
            serving_input_fn: A function that takes no arguments and returns an `InputFnOps`.
            assets_extra: A dict specifying how to populate the assets.extra directory
                within the exported SavedModel.  Each key should give the destination
                path (including the filename) relative to the assets.extra directory.
                The corresponding value gives the full path of the source file to be
                copied.  For example, the simple case of copying a single file without
                renaming it is specified as
                `{'my_asset_file.txt': '/path/to/my_asset_file.txt'}`.
            as_text: whether to write the SavedModel proto in text format.
            exports_to_keep: Number of exports to keep.  Older exports will be
                garbage-collected.  Defaults to 5.  Set to None to disable garbage collection.
        Returns:
            An ExportStrategy that can be passed to the Experiment constructor.
      """

    def export_fn(estimator, export_dir_base, checkpoint_path=None):
        """Exports the given Estimator as a SavedModel.

        Args:
            estimator: the Estimator to export.
            export_dir_base: A string containing a directory to write the exported
                graph and checkpoints.
            checkpoint_path: The checkpoint path to export.  If None (the default),
                the most recent checkpoint found within the model directory is chosen.
        Returns:
            The string path to the exported directory.
        Raises:
            ValueError: If `estimator` is a ${tf.estimator.Estimator} instance
                and `default_output_alternative_key` was specified.
        """
        export_result = estimator.export_savedmodel(
            export_dir_base, serving_input_fn, assets_extra=assets_extra, as_text=as_text,
            checkpoint_path=checkpoint_path)

        garbage_collect_exports(export_dir_base, exports_to_keep)
        return export_result

    return export_strategy.ExportStrategy('Servo', export_fn)
