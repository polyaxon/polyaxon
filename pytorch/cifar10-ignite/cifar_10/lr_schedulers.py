import numpy as np

from torch.optim.lr_scheduler import _LRScheduler


class LRSchedulerWithRestart(_LRScheduler):
    """Proxy learning scheduler with restarts: learning rate follows input scheduler strategy but
    the strategy can restart when passed a defined number of epochs. Ideas are taken from SGDR paper.

    Args:
        scheduler (_LRScheduler): input lr scheduler
        restart_every (int): restart input lr scheduler every `restart_every` epoch.
        restart_factor (float): factor to rescale `restart_every` after each restart.
            For example, if `restart_factor=0.5` then next restart occurs in half of `restart_every` epochs.
        init_lr_factor (float): factor to rescale base lr after each restart.
            For example, if base lr of the input scheduler is 0.01 and `init_lr_factor=0.5`, then after the restart
            base lr of the input scheduler will be `0.01 * 0.5`.

    Learning rate strategy formula:
    ```
    t[-1] = 0 # Internal epoch timer dependant of global epoch value
    ...
    t[e] = t[e-1] + 1
    if t[e] % restart_every == 0:
        t[e] = 0
        restart_every *= restart_factor
        scheduler.base_lrs = scheduler.base_lrs * init_lr_factor
    scheduler.last_epoch = t[e]
    lr[e] = scheduler.get_lr()
    ```
    """

    def __init__(self, scheduler, restart_every, restart_factor=1.0, init_lr_factor=1.0, verbose=False):
        self.scheduler = scheduler
        self.restart_every = restart_every
        self.restart_factor = restart_factor
        self.init_lr_factor = init_lr_factor
        self._t = -1
        self.verbose = verbose
        # Do not call super method as optimizer is already setup by input scheduler
        # super(LRSchedulerWithRestart, self).__init__(optimizer, last_epoch)

    def get_lr(self):
        return self.scheduler.get_lr()

    def step(self, epoch=None):
        self._t += 1
        if self.restart_every > 0 and self.scheduler.last_epoch > 0 and \
                self._t % self.restart_every == 0:
            self._t = 0
            self.restart_every = int(self.restart_every * self.restart_factor)
            self.scheduler.base_lrs = [lr * self.init_lr_factor for lr in self.scheduler.base_lrs]
            if self.verbose:
                print("LRSchedulerWithRestart: restart lr at epoch %i, next restart at %i"
                      % (self.scheduler.last_epoch, self.scheduler.last_epoch + self.restart_every))

        self.scheduler.step(self._t)
