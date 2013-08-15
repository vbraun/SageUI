

class GitError(RuntimeError):
    r"""
    Error raised when git exits with a non-zero exit code.

    EXAMPLES::

        sage: from sageui.model.git_error import GitError
        sage: raise GitError({'exit_code':128, 'stdout':'', 'stderr':'', 'cmd':'command'})
        Traceback (most recent call last):
        ...
        GitError: git returned with non-zero exit code (128) when executing "command"
            STDOUT: 
            STDERR: 
    """
    def __init__(self, result, explain=None, advice=None):
        r"""
        Initialization.

        TESTS::

            sage: from sageui.model.git_error import GitError
            sage: type(GitError({'exit_code':128, 'stdout':'', 'stderr':'', 'cmd':'command'}))
            <class 'sageui.model.git_error.GitError'>
        """
        self.exit_code = result['exit_code']
        self.cmd = result['cmd']
        self.stdout = result['stdout']
        self.stderr = result['stderr']
        self.explain = explain
        self.advice = advice
        template = 'git returned with non-zero exit code ({}) when executing "{}"\n    STDOUT: {}\n    STDERR: {}'
        RuntimeError.__init__(self, template.format(self.exit_code, self.cmd, self.stdout, self.stderr))


class DetachedHeadException(RuntimeError):
    r"""
    Error raised when a git command can not be executed because the repository
    is in a detached HEAD state.

    EXAMPLES::

        sage: from sageui.model.git_error import DetachedHeadException
        sage: raise DetachedHeadException()
        Traceback (most recent call last):
        ...
        DetachedHeadException: unexpectedly, git is in a detached HEAD state

    """
    def __init__(self):
        r"""
        Initialization.

        TESTS::

            sage: from sageui.model.git_error import DetachedHeadException
            sage: type(DetachedHeadException())
            <class 'sageui.model.git_error.DetachedHeadException'>
        """
        RuntimeError.__init__(self, "unexpectedly, git is in a detached HEAD state")


class InvalidStateError(RuntimeError):
    r"""
    Error raised when a git command can not be executed because the repository
    is not in a clean state.

    EXAMPLES::

        sage: from sageui.model.git_error import InvalidStateError
        sage: raise InvalidStateError()
        Traceback (most recent call last):
        ...
        InvalidStateError: unexpectedly, git is in an unclean state

    """
    def __init__(self):
        r"""
        Initialization.

        TESTS::

            sage: from sageui.model.git_error import InvalidStateError
            sage: type(InvalidStateError())
            <class 'sageui.model.git_error.InvalidStateError'>
        """
        RuntimeError.__init__(self, "unexpectedly, git is in an unclean state")


class UserEmailException(RuntimeError):
    r"""
    Error raised if user/email is not set.

    This means that it is not advisable to make commits to the repository.

    EXAMPLES::

        sage: from sageui.model.git_error import UserEmailException
        sage: raise UserEmailException()
        Traceback (most recent call last):
        ...
        UserEmailException: user/email is not configured, cannot make commits
    """
    def __init__(self):
        r"""
        Initialization.

        TESTS::

            sage: from sageui.model.git_error import UserEmailException
            sage: type(UserEmailException())
            <class 'sageui.model.git_error.UserEmailException'>
        """
        RuntimeError.__init__(self, "user/email is not configured, cannot make commits")

