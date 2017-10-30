from __future__ import absolute_import
from argparse import ArgumentParser
from collections import deque


def to_run(func, wrapper):
    func = get_parent(func)
    if not hasattr(func, '_run'):
        func._run = deque()

    func._run.appendleft(wrapper)


def do_run(func):
    if hasattr(func, '_run'):
        for wrapper_func in func._run:
            wrapper_func()

        delattr(func, '_run')


def get_parent(func):
    while hasattr(func, 'parent'):
        func = func.parent

    return func


def get_func(func):
    while hasattr(func, 'func'):
        func = func.func

    return func


def entrypoint(*args, **kwds):
    def wrapper(func):
        def run(*args, **kwds):
            do_run(func)
            for action in func.actions.keys():
                do_run(func.actions[action])

            func.args = func.parser.parse_args()
            run.args = func.args
            for action in func.actions.keys():
                func.actions[action].args = func.args

            func(*args, **kwds)
            if hasattr(func.args, 'action') and func.args.action in func.actions:
                func.actions[func.args.action]()

        func = get_func(func)
        func.parser = ArgumentParser(*args, **kwds)
        func.wrapper = run
        if not hasattr(func, 'actions'):
            func.actions = {}

        run.func = func
        return run

    return wrapper


def defaults(*args, **kwds):
    def wrapper(func):
        func = get_func(func)
        to_run(func, lambda: func.parser.set_defaults(*args, **kwds))
        return func

    return wrapper


def option(*args, **kwds):
    def wrapper(func):
        func = get_func(func)
        to_run(func, lambda: func.parser.add_argument(*args, **kwds))
        return func

    return wrapper


def action(parent, name, *args, **kwds):
    def wrapper(func):
        def action_wrapper():
            if not hasattr(parent, 'subparser'):
                parent.subparser = parent.parser.add_subparsers()

            func.parser = parent.subparser.add_parser(name, *args, **kwds)
            if not hasattr(func, 'actions'):
                func.actions = {}

            func.parser.set_defaults(action=name)

        func = get_func(func)
        func.wrapper = action_wrapper
        func.parent = parent
        if not hasattr(parent, 'actions'):
            parent.actions = {}

        parent.actions[name] = func
        to_run(func, action_wrapper)
        return func

    parent = get_func(parent)
    return wrapper
