#!/usr/bin/env python

'''
EcoSystem - Class to implement an ecosystem of evolving lineages and selection pressures.
Based on work by Moran & Pollack:
https://www.researchgate.net/publication/332133143_Evolving_Complexity_in_Prediction_Games


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

import copy
import numpy

from automata import CanonicalMooreMachine
from Hopcroft import Hopcroft_minimised


def moran_pollack_mutate(mm_parent: CanonicalMooreMachine, mutation, rng):
    '''Mutate the CanonicalMooreMachine mm_parent and return the result.  Mutations as described in Moran & Pollack.'''

    def random_state(m: CanonicalMooreMachine):
        return rng.choice(m.states())

    def add_new_state(m: CanonicalMooreMachine):
        # Add a state.
        m.add_state()

        # Remember the new state
        new_state = m.state_count() - 1

        # Random output
        m.set_output(new_state, rng.choice(list(m.outputs())))

        # For each input symbol, set the outgoing link from the new state randomly.
        for s in m.inputs():
            m.set_arc(new_state, s, random_state(m))

    def remove_existing_state(m: CanonicalMooreMachine):
        # Remove a random state, re-point incoming links to other random states.
        # Designate new start state if it was the start state (no effect at all on one-state automata).

        # Is there only one state? Only do this if there are more than 1.
        if m.state_count() > 1:
            q = random_state(m)
            # First - if this is the starting state, swap it with a random one.
            if q == m.starting_state():
                # Choose another starting state, and swap it with the current one.
                while True:
                    q = random_state(m)
                    if q != m.starting_state():
                        break

                m.set_starting_state(q)
                # At this point, q is no longer a starting state, and can be removed.

            # Make the state unreachable by re-pointing the incoming links.
            for s in m.states():
                for c in m.inputs():
                    if m.next_state(s, c) == q:
                        while True:
                            n = random_state(m)
                            if n != q:
                                break
                        m.set_arc(s, c, n)
            
            m.delete_state(q)


    def redirect(m: CanonicalMooreMachine):
        m.set_arc(random_state(m), rng.choice(m.inputs()), random_state(m))

    def new_output(m: CanonicalMooreMachine):
        m.set_output(random_state(m), rng.choice(list(m.outputs())))


    # First, make a copy of the given parent object
    m = copy.deepcopy(mm_parent)

    match mutation:
        case 0:
            add_new_state(m)
        case 1:
            remove_existing_state(m)
        case 2:
            # Redirect a link - pick a random link and point it to a random state.
            redirect(m)
        case 3:
            # Change a random state's output to a random output alphabet symbol.
            new_output(m)

    return m

class Individual(CanonicalMooreMachine):
    '''An individual instance of an Evolver.'''
    def __init__(self) -> None:
            '''Initialise as a CanonicalMooreMachine with binary input and output.'''
            super().__init__(1, 2, 2)

    def __str__(self):
        return str(self.state_count())

    def complexity(self):
        return Hopcroft_minimised(self).state_count()

class Element(object):
    def __init__(self) -> None:
        pass


class Evolver(Element):
    '''This is the Element of most interest - it evolves according to selection scores, with mutations from a given RN generator.'''
    def __init__(self, individual_creator, population_size, generator) -> None:
        super().__init__()

        self.create_individual = individual_creator

        self.individuals = [self.create_individual() for _ in range(population_size)]

        self.reset_scores()

        self.population_size = population_size
        self.rng = generator
    
    def __str__(self):
        return str([str(i) for i in self.individuals])

    def reset_scores(self):
        self.scores = [0 for i in self.individuals]
    
    def next_gen(self):
        '''Replace the current generation with mutated offspring, with replication rate proportional to score.'''

        # Scale probabilities to scores
        total = sum(self.scores)
        if total == 0:
            prob = [1 / len(self.scores) for _ in self.scores]
        else:
            prob = [s / total for s in self.scores]

        # select parents according to probability
        parents = self.rng.choice(self.individuals, len(self.individuals), True, prob)

        children = [moran_pollack_mutate(p, self.rng.integers(4), self.rng) for p in parents]
        self.individuals = children
        self.reset_scores()

    def individual(self, i):
        return self.individuals[i]
    
    def score(self, i, s):
        self.scores[i] += s


class Fixed(Element):
    '''This Element does not change over the generations. Represents stable elements of the ecosystem.'''
    def __init__(self, CMM) -> None:
        super().__init__()
        self.thing = CMM


class EcoSystem(object):
    '''A group of interacting lineages '''
    def __init__(self) -> None:
        self.elements = []
        self.relationships = []

    def __repr__(self):
        '''Unambiguous representation as a string.'''
        return ()

    def add_element(self, element):
        '''Add an element to the ecosystem.'''
        self.elements.append(element)

    def add_relationship(self, relationship):
        '''Add a relationship - this will be called as a function with no parameters to generate scores for evolutionary selection.'''
        self.relationships.append(relationship)
        
    def generations(self):
        '''generations - an unending iterator, yielding the collection of ecosystem elements in each generation.'''
        yield self.elements
        while True:
            self.next_gen()
            yield self.elements

    def next_gen(self):
        for e in self.elements:
            e.reset_scores()
        
        for r in self.relationships:
            r()

        for e in self.elements:
            e.next_gen()
        
        return


# UNIT TESTING

import unittest as ut

class TestEvolver(ut.TestCase):
    def test_init(self) -> None:
        e = Evolver(Individual, 10, None)
        self.assertEqual(len(e.individuals), 10)
        self.assertEqual(sum(e.scores), 0)

    def test_score(self):
        e = Evolver(Individual, 4, None)
        for i in range(4):
            e.score(i,i)
        self.assertEqual(sum(e.scores), 6)
        self.assertEqual(e.scores[3], 3)
        e.reset_scores()
        self.assertEqual(sum(e.scores), 0)

    def test_individual(self):
        e = Evolver(Individual, 2, None)
        self.assertIs(e.individual(1), e.individuals[1])

    def test_next_gen(self):
        rng = numpy.random.default_rng(24)
        e = Evolver(Individual, 2, rng)
        print("Gen 0")
        for i in e.individuals:
            print(i)
            print("")
        for i in range(len(e.individuals)):
            e.score(i, 1)
        e.next_gen()
        print("Gen 1")
        for i in e.individuals:
            print(i)
            print("")

        self.assertEqual(e.individuals[0].next_state(0,0), 0)
        self.assertEqual(e.individuals[0].state_count(), 1)
        self.assertEqual(e.individuals[0].output(0), 1)

        self.assertEqual(e.individuals[1].state_count(), 2)
        self.assertEqual(e.individuals[1].next_state(1, 0), 0)
        self.assertEqual(e.individuals[1].next_state(1, 1), 1)
        self.assertEqual(e.individuals[1].output(1), 1)


class TestMutate(ut.TestCase):
    def test_mutate(self):
        rng = numpy.random.default_rng(3)

        m = CanonicalMooreMachine.from_string(( "0 0 1 2\n"
                                                "1 1 0 2\n"
                                                "2 2 0 3\n"
                                                "3 0 3 2"))
        print(m)

        print("Add a state")
        m = moran_pollack_mutate(m, 0, rng)
        #print("")
        print(m)
        self.assertEqual(m.state_count(), 5)

        print("Delete a state")
        m = moran_pollack_mutate(m, 1, rng)
        #print("")
        print(m)
        self.assertEqual(m.state_count(), 4)

        print("Redirect an arc")
        m = moran_pollack_mutate(m, 2, rng)
        #print("")
        print(m)
        self.assertEqual(m.next_state(0, 0), 2)

        print("Change an output")
        m = moran_pollack_mutate(m, 3, rng)
        #print("")
        print(m)
        self.assertEqual(m.output(0), 3)

        self.assertEqual(m.next_state(1, 1), 0)

        self.assertEqual(m.next_state(3,2), 2)



if __name__ == '__main__':

    ut.main()

