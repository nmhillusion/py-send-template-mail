import os
import subprocess


def os_open_file(filename):
    """Open document with default application in Python."""
    try:
        os.startfile(filename)
    except AttributeError:
        subprocess.call(['open', filename])
