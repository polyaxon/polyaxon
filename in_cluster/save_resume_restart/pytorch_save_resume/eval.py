from __future__ import division
from __future__ import print_function


from torch.autograd import Variable


def eval_model(model, test_loader, cuda):
    model.eval()
    accuracy = 0
    # Get Batch
    for data, target in test_loader:
        data, target = Variable(data, volatile=True), Variable(target)
        if cuda:
            data, target = data.cuda(), target.cuda()
        # Evaluate
        output = model(data)
        # Load output on CPU
        if cuda:
            output.cpu()
        # Compute Accuracy
        prediction = output.data.max(1)[1]
        accuracy += prediction.eq(target.data).sum()
    return accuracy
