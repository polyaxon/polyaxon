import time

from torch.autograd import Variable


def train_model(model,
                optimizer,
                train_loader,
                train_dataset,
                loss_fn,
                num_epochs,
                epoch,
                batch_size,
                notify,
                cuda):
    average_time = 0
    model.train()
    for i, (images, labels) in enumerate(train_loader):
        # measure data loading time
        batch_time = time.time()
        images = Variable(images)
        labels = Variable(labels)

        if cuda:
            images, labels = images.cuda(), labels.cuda()

        # Forward + Backward + Optimize
        optimizer.zero_grad()
        outputs = model(images)
        loss = loss_fn(outputs, labels)

        if cuda:
            loss.cpu()

        loss.backward()
        optimizer.step()

        # Measure elapsed time
        batch_time = time.time() - batch_time
        average_time += batch_time

        prediction = outputs.data.max(1)[1]  # first column has actual prob.
        accuracy = prediction.eq(labels.data).sum() / batch_size * 100

        if (i + 1) % notify == 0:
            print(
                'Epoch: [%d/%d], Step: [%d/%d], Loss: %.4f, Accuracy: %.4f, Batch time: %f' % (
                    epoch + 1,
                    num_epochs,
                    i + 1,
                    len(train_dataset) // batch_size,
                    loss.data[0],
                    accuracy,
                    average_time / notify))
