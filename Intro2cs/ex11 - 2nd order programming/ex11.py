# FILE: ex11.py
# WRITER: Ofir Birka
# EXERCISE: intro2cs ex11 2015-2016
# DESCRIPTION:  2nd functions

# Imports
import math


# Constants
EPSILON = 1e-5
DELTA = 1e-3
SEGMENTS = 100

# Functions
def plot_func(graph, f, x0, x1, num_of_segments=SEGMENTS, c='black'):
    """
    plot f between x0 and x1 using num_of_segments straight lines.
    use the plot_line function in the graph object. 
    f will be plotted to the screen with color c.
    """
    difference = (x1 - x0)/num_of_segments
    x_previos = x0
    for i in range(1, num_of_segments+1):
        x0_segment = x0 + i*difference
        graph.plot_line((x_previos, f(x_previos)), (x0_segment, f(x0_segment)), c)
        x_previos = x0_segment


def const_function(c):
    """return the mathematical function f such that f(x) = c
    >>> const_function(2)(2)
    2
    >>> const_function(4)(2)
    4
    """
    return lambda x: c


def identity():
    """return the mathematical function f such that f(x) = x
    >>>identity()(3)
    3
    """
    return lambda x: x


def sin_function():
    """return the mathematical function f such that f(x) = sin(x)
    >>> sinF()(math.pi/2)
    1.0
    """
    return math.sin


def sum_functions(g, h):
    """return f s.t. f(x) = g(x)+h(x)"""
    return lambda x: g(x) + h(x)


def sub_functions(g, h):
    """return f s.t. f(x) = g(x)-h(x)"""
    return lambda x: g(x) - h(x)


def mul_functions(g, h):
    """return f s.t. f(x) = g(x)*h(x)"""
    return lambda x: g(x) * h(x)

def div_functions(g, h):
    """return f s.t. f(x) = g(x)/h(x)"""
    return lambda x: g(x) / h(x)

    # The function solve assumes that f is continuous.
    # solve return None in case of no solution
def solve(f, x0=-10000, x1=10000, epsilon=EPSILON):
    """return the solution to f in the range between x0 and x1"""
    if not f(x0)*f(x1) < 0 or epsilon <= 0:
        return None
    if abs(f(x0)) < epsilon:
        return x0
    if abs(f(x1)) < epsilon:
        return x1
    down_limit = x0
    up_limit = x1
    average = (down_limit+up_limit)/2
    while down_limit <= up_limit:
        if abs(f(average)) < epsilon:
            return average
        if f(average) * f(x1) > 0:
            up_limit = average
        else:
            down_limit = average
        average = (down_limit+up_limit)/2
    return None

    # inverse assumes that g is continuous and monotonic. 
def inverse(g, epsilon=EPSILON):
    """return f s.t. f(g(x)) = x"""
    def get_inverse(x):
        h = sub_functions(g, const_function(x))
        x0 = -epsilon
        x1 = epsilon
        solution = solve(h, x0, x1, epsilon)
        while solution is None:
            x0 *= 2
            x1 *= 2
            solution = solve(h, x0, x1, epsilon)
        return solution
    return get_inverse

def compose(g, h):
    """return the f which is the compose of g and h """
    return lambda x: g(h(x))


def derivative(g, delta=DELTA):
    """return f s.t. f(x) = g'(x)"""
    return lambda x: (g(x+delta) - g(x)) / delta


def definite_integral(f, x0, x1, num_of_segments=SEGMENTS):
    """
    return a float - the definite_integral of f between x0 and x1
    >>>definite_integral(const_function(3),-2,3)
    15
    """
    if num_of_segments == 0 or x1-x0 == 0:
        return 0
    riemann_sum = 0
    calc = (x1-x0)/num_of_segments
    for i in range(1, num_of_segments+1):
        x_start = calc*(i-1) + x0
        x_end = calc*i + x0
        riemann_sum += f((x_start+x_end) / 2) * (x_start-x_end)
    return float(riemann_sum)


def integral_function(f, delta=0.01):
    """return F such that F'(x) = f(x)"""
    def get_itegral(x):
        if x < 0:
            x0 = 0
            x1 = x
            g = const_function(-1)
        else:
            x0 = x
            x1 = 0
            g = const_function(1)
        return definite_integral(mul_functions(f, g), x0, x1, math.ceil(abs(x)/delta))
    return get_itegral


def ex11_func_list():
    """return a list of functions as a solution to q.12"""
    sin_x = sin_function()
    cos_x = derivative(sin_function())
    x_power_2 = mul_functions(identity(), identity())
    identity_x = identity()
    func_list = []
    func_list.append(const_function(4))
    func_list.append(sum_functions(sin_x, const_function(4)))
    func_list.append(compose(sin_x, sum_functions(identity_x, const_function(4))))
    func_list.append(div_functions(mul_functions(sin_x, x_power_2), const_function(100)))
    func_list.append(div_functions(sin_x, sum_functions(cos_x, const_function(2))))
    func_list.append(integral_function(
        sub_functions(sum_functions(x_power_2, identity_x), const_function(3))))
    func_list.append(mul_functions(const_function(5), sub_functions(compose(sin_x, cos_x), cos_x)))
    func_list.append(inverse(mul_functions(x_power_2, identity_x)))
    return func_list


# function that generate the figure in the ex description
def example_func(x):
    return (x/5)**3

if __name__ == "__main__":
    import tkinter as tk
    from ex11helper import Graph
    master = tk.Tk()
    graph = Graph(master, -10, -10, 10, 10)
    # un-tag the line below after implementation of plot_func
    #plot_func(graph,example_func,-10,10,SEGMENTS,'red')
    color_arr = ['black', 'blue', 'red', 'green', 'brown', 'purple',
                 'dodger blue', 'orange']
    # un-tag the lines below after implementation of ex11_func_list
    for f in ex11_func_list():
        plot_func(graph, f, -10, 10, SEGMENTS, 'red')
    master.mainloop()
