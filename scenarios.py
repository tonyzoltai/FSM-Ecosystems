#!/usr/bin/env python

'''
scenarios - construct ecosystem scenarios for the FSM-Ecosystems experiment.

Classes:
    None.

Functions:
    create_CONTROL - Create the CONTROL scenario of a single Evolver lineage drifting genetically.
    create_COMP - Create the COMP scenario of two Evolver lineages in competition.
'''

import numpy

from EcoSystem import EcoSystem, Individual, Evolver

from games import run_competition, run_cooperation


def drift_scores(evolver: Evolver):
    '''Provide the same fitness score for all individuals of an Evolver element - this leads to genetic drift.'''
    for i, _ in enumerate(evolver.individuals):
        evolver.score(i, 1)

def competition_scores(c1: Evolver, c2:Evolver):
    '''Two Evolvers compete, so either one is rewarded for matching, or the other for not.'''
    for i1, m1 in enumerate(c1.individuals):
        for i2, m2 in enumerate(c2.individuals):
            s1, s2 = run_competition(m1, m2)
            c1.score(i1, s1)
            c2.score(i2, s2)

def cooperation_scores(c1: Evolver, c2: Evolver):
    '''Two Evolvers cooperate, so both are rewarded for matching, neither rewarded for not.'''
    for i1, m1 in enumerate(c1.individuals):
        for i2, m2 in enumerate(c2.individuals):
            s1, s2 = run_cooperation(m1, m2)
            c1.score(i1, s1)
            c2.score(i2, s2)



def create_CONTROL(population_size, prn_generator):
    '''Create a CONTROL pattern ecosystem.  This is a single Evolver, with no selection, i.e. genetically drifting. '''
    e = EcoSystem()
    d = Evolver(Individual, population_size, prn_generator)
    e.add_element(d)
    e.add_relationship(lambda: drift_scores(d))
    return e

def create_COMP(population_size, prn_generator):
    '''Create a COMP ecosystem.  This is two Evolvers competing, i.e. one rewarded for matching, the other for not.'''
    e = EcoSystem()
    c1 = Evolver(Individual, population_size, prn_generator)
    e.add_element(c1)
    c2 = Evolver(Individual, population_size, prn_generator)
    e.add_element(c2)
    e.add_relationship(lambda: competition_scores(c1, c2))
    return e

def create_COOP(population_size, prn_generator):
    '''Create a COOP ecosystem.  This is two Evolvers cooperating, i.e. both are rewarded for matching, neither for not.'''
    e = EcoSystem()
    c1 = Evolver(Individual, population_size, prn_generator)
    e.add_element(c1)
    c2 = Evolver(Individual, population_size, prn_generator)
    e.add_element(c2)
    e.add_relationship(lambda: cooperation_scores(c1, c2))
    return e    

# UNIT TESTING

import unittest as ut

class TestScenarios(ut.TestCase):
    def test_CONTROL(self) -> None:
        e = create_CONTROL(10, None)
        self.assertEqual(len(e.elements[0].individuals), 10)
        self.assertEqual(len(e.relationships), 1)

class TestEcoSystem(ut.TestCase):
        def test_EcoSystem(self):
            print("Testing CONTROL")
            es = create_CONTROL(2, numpy.random.default_rng(0))
            self.assertEqual(len(es.elements), 1)
            self.assertEqual(len(es.relationships), 1)
            es.next_gen()
            print("CONTROL, gen 1")
            for i in es.elements:
                for j in i.individuals:
                    print(j)
                    print("")
            es.next_gen()
            print("CONTROL, gen 2")
            for i in es.elements:
                for j in i.individuals:
                    print(j)
                    print("")


if __name__ == '__main__':

    ut.main()