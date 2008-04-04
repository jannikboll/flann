#!/usr/bin/python

# Now go to work
from pyflann import *
from copy import copy
from numpy import *
from numpy.random import *
import unittest


class Test_PyFLANN_nn(unittest.TestCase):

    def setUp(self):
        self.nn = FLANN()


class Test_PyFLANN_nn_index(unittest.TestCase):

    def testnn_index_random_permute(self):

        numtests = 500
        dim = 10
        N = 100

        nns = [None]*numtests
        x   = [rand(N, dim) for i in xrange(numtests)]
        d   = empty(numtests, dtype=index_type)
        correct = empty(numtests, dtype=bool_)
        
        for i in permutation(numtests):
            nns[i] = FLANN()
            nns[i].build_index(x[i])
            
            # For kicks
            if rand() < 0.5:
                nns[i].kmeans(x[i], 5)
            if rand() < 0.5:
                nns[i].nn(x[i], x[i])

        for i in permutation(numtests):
            correct[i] = all(nns[i].nn_index(x[i]) == arange(N, dtype = index_type))

        for i in reversed(xrange(numtests)):
            if rand() < 0.5:
                nns[i].delete_index()
            else:
                del nns[i]

        self.assert_(all(correct))

    def testnn_index_bad_index_call_noindex(self):

        nn = FLANN()
        self.assertRaises(FLANNException, lambda: nn.nn_index(rand(5,5)))


    def testnn_index_bad_index_call_delindex(self):
        nn = FLANN()
        nn.build_index(rand(5,5))
        nn.delete_index()
        
        self.assertRaises(FLANNException, lambda: nn.nn_index(rand(5,5)))


if __name__ == '__main__':
    unittest.main()
