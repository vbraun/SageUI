"""
Diffs for Files in the Git Working Tree

"""


class GitFileABC(object):
    def __init__(self, filename):
        self._filename = filename

    @property
    def name(self):
        """
        The file name and path relative to the repository root
        """
        return self._filename
