import cython

@cython.cfunc
@cython.exceptval(-2, check=True)
def f(x: cython.double) -> cython.double:
    return x ** 2 - x

@cython.cfunc
def integrate_f(a: cython.double, b: cython.double, N: cython.int):
    i: cython.int
    s: cython.double
    dx: cython.double
    s = 0
    dx = (b-a)/N
    for i in range(N):
        s += f(a+i*dx)
    return s * dx

@cython.cfunc
def say_hello_to(name):
    print(f"Hello {name}!")
