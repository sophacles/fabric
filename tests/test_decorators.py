from nose.tools import ok_

from fabric import decorators, tasks

def test_task_is_an_instance_of_task_object():
    ok_(isinstance(decorators.task, tasks.Task))

