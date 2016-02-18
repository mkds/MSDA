__author__ = 'Mohan Kandaraj'
import numpy
import timeit

def sortwithloops(input):
    """Sort using iteration"""
    for i in range(len(input)):
        for j in range(i+1,len(input)):
            if input[j] < input[i]:
                input[j],input[i]=input[i],input[j]

    return input

def sortwithoutloops(input):
    """Python Sort function"""
    return input.sort()



def searchwithloops(input, value):
    """Search by looping thru the list"""
    for element in input:
        if value == element:
            return True
    return False



def searchwithoutloops(input, value):
    """Search using python function"""
    return value in input  #return a value

def sortnumpy(input):
    """Numpy sort"""
    return numpy.sort(input)

def sortnumpy1(input):
    """Numpy array self sort"""
    input.sort()

def searchnumpy(input,value):
    """Search numpy..(Provided input is numpy)"""
    return value in input

#Data to be used for timing the functions
L = numpy.random.random_integers(1000, size=5000) #Generate 5K random numbers
na = numpy.array(L)

if __name__ == "__main__":

    setup="from __main__ import sortwithloops, sortwithoutloops, searchwithloops, searchwithoutloops, sortnumpy, sortnumpy1, searchnumpy,L,na; import copy"
    t=timeit.Timer("x=copy.copy(L); sortwithloops(x)",setup)
    print "                Sort using iteration: 5K numbers 3 loops = %s seconds" % (t.timeit(3))
    t=timeit.Timer("x=copy.copy(L); sortwithoutloops(x)",setup)
    print " Sort using built in python function: 5K numbers 3 loops = %s seconds" % (t.timeit(3))
    t=timeit.Timer("x=copy.copy(na); sortnumpy(x)",setup)
    print "      Sort using numpy numpy.sort(x): 5K numbers 3 loops = %s seconds" % (t.timeit(3))
    t=timeit.Timer("x=copy.copy(na); sortnumpy1(x)",setup)
    print "      Sort using numpy x.sort       : 5K numbers 3 loops = %s seconds" % (t.timeit(3))
    print "\n"
    t=timeit.Timer("x=copy.copy(na); sortwithoutloops(x)",setup)
    print " Sort using built in python function: 5K numbers 50 loops = %s seconds" % (t.timeit(50))
    t=timeit.Timer("x=copy.copy(na); sortnumpy(x)",setup)
    print "      Sort using numpy numpy.sort(x): 5K numbers 50 loops = %s seconds" % (t.timeit(50))
    t=timeit.Timer("x=copy.copy(na); sortnumpy1(x)",setup)
    print "      Sort using numpy x.sort       : 5K numbers 50 loops = %s seconds" % (t.timeit(50))
    print "\n"
    t=timeit.Timer("searchwithloops(L,123)",setup)
    print "        Search using iteration : 5K numbers 50 loops = %s seconds" % (t.timeit(50))
    t=timeit.Timer("searchwithoutloops(L,123)",setup)
    print "Search using built in function : 5K numbers 50 loops = %s seconds" % (t.timeit(50))
    t=timeit.Timer("searchnumpy(na,123)",setup)
    print "           Search using numpy  : 5K numbers 50 loops = %s seconds" % (t.timeit(50))



