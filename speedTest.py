import time

import scipy
from scipy.integrate import odeint

from lsodar import *

def func(y, t):
    ydot = scipy.zeros(3, scipy.float64)
    ydot[0] = -0.04 * y[0] + 1e4*y[1]*y[2]
    ydot[1] = 0.04 * y[0] - 1e4*y[1]*y[2] - 3e7*y[1]**2
    ydot[2] = 3e7*y[1]**2
    return ydot

def Dfun(y, t):
    pd = scipy.zeros((3,3), scipy.float64)
    pd[0,0] = -0.04
    pd[0,1] = 1e4*y[2]
    pd[0,2] = 1e4*y[1]
    pd[1,0] = 0.04
    pd[1,1] = -1e4*y[2] - 6e7*y[1]
    pd[1,2] = -1e4*y[1]
    pd[2,1] = 6e7*y[1]
    return pd

def root_func(y, t):
    out = scipy.zeros(2, scipy.float64)
    out[0] = y[0] - 1e-4
    out[1] = y[2] - 1e-2
    return out

y0 = [1.0, 0, 0]
t = scipy.array([0] + [4 * 10**x for x in range(-1, 11)])

start_time = time.clock()
for ii in range(1000):
    y = odeintr(func, y0, t, Dfun=Dfun,
                rtol=1e-4, atol=[1e-6, 1e-10, 1e-6])
print 'odeintr took %f seconds' % (time.clock() - start_time)

start_time = time.clock()
for ii in range(1000):
    y = odeint(func, y0, t, Dfun=Dfun,
                rtol=1e-4, atol=[1e-6, 1e-10, 1e-6])
print 'odeint took %f seconds' % (time.clock() - start_time)
