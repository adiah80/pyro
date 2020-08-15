# Copyright Contributors to the Pyro project.
# SPDX-License-Identifier: Apache-2.0

import pyroapi

from pyro.contrib.funsor.handlers import condition, do, markov  # noqa: F401
from pyro.contrib.funsor.handlers import plate as _plate
from pyro.contrib.funsor.handlers.primitives import to_data, to_funsor  # noqa: F401
from pyro.primitives import (clear_param_store, deterministic, factor, get_param_store, module, param,  # noqa: F401
                             plate, random_module, sample, subsample)


def plate(*args, **kwargs):
    return _plate(None, *args, **kwargs)


pyroapi.register_backend('contrib.funsor', {
    'distributions': 'pyro.distributions',
    'handlers': 'pyro.contrib.funsor.handlers',
    'infer': 'pyro.contrib.funsor.infer',
    'ops': 'torch',
    'optim': 'pyro.optim',
    'pyro': 'pyro.contrib.funsor',
})
