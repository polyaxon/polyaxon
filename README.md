# tensorflow-lstm-regression

This is an example of a regressor based on recurrent networks:

The objective is to predict continuous values, sin and cos functions in this example, based on previous observations using the LSTM architecture.

## Install and Run

### Create a Virtual Environment
It is reccomended that you create a virtualenv for the setup since this example is highly dependant on the versions set in the requirements file.

```
$ virtualenv ~/python/ltsm
$ source ~/python/ltsm/bin/activate
(ltsm) $
```

### Install Requirements
This example depends on **tensorflow-0.11.0** to work. You will first need to install the requirements. You will need the appropriate version of tensorflow for your platform, this example is for mac. For more details goto [TAG tensorflow-0.11.0 Setup](https://github.com/tensorflow/tensorflow/blob/v0.11.0/tensorflow/g3doc/get_started/os_setup.md)
```
(ltsm) $ pip install -U https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-0.11.0-py3-none-any.whl
(ltsm) $ pip install -r ./requirements.txt
```

### Running on Jupyter
Three Jupyter notebooks are provided as examples on how to use lstm for predicting shapes. They will be available when you start up Jupyter in the project dir.

```
(ltsm) $ jupyter notebook
```


## Other Reading
For more details please look at this blog post [Sequence prediction using recurrent neural networks(LSTM) with TensorFlow](http://mourafiq.com/2016/05/15/predicting-sequences-using-rnn-in-tensorflow.html)
