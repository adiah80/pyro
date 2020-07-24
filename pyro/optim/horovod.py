# Copyright Contributors to the Pyro project.
# SPDX-License-Identifier: Apache-2.0

import pyro

from .optim import PyroOptim


class HorovodOptimizer(PyroOptim):
    r"""
    Distributed wrapper for a :class:`~pyro.optim.optim.PyroOptim` optimizer.

    This class wraps a ``PyroOptim`` object similar to the way
    :func:`horovod.torch.DistributedOptimizer` wraps a
    :class:`torch.optim.Optimizer`.

    .. note::

        This requires :mod:`horovod.torch` is installed, e.g. via
        ``pip install pyro[horovod]``. For details see
        https://horovod.readthedocs.io/en/stable/install.html

    :param: A Pyro optimizer instance.
    :type pyro_optim: ~pyro.optim.optim.PyroOptim
    :param \*\*horovod_kwargs: Extra parameters passed to
        :func:`horovod.torch.DistributedOptimizer`.
    """
    def __init__(self, pyro_optim, **horovod_kwargs):
        param_store = pyro.get_param_store()

        def optim_constructor(params, **pt_kwargs):
            import horovod.torch as hvd
            pt_optim = pyro_optim.pt_optim_constructor(params, **pt_kwargs)
            named_parameters = [(param_store.param_name(p), p) for p in params]
            hvd_optim = hvd.DistributedOptimizer(
                pt_optim,
                named_parameters=named_parameters,
                **horovod_kwargs,
            )
            return hvd_optim

        super().__init__(optim_constructor, pyro_optim.pt_optim_args, pyro_optim.pt_clip_args)
