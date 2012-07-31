import unittest

import scipy

import lsodar
odeintr = lsodar.odeintr

# XXX: I don't understand the banded jacobian case properly, so I don't have
#      tests for it.

# This test problem is from the lsodar documentation.
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

class test_lsodar(unittest.TestCase):
    def test_basic(self):
        """ Basic test of lsodar """
        y = odeintr(func, y0, t,
                    rtol = 1e-4, atol = [1e-6, 1e-10, 1e-6])

        self.assertAlmostEqual(y[1][1], 3.386380e-5, 4)
        self.assertAlmostEqual(y[6][2], 9.610125e-1, 4)

    def test_Dfun(self):
        """ Test user-supplied Jacobian """
        y = odeintr(func, y0, t, Dfun=Dfun,
                    rtol=1e-4, atol=[1e-6, 1e-10, 1e-6])

        self.assertAlmostEqual(y[1][1], 3.386380e-5, 4)
        self.assertAlmostEqual(y[6][2], 9.610125e-1, 4)

    def test_full_output(self):
        """ Test full_output """
        y, info_dict = odeintr(func, y0, t, Dfun=Dfun,
                               full_output=True, rtol=1e-4,
                               atol=[1e-6, 1e-10, 1e-6])

        for key, val in info_dict.items():
            if key != 'message':
                self.assertEqual(len(y) - 1, len(val))
        self.assertAlmostEqual(y[1][1], 3.386380e-5, 4)
        self.assertAlmostEqual(y[6][2], 9.610125e-1, 4)

    def test_h0(self):
        """ Test h0 """
        # XXX: This only tests that h0 doesn't screw up the integration.
        # It doesn't actually ensure that it is used, since I don't know
        #  how to test for that.
        h0 = 1.
        y, info_dict = odeintr(func, y0, t, Dfun=Dfun,
                               full_output=True, rtol=1e-4,
                               atol=[1e-6, 1e-10, 1e-6],
                               h0 = h0)

        self.assertAlmostEqual(y[1][1], 3.386380e-5, 4)
        self.assertAlmostEqual(y[6][2], 9.610125e-1, 4)

    def test_hmax(self):
        """ Test hmax  """
        hmax = 1e8
        y, info_dict = odeintr(func, y0, t, Dfun=Dfun,
                               full_output=True, rtol=1e-4,
                               atol=[1e-6, 1e-10, 1e-6],
                               hmax = hmax)

        for hu in info_dict['hu']:
            assert(hu <= hmax)
        self.assertAlmostEqual(y[1][1], 3.386380e-5, 4)
        self.assertAlmostEqual(y[6][2], 9.610125e-1, 4)

    def test_hmin(self):
        """ Test hmin  """
        # XXX: Not sure how to test hmin. Integrator dies if hmin is too small,
        #      and I don't get the smallest stepsize taken in the info_dict.
        hmin = 1e-6
        y, info_dict = odeintr(func, y0, t, Dfun=Dfun,
                               full_output=True, rtol=1e-4,
                               atol=[1e-6, 1e-10, 1e-6],
                               hmin = hmin)

        self.assertAlmostEqual(y[1][1], 3.386380e-5, 4)
        self.assertAlmostEqual(y[6][2], 9.610125e-1, 4)

    def test_ixpr(self):
        """ Test ixpr """
        # XXX: Need a different example to text ixpr. This example always uses
        #      stiff methods.
        y, info_dict = odeintr(func, y0, t, Dfun=Dfun,
                               full_output=True, rtol=1e-4,
                               atol=[1e-6, 1e-10, 1e-6],
                               ixpr=True)

        self.assertAlmostEqual(y[1][1], 3.386380e-5, 4)
        self.assertAlmostEqual(y[6][2], 9.610125e-1, 4)

    def test_mxstep(self):
        """ Test mxstep """
        # XXX: Annoying that this is expected to print an error message,
        #      at least if I'm following odeint semantics.
        print
        mxstep = 20
        y, info_dict = odeintr(func, y0, t, Dfun=Dfun,
                               full_output=True, rtol=1e-4,
                               atol=[1e-6, 1e-10, 1e-6],
                               mxstep=mxstep)

        assert(info_dict['nst'][0] <= mxstep)

    def test_mxhnil(self):
        """ Test mxhnil """
        # XXX: Not sure how to test this.
        mxhnil = 10
        y, info_dict = odeintr(func, y0, t, Dfun=Dfun,
                               full_output=True, rtol=1e-4,
                               atol=[1e-6, 1e-10, 1e-6],
                               mxhnil=mxhnil)

        self.assertAlmostEqual(y[1][1], 3.386380e-5, 4)
        self.assertAlmostEqual(y[6][2], 9.610125e-1, 4)

    def test_mxordn(self):
        """ Test mxordn """
        # XXX: Again, need a non-stiff example, and there's no way I can see
        #      what order was actually used
        mxordn = 4
        y, info_dict = odeintr(func, y0, t, Dfun=Dfun,
                               full_output=True, rtol=1e-4,
                               atol=[1e-6, 1e-10, 1e-6],
                               mxordn=mxordn)

        self.assertAlmostEqual(y[1][1], 3.386380e-5, 4)
        self.assertAlmostEqual(y[6][2], 9.610125e-1, 4)

    def test_mxords(self):
        """ Test mxords """
        # XXX: There's no way I can see what order was actually used.
        #      I could check that integration goes bad if mxords is too low,
        #      but that seems silly.
        mxords = 3
        y, info_dict = odeintr(func, y0, t, Dfun=Dfun,
                               full_output=True, rtol=1e-4,
                               atol=[1e-6, 1e-10, 1e-6],
                               mxords=mxords)

        self.assertAlmostEqual(y[1][1], 3.386380e-5, 4)
        self.assertAlmostEqual(y[6][2], 9.610125e-1, 4)

    def test_mxstep(self):
        """ Test mxstep """
        # XXX: Annoying that this prints messages. Maybe I could capture them?
        print
        y, info_dict = odeintr(func, y0, t, Dfun=Dfun,
                               full_output=True, rtol=1e-4,
                               atol=[1e-6, 1e-10, 1e-6],
                               printmessg=True)

    def test_noterm_roots(self):
        """ Test basic root finding """
        root_term = [0, 0]
        y, tout, t_root, y_root, i_root, info_dict = \
                odeintr(func, y0, t, Dfun=Dfun,
                        full_output=True, rtol=1e-4,
                        atol=[1e-6, 1e-10, 1e-6],
                        root_func = root_func, root_term = root_term)

        self.assertAlmostEqual(t_root[0], 2.6400e-1, 4)
        self.assertAlmostEqual(y_root[0][1], 3.470563e-5, 4)
        self.assertEqual(i_root[0], 1)
        self.assertAlmostEqual(y_root[1][1], 4.000395e-10, 4)
        # Negative number of decimal places here...
        self.assertAlmostEqual(t_root[1], 2.0745e7, -3)
        self.assertEqual(i_root[1], 0)

        out_index = tout.index(t[1])
        self.assertAlmostEqual(y[out_index][1], 3.386380e-5, 4)
        out_index = tout.index(t[6])
        self.assertAlmostEqual(y[out_index][2], 9.610125e-1, 4)

    def test_term_roots(self):
        """ Test root finding with termination """
        root_term = [1, 0]
        y, tout, t_root, y_root, i_root, info_dict = \
                odeintr(func, y0, t, Dfun=Dfun,
                        full_output=True, rtol=1e-4,
                        atol=[1e-6, 1e-10, 1e-6],
                        root_func = root_func, root_term = root_term)

        self.assertAlmostEqual(t_root[0], 2.6400e-1, 4)
        self.assertAlmostEqual(y_root[0][1], 3.470563e-5, 4)
        self.assertEqual(i_root[0], 1)
        self.assertAlmostEqual(y_root[1][1], 4.000395e-10, 4)
        # Negative number of decimal places here...
        self.assertAlmostEqual(t_root[1], 2.0745e7, -3)
        self.assertEqual(i_root[1], 0)
        # Check that we stopped at the proper point
        self.assertEqual(tout[-1], t_root[1])
        self.assertEqual(y[-1][0], y_root[1][0])

    def test_int_pts(self):
        """ Test intermediate output """
        y, tout = odeintr(func, y0, t,
                          rtol = 1e-4, atol = [1e-6, 1e-10, 1e-6],
                          int_pts = True)

        out_index = tout.index(t[1])
        self.assertAlmostEqual(y[out_index][1], 3.386380e-5, 4)
        out_index = tout.index(t[6])
        self.assertAlmostEqual(y[out_index][2], 9.610125e-1, 4)
        self.assertEqual(t[-1], tout[-1])

    def test_tcrit(self):
        """ Test critical times """
        # Really only tests that tcrit doesn't mess up integration. The
        #  success of the int_pts test suggests, however, that tcrit is
        #  working properly.
        y = odeintr(func, y0, t,
                    rtol = 1e-4, atol = [1e-6, 1e-10, 1e-6],
                    tcrit = [0.2, 0.9, 1.7])

        self.assertAlmostEqual(y[1][1], 3.386380e-5, 4)
        self.assertAlmostEqual(y[6][2], 9.610125e-1, 4)

suite = unittest.makeSuite(test_lsodar, 'test lsodar')

if __name__ == '__main__':
    unittest.main()
