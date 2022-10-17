Lovely Tensors
================

<!-- WARNING: THIS FILE WAS AUTOGENERATED! DO NOT EDIT! -->

## Install

``` sh
pip install lovely-tensors
```

## How to use

How often do you find yourself debuggin a neural network? You dump a
tensor to the cell output, and see this:

``` python
numbers
```

    tensor([[[-0.3541, -0.3369, -0.4054,  ..., -0.5596, -0.4739,  2.2489],
             [-0.4054, -0.4226, -0.4911,  ..., -0.9192, -0.8507,  2.1633],
             [-0.4739, -0.4739, -0.5424,  ..., -1.0390, -1.0390,  2.1975],
             ...,
             [-0.9020, -0.8335, -0.9363,  ..., -1.4672, -1.2959,  2.2318],
             [-0.8507, -0.7822, -0.9363,  ..., -1.6042, -1.5014,  2.1804],
             [-0.8335, -0.8164, -0.9705,  ..., -1.6555, -1.5528,  2.1119]],

            [[-0.1975, -0.1975, -0.3025,  ..., -0.4776, -0.3725,  2.4111],
             [-0.2500, -0.2325, -0.3375,  ..., -0.7052, -0.6702,  2.3585],
             [-0.3025, -0.2850, -0.3901,  ..., -0.7402, -0.8102,  2.3761],
             ...,
             [-0.4251, -0.2325, -0.3725,  ..., -1.0903, -1.0203,  2.4286],
             [-0.3901, -0.2325, -0.4251,  ..., -1.2304, -1.2304,  2.4111],
             [-0.4076, -0.2850, -0.4776,  ..., -1.2829, -1.2829,  2.3410]],

            [[-0.6715, -0.9853, -0.8807,  ..., -0.9678, -0.6890,  2.3960],
             [-0.7238, -1.0724, -0.9678,  ..., -1.2467, -1.0201,  2.3263],
             [-0.8284, -1.1247, -1.0201,  ..., -1.2641, -1.1596,  2.3786],
             ...,
             [-1.2293, -1.4733, -1.3861,  ..., -1.5081, -1.2641,  2.5180],
             [-1.1944, -1.4559, -1.4210,  ..., -1.6476, -1.4733,  2.4308],
             [-1.2293, -1.5256, -1.5081,  ..., -1.6824, -1.5256,  2.3611]]])

Was it really useful?

What is the shape?  
What are the statistics?  
Are any of the values `nan` or `int`?  
Is it an image of a man holding a tench?

``` python
import lovely_tensors.tensors as lt
```

``` python
# A very short tensor
print(lt.lovely(numbers.view(-1)[:2]))
```

    tensor[2] μ=-0.345 σ=0.012 x=[-0.354, -0.337]

``` python
# A slightly longer tensor
print(lt.lovely(numbers.view(-1)[:6].view(2,3)))
```

    tensor[2, 3] n=6 x∈[-0.440, -0.337] μ=-0.388 σ=0.038 x=[[-0.354, -0.337, -0.405], [-0.440, -0.388, -0.405]]

``` python
t = numbers.view(-1)[:12].clone()

t[0] *= 10000
t[1] /= 10000
t[2] = float('inf')
t[3] = float('-inf')
t[4] = float('nan')
t = t.reshape((2,6))

print(t)
print("\n")

# A spicy tensor
print(lt.lovely(t))

# A zero tensor
print(lt.lovely(torch.zeros(10, 10)))
```

    tensor([[-3.5405e+03, -3.3693e-05,         inf,        -inf,         nan, -4.0543e-01],
            [-4.2255e-01, -4.9105e-01, -5.0818e-01, -5.5955e-01, -5.4243e-01, -5.0818e-01]])


    tensor[2, 6] n=12 x∈[-3.541e+03, -3.369e-05] μ=-393.776 σ=1.180e+03 +inf! -inf! nan! x=...
    tensor[10, 10] all_zeros 

``` python
# Too long to show values
lt.lovely(numbers)
```

    'tensor[3, 196, 196] n=115248 x∈[-2.118, 2.640] μ=-0.388 σ=1.073 x=...'

Now the important queston - is it the Tenchman?

``` python
lt.show_rgb(numbers)
```

![](index_files/figure-gfm/cell-8-output-1.png)

*Maaaaybe?* Looks like someone normalized him.

``` python
in_stats = { "mean": (0.485, 0.456, 0.406), "std": (0.229, 0.224, 0.225) }
lt.show_rgb(numbers, in_stats)
```

![](index_files/figure-gfm/cell-9-output-1.png)

There can be no doubt.

One last thing - let’s monkey-patch `torch.Tensor` for convenience.

``` python
lt.monkey_patch()

t
```

    tensor[2, 6] n=12 x∈[-3.541e+03, -3.369e-05] μ=-393.776 σ=1.180e+03 +inf! -inf! nan! x=...

``` python
t.verbose
```

    tensor[2, 6] n=12 x∈[-3.541e+03, -3.369e-05] μ=-393.776 σ=1.180e+03 +inf! -inf! nan!
    x=[[-3.5405e+03, -3.3693e-05,         inf,        -inf,         nan, -4.0543e-01],
       [-4.2255e-01, -4.9105e-01, -5.0818e-01, -5.5955e-01, -5.4243e-01, -5.0818e-01]]

``` python
t.plain
```

    [[-3.5405e+03, -3.3693e-05,         inf,        -inf,         nan, -4.0543e-01],
     [-4.2255e-01, -4.9105e-01, -5.0818e-01, -5.5955e-01, -5.4243e-01, -5.0818e-01]]

``` python
numbers.rgb
```

![](index_files/figure-gfm/cell-13-output-1.png)

``` python
# The values are the same, but we de-norm before displaying.
numbers.denorm=in_stats
numbers.rgb
```

![](index_files/figure-gfm/cell-14-output-1.png)
