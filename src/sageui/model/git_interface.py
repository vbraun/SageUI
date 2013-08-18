r"""
Git Interface

This module provides a python interface to git. Essentially, it is
a raw wrapper around calls to git and retuns the output as strings.

EXAMPLES::

    sage: globals()

    sage: git._check_user_email()
    DEBUG cmd: git config user.name
    DEBUG cmd: git config user.email

    sage: git.execute('status', porcelain=True)
    DEBUG cmd: git status --porcelain
    DEBUG stdout: ?? untracked
    '?? untracked\n'

    sage: git.status(porcelain=True)
    DEBUG cmd: git status --porcelain
    DEBUG stdout: ?? untracked
    '?? untracked\n'

    sage: git.untracked_files()
    DEBUG cmd: git ls-files --exclude-standard --other
    DEBUG stdout: untracked
    ['untracked']
"""

##############################################################################
#  SageUI: A graphical user interface to Sage, Trac, and Git.
#  Copyright (C) 2013  Volker Braun <vbraun.name@gmail.com>
#                      David Roe <roed.math@gmail.com>
#                      Julian Rueth <julian.rueth@fsfe.org>
#                      Keshav Kini <keshav.kini@gmail.com>
#                      Nicolas M. Thiery <Nicolas.Thiery@u-psud.fr>
#                      Robert Bradshaw <robertwb@gmail.com>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
##############################################################################


import os
import subprocess

from sageui.misc.cached_property import cached_property

from .git_error import GitError, DetachedHeadException, UserEmailException




class GitInterfaceSilentProxy(object):
    """
    Execute a git command silently, discarding the output.
    """
    def __init__(self, actual_interface):
        self._interface = actual_interface

    def execute(self, *args, **kwds):
        self._interface.execute(*args, **kwds)
        return None  # the "silent" part


class GitInterfaceExitCodeProxy(object):
    """
    Execute a git command silently, return only the exit code.
    """
    def __init__(self, actual_interface):
        self._interface = actual_interface

    def execute(self, cmd, *args, **kwds):
        result = self._interface._run(cmd, args, kwds, 
                                      popen_stdout=subprocess.PIPE, 
                                      popen_stderr=subprocess.PIPE,
                                      exit_code_to_exception=False)
        return result['exit_code']


class GitInterfacePrintProxy(object):
    """
    Execute a git command and print to stdout like the commandline client.
    """
    def __init__(self, actual_interface):
        self._interface = actual_interface

    def execute(self, cmd, *args, **kwds):
        result = self._interface._run(cmd, args, kwds, 
                                      popen_stdout=subprocess.PIPE, 
                                      popen_stderr=subprocess.PIPE)
        print(result['stdout'])
        if result['stderr']:
            WARNING = '\033[93m'
            RESET = '\033[0m'
            print(WARNING+result['stderr']+RESET)
        return None




class GitInterface(object):
    r"""
    A wrapper around the ``git`` command line tool.

    Most methods of this class correspond to actual git commands. Some add
    functionality which is not directly available in git. However, all of the
    methods should be non-interactive. If interaction is required the method
    should live in :class:`saged.dev.sagedev.SageDev`.

    EXAMPLES::

        >>> git   # doctest: +ELLIPSIS
        Interface to git repo at /.../git_repo
    """

    def __init__(self, repository_path, verbose=False, git_dir=None, git_cmd=None):
        self._verbose = verbose
        if not os.path.exists(repository_path):
            raise ValueError('{} does not point to an existing directory.'.format(repository_path))
        self._work_tree = os.path.abspath(repository_path)
        self._git_dir = os.path.join(self._work_tree, '.git') if git_dir is None else git_dir
        self._git_cmd = 'git' if git_cmd is None else git_cmd
        self._user_email_set = False
        self.silent = GitInterfaceSilentProxy(self)
        self.exit_code = GitInterfaceExitCodeProxy(self)
        self.echo = GitInterfacePrintProxy(self)

    @property
    def git_cmd(self):
        """
        The git executable
        
        EXAMPLES::

            >>> git.git_cmd
            'git'
        """
        return self._git_cmd

    @property
    def git_dir(self):
        """
        The git private directory. Usually ``.git``
        
        OUTPUT:

        Absolute path as a string.

        EXAMPLES::

            >>> git.git_dir  # doctest: +ELLIPSIS
            '/.../git_repo/.git'
        """
        return self._git_dir

    @property
    def work_tree(self):
        """
        The git work tree

        OUTPUT:

        Absolute path as a string.

        EXAMPLES::

            >>> git.work_tree # doctest: +ELLIPSIS
            '/.../git_repo'
        """
        return self._work_tree

    def __repr__(self):
        r"""
        Return a printable representation of this object.
        
        TESTS::

            >>> repr(git)   # doctest: +ELLIPSIS
            'Interface to git repo at /.../git_repo'
        """
        return 'Interface to git repo at '+self.work_tree

    def get_state(self):
        r"""
        Get the current state of merge/rebase/am/etc operations.

        OUTPUT:

        A tuple of strings which consists of any of the following:
        ``'rebase'``, ``'am'``, ``'rebase-i'``, ``'rebase-m'``, ``'merge'``,
        ``'bisect'``, ``'cherry-seq'``, ``'cherry'``.

        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::

            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create two conflicting branches::

            sage: os.chdir(config['git']['src'])
            sage: with open("file","w") as f: f.write("version 0")
            sage: git.add("file")
            sage: git.commit(SUPER_SILENT, "-m","initial commit")
            sage: git.checkout(SUPER_SILENT, "-b","branch1")
            sage: with open("file","w") as f: f.write("version 1")
            sage: git.commit(SUPER_SILENT, "-am","second commit")
            sage: git.checkout(SUPER_SILENT, "master")
            sage: git.checkout(SUPER_SILENT, "-b","branch2")
            sage: with open("file","w") as f: f.write("version 2")
            sage: git.commit(SUPER_SILENT, "-am","conflicting commit")

        A ``merge`` state::

            sage: git.checkout(SUPER_SILENT, "branch1")
            sage: git.merge(SUPER_SILENT, 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1)
            sage: git.get_state()
            ('merge',)
            sage: git.merge(SUPER_SILENT,abort=True)
            sage: git.get_state()
            ()

        A ``rebase`` state::

            sage: git.execute_supersilent('rebase', 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1)
            sage: git.get_state()
            ('rebase',)
            sage: git.rebase(SUPER_SILENT, abort=True)
            sage: git.get_state()
            ()

        A merge within an interactive rebase::

            sage: git.rebase(SUPER_SILENT, 'HEAD^', interactive=True, env={'GIT_SEQUENCE_EDITOR':'sed -i s+pick+edit+'})
            sage: git.get_state()
            ('rebase-i',)
            sage: git.merge(SUPER_SILENT, 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1)
            sage: git.get_state()
            ('merge', 'rebase-i')
            sage: git.rebase(SUPER_SILENT, abort=True)
            sage: git.get_state()
            ()
        """
        # logic based on zsh's git backend for vcs_info
        opj = os.path.join
        p = lambda x: opj(self._dot_git, x)
        ret = []
        for d in map(p,("rebase-apply", "rebase", opj("..",".dotest"))):
            if os.path.isdir(d):
                if os.path.isfile(opj(d, 'rebasing')) and 'rebase' not in ret:
                    ret.append('rebase')
                if os.path.isfile(opj(d, 'applying')) and 'am' not in ret:
                    ret.append('am')
        for f in map(p, (opj('rebase-merge', 'interactive'),
                         opj('.dotest-merge', 'interactive'))):
            if os.path.isfile(f):
                ret.append('rebase-i')
                break
        else:
            for d in map(p, ('rebase-merge', '.dotest-merge')):
                if os.path.isdir(d):
                    ret.append('rebase-m')
                    break
        if os.path.isfile(p('MERGE_HEAD')):
            ret.append('merge')
        if os.path.isfile(p('BISECT_LOG')):
            ret.append('bisect')
        if os.path.isfile(p('CHERRY_PICK_HEAD')):
            if os.path.isdir(p('sequencer')):
                ret.append('cherry-seq')
            else:
                ret.append('cherry')
        # return in reverse order so reset operations are correctly ordered
        return tuple(reversed(ret))

    def reset_state(self):
        r"""
        Get out of a merge/am/rebase/etc state.

        EXAMPLES:

        Create a :class:`GitInterface` for doctesting::

            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: git = GitInterface(config["git"], DoctestUserInterface(config["UI"]))

        Create two conflicting branches::

            sage: os.chdir(config['git']['src'])
            sage: with open("file","w") as f: f.write("version 0")
            sage: git.add("file")
            sage: git.commit(SUPER_SILENT, "-m","initial commit")
            sage: git.checkout(SUPER_SILENT, "-b","branch1")
            sage: with open("file","w") as f: f.write("version 1")
            sage: git.commit(SUPER_SILENT, "-am","second commit")
            sage: git.checkout(SUPER_SILENT, "master")
            sage: git.checkout(SUPER_SILENT, "-b","branch2")
            sage: with open("file","w") as f: f.write("version 2")
            sage: git.commit(SUPER_SILENT, "-am","conflicting commit")

        A merge within an interactive rebase::

            sage: git.checkout(SUPER_SILENT, "branch1")
            sage: git.rebase(SUPER_SILENT, 'HEAD^', interactive=True, env={'GIT_SEQUENCE_EDITOR':'sed -i s+pick+edit+'})
            sage: git.get_state()
            ('rebase-i',)
            sage: git.merge(SUPER_SILENT, 'branch2')
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (1)
            sage: git.get_state()
            ('merge', 'rebase-i')

        Get out of this state::

            sage: git.reset_to_clean_state()
            sage: git.get_state()
            ()
        """
        for state in self.get_state():
            if state.startswith('rebase'):
                self.rebase(abort=True)
            elif state == 'am':
                self.am(abort=True)
            elif state == 'merge':
                self.merge(abort=True)
            elif state == 'bisect':
                raise NotImplementedError(state)
            elif state.startswith('cherry'):
                self.cherry_pick(abort=True)
            else:
                raise ValueError("'%s' is not a valid state"%state)

    def _log(self, prefix, log):
        if self._verbose:
            for line in log.splitlines():
                print('DEBUG '+prefix+': '+line)

    def _run_unsafe(self, cmd, args, kwds={}, popen_stdout=None, popen_stderr=None):
        r"""
        Run git

        INPUT:

        - ``cmd`` -- git command run

        - ``args`` -- extra arguments for git

        - ``kwds`` -- extra keywords for git

        - ``popen_stdout`` -- Popen-like keywords.

        - ``popen_stderr`` -- Popen-like keywords.
        
        OUTPUT:

        A dictionary with keys ``exit_code``, ``stdout``, ``stderr``, ``cmd``.

        .. WARNING::

            This method does not raise an exception if the git call returns a
            non-zero exit code.

        EXAMPLES::

            sage: git._run_git('status', (), {})
            # On branch master
            #
            # Initial commit
            #
            nothing to commit (create/copy files and use "git add" to track)
            (0, None, None, 'git status')
            sage: git._run_git('status', (), {}, stdout=False)
            (0, None, None, 'git status')
        """ 
        s = [self.git_cmd, cmd]
        for k, v in kwds.items():
            if len(k) == 1:
                k = '-' + k
            else:
                k = '--' + k.replace('_', '-')
            if v is True:
                s.append(k)
            elif v is not False:
                s.append(k+'='+str(v))
        if args:
            s.extend(a for a in args if a is not None)
        s = [str(arg) for arg in s]
        complete_cmd = ' '.join(s)
        self._log('cmd', complete_cmd)

        env = dict(os.environ)
        env['GIT_DIR'] = self.git_dir
        env['GIT_WORK_TREE'] = self.work_tree
        if cmd == 'stash':
            # bug
            try:
                cwd = os.getcwd()
                os.chdir(self.work_tree)
                process = subprocess.Popen(s, stdout=popen_stdout, stderr=popen_stderr, env=env)
            finally:
                os.chdir(cwd)
        else:
            process = subprocess.Popen(s, stdout=popen_stdout, stderr=popen_stderr, env=env)
        stdout, stderr = process.communicate()
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        retcode = process.poll()
        if stdout is not None and popen_stdout is subprocess.PIPE:
            self._log('stdout', stdout)
        if stderr is not None and popen_stderr is subprocess.PIPE:
            self._log('stderr', stderr)
        return {'exit_code':retcode, 'stdout':stdout, 'stderr':stderr, 'cmd':complete_cmd}

    # commands that cannot change the working tree even with
    # some crazy flags set - these commands should be safe
    _safe_commands = [
        'config', 'diff', 'grep', 'log', 'ls_remote', 'remote', 'reset', 'show', 
        'show_ref', 'status', 'symbolic_ref' ]
        
    def _run(self, cmd, args, kwds={}, popen_stdout=None, popen_stderr=None, exit_code_to_exception=True):
        if cmd not in self._safe_commands:
            self._check_user_email()
        result = self._run_unsafe(cmd, args, kwds,
                                  popen_stdout=popen_stdout,
                                  popen_stderr=popen_stderr)
        if exit_code_to_exception and result['exit_code']:
            raise GitError(result)
        return result

    def execute(self, cmd, *args, **kwds):
        r"""
        Run git on a command given by a string.

        Raises an exception if git has non-zero exit code.

        INPUT:

        - ``cmd`` -- string. The git command to run

        - ``*args`` -- list of strings. Extra arguments for git.

        - ``**kwds`` -- keyword arguments. Extra keywords for git. Will be rewritten 
          such that ``foo='bar'`` becomes the git commandline argument ``--foo='bar'``. 
          As a special case, ``foo=True`` becomes just ``--foo``.

        EXAMPLES::

            sage: git.execute('status')
            # On branch master
            #
            # Initial commit
            #
            nothing to commit (create/copy files and use "git add" to track)
            sage: git.execute('status', foo=True) # --foo is not a valid parameter
            Traceback (most recent call last):
            ...
            GitError: git returned with non-zero exit code (129)
        """
        result = self._run(cmd, args, kwds,
                           popen_stdout=subprocess.PIPE,
                           popen_stderr=subprocess.PIPE)
        return result['stdout']

    __call__ = execute

    def _check_user_email(self):
        r"""
        Make sure that a real name and an email are set for git. These will
        show up next to any commit that user creates.

        TESTS::

            sage: import os
            sage: from sage.dev.git_interface import GitInterface, SILENT, SUPER_SILENT
            sage: from sage.dev.test.config import DoctestConfig
            sage: from sage.dev.test.user_interface import DoctestUserInterface
            sage: config = DoctestConfig()
            sage: del config['git']['user.name']
            sage: del config['git']['user.email']
            sage: UI = DoctestUserInterface(config["UI"])
            sage: git = GitInterface(config["git"], UI)
            sage: os.chdir(config['git']['src'])
            sage: UI.append("Doc Test")
            sage: UI.append("doc@test")
            sage: git._check_user_email()
        """
        if self._user_email_set:
            return
        name = self._run_unsafe('config', ['user.name'], popen_stdout=open('/dev/null', 'wb'))
        email = self._run_unsafe('config', ['user.email'], popen_stdout=open('/dev/null', 'wb'))
        if (name['exit_code'] == 0) and (email['exit_code'] == 0):
            self._user_email_set = True
        else:
            raise UserEmailException()




git_commands = (
    "add",
    "am",
    "apply",
    "bisect",
    "branch",
    "config",
    "checkout",
    "cherry_pick",
    "clean",
    "clone",
    "commit",
    "diff",
    "fetch",
    "for_each_ref",
    "format_patch",
    "grep",
    "init",
    "log",
    "ls_files",
    "ls_remote",
    "merge",
    "mv",
    "pull",
    "push",
    "rebase",
    "remote",
    "reset",
    "rev_list",
    "rm",
    "show",
    "show_ref",
    "stash",
    "status",
    "symbolic_ref",
    "tag"
)

def create_wrapper(git_cmd_underscore):
    r"""
    Create a wrapper for ``git_cmd_underscore``.
    """
    git_cmd = git_cmd_underscore.replace('_', '-')
    def meth(self, *args, **kwds):
        return self.execute(git_cmd, *args, **kwds)
    meth.__doc__ = r"""
    Call `git {0}`.

    OUTPUT:

    See :meth:`execute` for more information.

    EXAMPLES:

        sage: git.{1}() # not tested
    """.format(git_cmd, git_cmd_underscore)
    return meth



for command in git_commands:
    setattr(GitInterface, command, create_wrapper(command))
    setattr(GitInterfaceSilentProxy, command, create_wrapper(command))
    setattr(GitInterfaceExitCodeProxy, command, create_wrapper(command))
    setattr(GitInterfacePrintProxy, command, create_wrapper(command))
