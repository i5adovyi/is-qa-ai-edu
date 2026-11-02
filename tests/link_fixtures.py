"""Create real directory redirections and file symlinks for confinement tests."""
import os
from unittest import SkipTest


def directory_link(link, target):
    if os.name == "nt":
        # CPython's native junction operation needs neither elevation nor Developer Mode.
        from _winapi import CreateJunction
        CreateJunction(str(target), str(link))
    else:
        link.symlink_to(target, target_is_directory=True)


def file_symlink(link, target):
    try:
        link.symlink_to(target)
    except OSError as error:
        if getattr(error, "winerror", None) == 1314:
            raise SkipTest("This Windows account cannot create file symlinks (WinError 1314).") from error
        raise
