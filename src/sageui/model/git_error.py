

class GitError(Exception):
    pass

class DetachedHeadError(GitError):
    pass

class UserEmailException(GitError):
    pass
