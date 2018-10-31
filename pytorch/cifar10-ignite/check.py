import torch

print("torch version: {}".format(torch.__version__))
print("torch cuda version: {}".format(torch.version.cuda))
print("torch cuda available: {}".format(torch.cuda.is_available()))

x = torch.rand(4, 512, 512, 3).to('cuda')
print(torch.sum(x))
