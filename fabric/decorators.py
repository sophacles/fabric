"""
Convenience decorators for use in fabfiles.
"""

from functools import wraps

from . import tasks

def task(func):
    """
    Decorator defining a function as a task.

    This is a convenience wrapper around `tasks.WrappedCallableTask`.
    """
    if not isinstance(func, tasks.Task):
        func = tasks.WrappedCallableTask(func)
    return func

def hosts(*host_list):
    """
    Decorator defining which host or hosts to execute the wrapped function on.

    For example, the following will ensure that, barring an override on the
    command line, ``my_func`` will be run on ``host1``, ``host2`` and
    ``host3``, and with specific users on ``host1`` and ``host3``::

        @hosts('user1@host1', 'host2', 'user2@host3')
        def my_func():
            pass

    Note that this decorator actually just sets the function's ``.hosts``
    attribute, which is then read prior to executing the function.
    """
    def attach_hosts(func):
        func.hosts = list(host_list)
        return func
    return attach_hosts


def roles(*role_list):
    """
    Decorator defining a list of role names, used to look up host lists.

    A role is simply defined as a key in `env` whose value is a list of one or
    more host connection strings. For example, the following will ensure that,
    barring an override on the command line, ``my_func`` will be executed
    against the hosts listed in the ``webserver`` and ``dbserver`` roles::

        env.roledefs.update({
            'webserver': ['www1', 'www2'],
            'dbserver': ['db1']
        })

        @roles('webserver', 'dbserver')
        def my_func():
            pass

    Note that this decorator actually just sets the function's ``.roles``
    attribute, which is then read prior to executing the function.
    """
    def attach_roles(func):
        func.roles = list(role_list)
        return func
    return attach_roles


def runs_once(func):
    """
    Decorator preventing wrapped function from running more than once.

    By keeping internal state, this decorator allows you to mark a function
    such that it will only run once per Python interpreter session, which in
    typical use means "once per invocation of the ``fab`` program".

    Any function wrapped with this decorator will silently fail to execute the
    2nd, 3rd, ..., Nth time it is called, and will return None in that instance.
    """
    g = func.run # avoid some issues w/ name overriding
    @wraps(g)
    def decorated(*args, **kwargs):
        if hasattr(func, 'has_run'):
            return
        else:
            func.has_run = True
            return g(*args, **kwargs)
    func.run = decorated
    return func


