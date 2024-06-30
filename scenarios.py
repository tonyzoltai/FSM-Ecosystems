#!/usr/bin/env python

'''
scenarios - construct ecosystem scenarios for the FSM-Ecosystems experiment.

Classes:
    None.

Functions:
    create_named_ecosystem - receives command line parameter values from the main program, runs an ecosystem and produces output.
'''

from EcoSystem import EcoSystem, Individual, Evolver


def drift_scores(evolver: Evolver):
    '''Provide the same fitness score for all individuals of an Evolver element - this leads to genetic drift.'''
    for i, _ in enumerate(evolver.individuals):
        evolver.score(i, 1)


def create_CONTROL(population_size, prn_generator):
    '''Create a CONTROL pattern ecosystem.  This is a single Evolver, with no selection, i.e. genetically drifting. '''
    e = EcoSystem()
    d = Evolver(Individual, population_size, prn_generator)
    e.add_element(d)
    e.add_relationship(lambda: drift_scores(d))
    return e
    

# UNIT TESTING

import unittest as ut

class TestScenarios(ut.TestCase):
    def test_CONTROL(self) -> None:
        e = create_CONTROL(10, None)
        self.assertEqual(len(e.elements[0].individuals), 10)
        self.assertEqual(len(e.relationships), 1)


if __name__ == '__main__':

    ut.main()