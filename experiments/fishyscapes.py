from sacred import Experiment
from sacred.utils import apply_backspaces_and_linefeeds
from .common import get_observer, experiment_context, clear_directory, load_data
import os
import sys
import logging
from zipfile import ZipFile
import tensorflow as tf
import bdlb

from .utils import ExperimentData
from fs.data.fsdata import FSData
from fs.data.utils import load_gdrive_file
from fs.data.augmentation import crop_multiple
from driving_uncertainty.test_fishy_torch import estimator

ex = Experiment()
ex.capture_out_filter = apply_backspaces_and_linefeeds
ex.observers.append(get_observer())

@ex.command
def saved_model(testing_dataset, model_id, _run, _log, batching=False, validation=False):
    fsdata = FSData(**testing_dataset)

    # Hacks because tf.data is shit and we need to translate the dict keys
    def data_generator():
        dataset = fsdata.validation_set if validation else fsdata.testset
        for item in dataset:
            data = fsdata._get_data(training_format=False, **item)
            out = {}
            for m in fsdata.modalities:
                blob = crop_multiple(data[m])
                if m == 'rgb':
                    m = 'image_left'
                if 'mask' not in fsdata.modalities and m == 'labels':
                    m = 'mask'
                out[m] = blob
            yield out

    data_types = {}
    for key, item in fsdata.get_data_description()[0].items():
        if key == 'rgb':
            key = 'image_left'
        if 'mask' not in fsdata.modalities and key == 'labels':
            key = 'mask'
        data_types[key] = item

    data = tf.data.Dataset.from_generator(data_generator, data_types)

    ZipFile(load_gdrive_file(model_id, 'zip')).extractall('/tmp/extracted_module')
    tf.compat.v1.enable_resource_variables()
    net = tf.saved_model.load('/tmp/extracted_module')

    def eval_func(image):
        if batching:
            image = tf.expand_dims(image, 0)
        out = estimator(image)
        return out

    fs = bdlb.load(benchmark="fishyscapes", download_and_prepare=False)
    _run.info['{}_anomaly'.format(model_id)] = fs.evaluate(eval_func, data)


if __name__ == '__main__':
    ex.run_commandline()
    os._exit(os.EX_OK)
