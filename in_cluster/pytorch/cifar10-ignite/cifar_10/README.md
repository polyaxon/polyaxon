# CIFAR10 Playground

Train and evaluate models with [ignite](https://github.com/pytorch/ignite)

## Requirements

Install PyTorch from http://pytorch.org/ and some dependencies:

```bash
pip install --upgrade git+https://github.com/pytorch/vision.git
pip install --upgrade git+https://github.com/pytorch/ignite.git
pip install --upgrade git+https://github.com/lanpa/tensorboard-pytorch.git
pip install --upgrade numpy scikit-learn
```

if you want to use NASNet-A Mobile, consider to install
```bash
pip install --upgrade git+https://github.com/Cadene/pretrained-models.pytorch.git
```  

## Training

Start training with a simple command:
```bash
python cifar10_train_playground.py --output=cifar10_output
# or more complicated command
python cifar10_train_playground.py --output=cifar10_output --debug --model=vgg16_bn --lr=0.0005234 --gamma=0.98 --restart_every=20 --imgaugs=imgaugs_YCbCr.py
```
for more options:
```bash
ptyhon cifar10_train_playground.py --help
```

The output folder will contain folders of with training runs:
- `training_YYYYmmDD_HHMM`
    - `train.log` : training log
    - 5 best models, `model_*.pth`
    - tensorboard logs

### TensorboardX training monitoring

```bash
tensorboard --logdir=cifar10_output
``` 

| ![tb_scalars](imgs/tb_scalars.png) | ![tb_scalars](imgs/tb_text.png) |
| --- | --- | 



## Evaluation

Produce classification report (precision, recall, f1-score) like this
```bash
             precision    recall  f1-score   support

          0       0.84      0.86      0.85      1000
          1       0.93      0.92      0.93      1000
          2       0.78      0.73      0.75      1000
          3       0.67      0.69      0.68      1000
          4       0.78      0.82      0.80      1000
          5       0.78      0.75      0.77      1000
          6       0.85      0.88      0.87      1000
          7       0.87      0.84      0.86      1000
          8       0.91      0.89      0.90      1000
          9       0.89      0.91      0.90      1000

avg / total       0.83      0.83      0.83     10000
```
Run evaluation with 10 test time augmentations of a trained model:
```bash
python cifar10_eval_playground.py cifar10_output/raining_20180405_1259/model_SqueezeNetV11BN_48_val_loss\=0.6439508.pth --output=cifar10_output --n_tta=10
```


 