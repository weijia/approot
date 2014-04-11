import os
import sys


def unbuffer_console():
    global unbuffered_out, unbuffered_err
    unbuffered_out = os.fdopen(os.dup(sys.stdout.fileno()), 'w', 0)
    sys.stdout = unbuffered_out
    unbuffered_err = os.fdopen(os.dup(sys.stderr.fileno()), 'w', 0)
    sys.stderr = unbuffered_err