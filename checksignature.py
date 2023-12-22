from collections import OrderedDict as odict
from inspect import _empty as NoTypeInfo
from inspect import _ParameterKind as ParameterKind
from inspect import signature
from string import Template
from typing import Callable
from typing import Optional
from typing import TypeVar


T = TypeVar('T')

class CheckSignature:

    def __init__(self, func: Optional[Callable[..., T]] = None):
        self.func = func

    def evaluate(self, *args, **kwargs):
        print('>>>', args)
        if not self.func:
            return None

        given_params = args
        given_kw_params = tuple(odict(kwargs).values())
        parameters = signature(self.func).parameters
        print(-1, given_kw_params)
        print(0, given_params)
        print(1, parameters)
        parameters_keys = tuple(parameters.keys())
        print('1+', parameters_keys)

        i = 0
        while i <= len(parameters_keys):
            key = parameters_keys[i]
        # for i, key in enumerate(parameters.keys()):
            #print(dir(parameters[key]))
            print(2, parameters[key])
            #print(type(parameters[key]))
            print(3, parameters[key]._name)
            print(4, parameters[key]._kind)
            print(5, parameters[key].kind)
            expected_type = parameters[key].annotation

            # TODO (withtwoemms) -- handle varargs
            try:
                if parameters[key].kind == ParameterKind.VAR_POSITIONAL:
                    for j in range(len(given_params)):
                    # for j, param in enumerate(given_params):
                        given_param = given_params[i + j]
                        print(6, given_param, i, j)
                        thing(given_param, key, expected_type)
                        # i += 1
                        # continue
                if parameters[key].kind == ParameterKind.VAR_KEYWORD:
                    # j = 0
                    for k, _ in enumerate(given_kw_params):
                        given_kw_param = given_kw_params[k]
                        print(7, given_kw_param)
                        thing(given_kw_param, key, expected_type)
                        # j += 1
                    break

                given_param = given_params[i]
                thing(given_param, key, expected_type)
                print('~>', expected_type, given_param, type(given_param))
            except IndexError:
                # return None
                pass
            
            print('$$$>', i)
            i += 1

    def __call__(self, *args, **kwargs):
        if self.func:
            self.evaluate(*args, **kwargs)
            return self.func(*args, **kwargs)

    def __repr__(self):
        if self.func:
            return f'<CheckSignature({self.func.__name__})>'
        else:
            return f'<CheckSignature()>'

    def __str__(self):
        if self.func:
            return self.func.__name__
        else:
            return ''


def checksignature(function: Callable = None):
    return CheckSignature(function)


def thing(given_param, key, expected_type):
    given_param_type = type(given_param)

    def raise_TypeError(expected_type_name: str):
        issue = Template(
            'Expected "$key" with value "$value" to be of type, "$expected_type". '
        )
        actuality = Template(
            'Received "$given_type" instead.'
        )
        raise TypeError(
            issue.substitute(
                key=key,
                value=given_param,
                expected_type=expected_type_name
            ) + actuality.substitute(
                given_type=type(given_param).__name__
            )
        )

    if expected_type != NoTypeInfo:
        if str(expected_type).startswith('typing.Union'):
            if given_param_type not in expected_type.__args__:
                raise_TypeError(f'{[et.__name__ for et in expected_type.__args__]}')
        else:
            if given_param_type != expected_type:
                raise_TypeError(expected_type.__name__)


