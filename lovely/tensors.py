# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_tensors.ipynb.

# %% auto 0
__all__ = ['tensor_str', 'lovely', 'monkey_patch']

# %% ../nbs/00_tensors.ipynb 2
from typing import Optional

import torch
from click import style
from nbdev.showdoc import *
from fastcore.test import test_eq

# import wandb

# %% ../nbs/00_tensors.ipynb 3
class __PrinterOptions(object):
    precision: int = 3
    threshold_max: int = 3 # .abs() larger than 1e3 -> Sci mode
    threshold_min: int = -4 # .abs() smaller that 1e-4 -> Sci mode
    sci_mode: Optional[bool] = None # None = auto. Otherwise, force sci mode.
    color: bool = True # Now in color

PRINT_OPTS = __PrinterOptions()

# %% ../nbs/00_tensors.ipynb 4
# Do we want this float in decimal or scientific mode?
def sci_mode(f: float):
    return (abs(f) < 10**(PRINT_OPTS.threshold_min) or
            abs(f) > 10**PRINT_OPTS.threshold_max)

# %% ../nbs/00_tensors.ipynb 8
# Convert a tensor into a string.
# This only looks good for small tensors, which is how it's intended to be used.
def tensor_str(t: torch.Tensor):
    if t.dim() == 0:
        v = t.item()
        if t.is_floating_point():
            if not t.is_nonzero():
                return "0."

            sci = (PRINT_OPTS.sci_mode or
                    (PRINT_OPTS.sci_mode is None and sci_mode(v)))

            # The f-string will generate something like "{.4f}", which is used
            # to format the value.
            return f"{{:.{PRINT_OPTS.precision}{'e' if sci else 'f'}}}".format(v)
        else:
            return '{}'.format(v) # Should we use sci mode for large ints too?
    else:
        slices = [tensor_str(t[i]) for i in range(0, t.size(0))]
        return '[' + ", ".join(slices) + ']'

# %% ../nbs/00_tensors.ipynb 13
def space_join(lst):
    # Join non-empty list elements into a space-sepaeated string
    return " ".join( [ l for l in lst if l] )

# %% ../nbs/00_tensors.ipynb 16
@torch.no_grad()
def lovely(t: torch.Tensor, verbose=False, plain=False):
    if plain:
        return torch._tensor_str._tensor_str(t, indent=0)

    tname = "tensor" if type(t) in [torch.Tensor, torch.nn.Parameter] else type(t).__name__

    grad_fn = "grad_fn" if t.grad_fn else None
    # All tensors along the compute path actually have required_grad=True. Torch __repr__ just dones not show it.
    grad = "grad" if not t.grad_fn and t.requires_grad else None

    shape = str(list(t.shape))

    zeros = style("all_zeros", (127, 127, 127)) if not t.count_nonzero() else None
    pinf = style("+inf!", "red") if t.isposinf().any() else None
    ninf = style("-inf!", "red") if t.isneginf().any() else None
    nan = style("nan!", "red") if t.isnan().any() else None

    attention = space_join([zeros,pinf,ninf,nan])

    x, summary = "", ""
    if not zeros:
        x = "x=" + (tensor_str(t) if t.numel() <= 10 else "...")

        # Make sure it's float32. Also, we calculate stats on good values only.
        ft = t.float()[  torch.isfinite(t) ]

        minmax = f"x∈[{tensor_str(ft.min())}, {tensor_str(ft.max())}]" if t.numel() > 2 and ft.numel() > 2 else None
        meanstd = f"μ={tensor_str(ft.mean())} σ={tensor_str(ft.std())}" if t.numel() >= 2 and ft.numel() >= 2 else None
        numel = f"n={t.numel()}" if t.numel() > 5 else None

        summary = space_join([numel, minmax, meanstd])

    dtnames = { torch.float32: "",
                torch.float16: "fp16",
                torch.float64: "fp64",
                torch.uint8: "u8",
                torch.int32: "i32",
             }

    dtype = dtnames[t.dtype] if t.dtype in dtnames else str(t.dtype)[6:]
    dev = str(t.device) if t.device.type != "cpu" else None

    res = tname + space_join([shape,summary,dtype,grad,grad_fn,dev,attention]) 
    return res + ("\nx=" + torch._tensor_str._tensor_str(t, indent=2) if verbose else " "+x)


# %% ../nbs/00_tensors.ipynb 28
def styled_tensor(t: torch.Tensor, tensor_contents, style):
    assert style in ["plain", "verbose"]
    t = tensor_contents if tensor_contents is not None else t
    t = t.view(t.shape)
    setattr(t, "_lovely_" + style, True)
    return t

# Keep an esiy way to get the standard behavior.
@property
def plain_tensor(t: torch.Tensor, *, tensor_contents=None):
    return styled_tensor(t, tensor_contents, "plain")

# And a verbose option for a good measure.
@property
def verbose_tensor(t: torch.Tensor, *, tensor_contents=None):
    return styled_tensor(t, tensor_contents, "verbose")


# %% ../nbs/00_tensors.ipynb 29
def lovely_repr(t: torch.Tensor, *, tensor_contents=None):
    plain = hasattr(t, "_lovely_plain") and t._lovely_plain
    verbose = hasattr(t, "_lovely_verbose") and t._lovely_verbose

    return lovely(t, plain=plain, verbose=verbose)

# %% ../nbs/00_tensors.ipynb 30
def monkey_patch(cls=torch.Tensor):
    "Monkey-patch lovely features into `cls`" 
    cls.__repr__ = lovely_repr
    cls.plain = plain_tensor
    cls.verbose = verbose_tensor

