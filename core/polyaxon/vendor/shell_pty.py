# This code is based on logic from
# http://sqizit.bartletts.id.au/2011/02/14/pseudo-terminals-in-python/
# Licensed under the MIT license:
# Copyright (c) 2011 Joshua D. Bartlett
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import errno
import fcntl
import json
import os
import pty
import select
import signal
import struct
import termios
import tty

from polyaxon.client.transport import ws_client


class PseudoTerminal:
    """Wraps the pseudo-TTY (PTY) allocated to a container.

    The PTY is managed via the current process' TTY until it is closed.
    """

    START_ALTERNATE_MODE = set("\x1b[?{0}h".format(i) for i in ("1049", "47", "1047"))
    END_ALTERNATE_MODE = set("\x1b[?{0}l".format(i) for i in ("1049", "47", "1047"))
    ALTERNATE_MODE_FLAGS = tuple(START_ALTERNATE_MODE) + tuple(END_ALTERNATE_MODE)

    def __init__(self, client_shell=None):
        self.client_shell = client_shell
        self.master_fd = None

    def start(self, argv=None):
        """
        Create a spawned process.
        Based on the code for pty.spawn().
        """
        if not argv:
            argv = [os.environ["SHELL"]]

        pid, master_fd = pty.fork()
        self.master_fd = master_fd
        if pid == pty.CHILD:
            os.execlp(argv[0], *argv)

        old_handler = signal.signal(signal.SIGWINCH, self._signal_winch)
        try:
            mode = tty.tcgetattr(pty.STDIN_FILENO)
            tty.setraw(pty.STDIN_FILENO)
            restore = 1
        except tty.error:  # This is the same as termios.error
            restore = 0
        self._init_fd()
        try:
            self._loop()
        except (IOError, OSError):
            if restore:
                tty.tcsetattr(pty.STDIN_FILENO, tty.TCSAFLUSH, mode)

        self.client_shell.close()
        self.client_shell = None
        if self.master_fd:
            os.close(self.master_fd)
            self.master_fd = None
        signal.signal(signal.SIGWINCH, old_handler)

    def _init_fd(self):
        """
        Called once when the pty is first set up.
        """
        self._set_pty_size()

    def _signal_winch(self, signum, frame):
        """
        Signal handler for SIGWINCH - window size has changed.
        """
        self._set_pty_size()

    def _set_pty_size(self):
        """
        Sets the window size of the child pty based on the window size of
        our own controlling terminal.
        """
        packed = fcntl.ioctl(
            pty.STDOUT_FILENO, termios.TIOCGWINSZ, struct.pack("HHHH", 0, 0, 0, 0)
        )
        rows, cols, h_pixels, v_pixels = struct.unpack("HHHH", packed)
        self.client_shell.write_channel(
            ws_client.RESIZE_CHANNEL, json.dumps({"Height": rows, "Width": cols})
        )

    def _loop(self):
        """
        Main select loop. Passes all data to self.master_read() or self.stdin_read().
        """
        assert self.client_shell is not None
        client_shell = self.client_shell
        while 1:
            try:
                rfds, wfds, xfds = select.select(
                    [pty.STDIN_FILENO, client_shell.sock.sock], [], []
                )
            except select.error as e:
                no = e.errno
                if no == errno.EINTR:
                    continue
            if pty.STDIN_FILENO in rfds:
                data = os.read(pty.STDIN_FILENO, 1024)
                self.stdin_read(data)
            if client_shell.sock.sock in rfds:
                # read from client_shell
                if client_shell.peek_stdout():
                    self.master_read(client_shell.read_stdout())
                if client_shell.peek_stderr():
                    self.master_read(client_shell.read_stderr())
                # error occurs
                if client_shell.peek_channel(ws_client.ERROR_CHANNEL):
                    break

    def write_stdout(self, data):
        """
        Writes to stdout as if the child process had written the data.
        """
        os.write(pty.STDOUT_FILENO, data.encode())

    def write_master(self, data):
        """
        Writes to the child process from its controlling terminal.
        """
        assert self.client_shell is not None
        self.client_shell.write_stdin(data)

    def master_read(self, data):
        """
        Called when there is data to be sent from the child process back to the user.
        """
        flag = self.findlast(data, self.ALTERNATE_MODE_FLAGS)
        if flag is not None:
            if flag in self.START_ALTERNATE_MODE:
                # This code is executed when the child process switches the
                #       terminal into alternate mode. The line below
                #       assumes that the user has opened vim, and writes a
                #       message.
                self.write_master("IEntering special mode.\x1b")
            elif flag in self.END_ALTERNATE_MODE:
                # This code is executed when the child process switches the
                #       terminal back out of alternate mode. The line below
                #       assumes that the user has returned to the command
                #       prompt.
                self.write_master('echo "Leaving special mode."\r')
        self.write_stdout(data)

    def stdin_read(self, data):
        """
        Called when there is data to be sent from the user/controlling
        terminal down to the child process.
        """
        self.write_master(data)

    @staticmethod
    def findlast(s, substrs):
        """
        Finds whichever of the given substrings occurs last in the given string
        and returns that substring, or returns None if no such strings occur.
        """
        i = -1
        result = None
        for substr in substrs:
            pos = s.rfind(substr)
            if pos > i:
                i = pos
                result = substr
        return result
