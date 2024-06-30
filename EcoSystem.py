#!/usr/bin/env python

'''
EcoSystem - Class to implement an ecosystem of evolving lineages and selection pressures.

Classes:
...

Functions:
...
'''


__author__ = "Gabor 'Tony' Zoltai"
__copyright__ = "Copyright 2024, Gabor Zoltai"
__credits__ = ["Gabor Zoltai"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Tony Zoltai"
__email__ = "tony.zoltai@gmail.com"
__status__ = "Prototype"

class EcoSystem(object):
    '''A group of interacting lineages '''
    def __init__(self, population_size = 50) -> None:
        pass

    def generations(self):
        yield "first gen"
        yield "second gen"
        yield "third gen"
        return 