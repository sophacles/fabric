from nose.tools import eq_, ok_
import random
import unittest

from fabric import decorators, tasks

def test_task_returns_an_instance_of_wrappedfunctask_object():
    def foo():
        pass
    task = decorators.task(foo)
    ok_(isinstance(task, tasks.WrappedCallableTask))

class TestOfRunsOnceDecorator(unittest.TestCase):
    def test_runs_only_once(self):
        def foo():
            task.counter += 1
        task = decorators.runs_once(foo)
        task.counter = 0

        for i in range(2):
            task()
            eq_(1, task.counter, "invocation counter should not advance past 1, run: %d; got: %d" % (i, task.counter))

    def test_returns_same_value_each_run(self):
        rand = random.randint(100, 200)
        def foo():
            return rand

        eq_(rand, foo(), "smoke test")

        task = decorators.runs_once(foo)
        for i in range(10):
            eq_(rand, task(), "comparing task return, run: %d" % i)

