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

from games import run_competition, run_cooperation, run_mismatch_coop


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

def mismatch_coop_scores(c1: Evolver, c2: Evolver):
    '''Two Evolvers cooperate, but BOTH are rewarded for NOT matching.'''
    for i1, m1 in enumerate(c1.individuals):
        for i2, m2 in enumerate(c2.individuals):
            s1, s2 = run_mismatch_coop(m1, m2)
            c1.score(i1, s1)
            c2.score(i2, s2)


# SCENARIO CREATOR FUNCTIONS
# Each function creates an ecosystem scenario.  Standardised parameters:
# population_size: the number of individuals in the initial population
# prn_generator: pseudo-random-number generator to use (by passing this around, we can ensure an entire simulation run uses the same generator and original seed)
# random_out: TRUE if the outputs of the initial automata are to be randomised from the output alphabet; FALSE if canonical 0 output is OK.

def random_out_Individual(rng):
    '''Create a default Individual, but set its output randomly, using the provided random generator.'''
    i = Individual()
    i.set_output(0, rng.choice(list(i.outputs())))
    return i

def create_CONTROL(population_size, prn_generator, random_out = False):
    '''Create a CONTROL pattern ecosystem.  This is a single Evolver, with no selection, i.e. genetically drifting. '''

    if random_out:
        individual_creator = lambda: random_out_Individual(prn_generator)
    else:
        individual_creator = Individual

    e = EcoSystem()
    d = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(d)
    e.add_relationship(lambda: drift_scores(d))
    return e

def create_COMP(population_size, prn_generator, random_out = False):
    '''Create a COMP ecosystem.  This is two Evolvers competing, i.e. one rewarded for matching, the other for not.'''

    if random_out:
        individual_creator = lambda: random_out_Individual(prn_generator)
    else:
        individual_creator = Individual

    e = EcoSystem()
    c1 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c1)
    c2 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c2)
    e.add_relationship(lambda: competition_scores(c1, c2))
    return e

def create_COOP(population_size, prn_generator, random_out = False):
    '''Create a COOP ecosystem.  This is two Evolvers cooperating, i.e. both are rewarded for matching, neither for not.'''

    if random_out:
        individual_creator = lambda: random_out_Individual(prn_generator)
    else:
        individual_creator = Individual

    e = EcoSystem()
    c1 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c1)
    c2 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c2)
    e.add_relationship(lambda: cooperation_scores(c1, c2))
    return e

def create_MISMATCH_COOP(population_size, prn_generator, random_out = False):
    '''Create a COOP ecosystem, but both Evolvers are rewarded for NOT matching.'''

    if random_out:
        individual_creator = lambda: random_out_Individual(prn_generator)
    else:
        individual_creator = Individual

    e = EcoSystem()
    c1 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c1)
    c2 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c2)
    e.add_relationship(lambda: mismatch_coop_scores(c1, c2))
    return e

# Scenario Coding:
# X - COMP
# C - COOP
# M - MISMATCH_COOP
# letter 1: link between elements a and b
# letterw 2-3: links from a to c and b to c
# letters 4-6: links from a to d, b to d and c to d
#
#TO FROM
# v abc
#  +---
# b|1..
# c|23.
# d|456
#
# e.g. - M - a mismatch-cooperates with b
# e.g. - C_X - a cooperates with b which competes with c
# e.g. - CXC - a cooperates with b and competes with c, b cooperates with c
# e.g. - CXM__X - a cooperates with b and competes with c, b mismatch-cooperates with c, a and b have no link to d, but c competes with d

def create_C_X(population_size, prn_generator, random_out = False):
    '''Create a "Mix 3" ecosystem, A cooperates with B, which competes with C.'''

    if random_out:
        individual_creator = lambda: random_out_Individual(prn_generator)
    else:
        individual_creator = Individual

    e = EcoSystem()
    c1 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c1)
    c2 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c2)
    c3 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c3)

    e.add_relationship(lambda: cooperation_scores(c1, c2))
    e.add_relationship(lambda: competition_scores(c2, c3))
    return e

def create_M_X(population_size, prn_generator, random_out = False):
    '''Create a "Mix 3" ecosystem, A cooperates with B, which competes with C.'''

    if random_out:
        individual_creator = lambda: random_out_Individual(prn_generator)
    else:
        individual_creator = Individual

    e = EcoSystem()
    c1 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c1)
    c2 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c2)
    c3 = Evolver(individual_creator, population_size, prn_generator)
    e.add_element(c3)

    e.add_relationship(lambda: mismatch_coop_scores(c1, c2))
    e.add_relationship(lambda: competition_scores(c2, c3))
    return e

# UNIT TESTING

import unittest as ut

class TestScenarios(ut.TestCase):
    def test_CONTROL(self) -> None:
        e = create_CONTROL(10, numpy.random.default_rng(0), True)
        self.assertEqual(len(e.elements[0].individuals), 10)
        self.assertEqual(len(e.relationships), 1)
        self.assertEqual(e.elements[0].individuals[2].output(0), 1)
        self.assertEqual(e.elements[0].individuals[3].output(0), 0)

    def test_MISMATCH_COOP(self) -> None:
        rng = numpy.random.default_rng(0)
        e = create_MISMATCH_COOP(10, rng)
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