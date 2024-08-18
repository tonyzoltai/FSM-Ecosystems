#!/usr/bin/env python
'''Games - prediction games played between Moore Machines.

Classes:
    None.

Functions:
    run_competition - run a competitive game between two Machines.  One gets rewarded for matching, the other for not.
    run_cooperation - run a cooperative game between two Machiens.  Both get rewarded for matching, neither for not.
'''

__author__ = "Gabor 'Tony' Zoltai"
__copyright__ = "Copyright 2024, Gabor Zoltai"
__credits__ = ["Gabor Zoltai"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Tony Zoltai"
__email__ = "tony.zoltai@gmail.com"
__status__ = "Prototype"

import automata

# Reward styles.
REWARD_ZERO = 0
REWARD_MATCH = 1
REWARD_MISMATCH = 2


def run_competition(m1, m2):
    return run_game(m1, m2, REWARD_MATCH, REWARD_MISMATCH)

def run_cooperation(m1, m2):
    return run_game(m1, m2, REWARD_MATCH, REWARD_MATCH)

def run_mismatch_coop(m1, m2):
    return run_game(m1, m2, REWARD_MISMATCH, REWARD_MISMATCH)


def run_game(m1, m2, reward1, reward2):
    r1 = automata.MooreMachineRun(m1)
    r2 = automata.MooreMachineRun(m2)

    # Run the two machines in parallel.  For each state pair reached, record the scores in a list.
    l = []

    # Also, keep a dictionary of state pairs reached, mapping to the index in the list where each was encountered.
    d = dict()
    
    q1 = r1.state()
    q2 = r2.state()

    n = 0

    # Stop when a state pair is reached that is already in the dict, this indicates a loop.
    while (q1, q2) not in d:
        # Until a loop is complete, compute and record the scores and state pairs.
        # ASSIGN s1 and s2 with scores
        if (reward1 == REWARD_MATCH and r1.output() == r2.output()) \
        or (reward1 == REWARD_MISMATCH and r1.output() != r2.output()):
            s1 = 1
        else:
            s1 = 0
        
        if (reward2 == REWARD_MATCH and r1.output() == r2.output()) \
        or (reward2 == REWARD_MISMATCH and r1.output() != r2.output()):
            s2 = 1
        else:
            s2 = 0

        l.append((s1, s2))
        d[(q1,q2)] = n

        # Advance the machines by one step.
        o1 = r1.output()
        r1.step(r2.output())
        r2.step(o1)

        q1 = r1.state()
        q2 = r2.state()

        n += 1

    # Once the loop is detected, total the scores of ONLY THE LOOP, and return the pair of totals.
    t1, t2 = 0, 0
    the_loop = l[d[(q1,q2)]:]
    loop_len = len(the_loop)
    for s1, s2 in the_loop:
        t1 += s1
        t2 += s2
    
    #return (t1, t2)
    return (t1/loop_len, t2/loop_len)


# UNIT TESTING

import unittest as ut

class TestGame(ut.TestCase):
    def test_run_game(self) -> None:
        m1 = automata.CanonicalMooreMachine.from_string("0 1 1\n"
                                                        "0 2 2\n"
                                                        "0 3 3\n"
                                                        "0 4 4\n"
                                                        "1 5 5\n"
                                                        "1 6 6\n"
                                                        "1 3 3")
        m2 = automata.CanonicalMooreMachine.from_string("0 1 1\n"
                                                        "1 2 2\n"
                                                        "1 0 0")
        s1, s2 = run_cooperation(m1, m2)
        self.assertEqual(s1, 7/12)
        self.assertEqual(s2, 7/12)

        s1, s2 = run_competition(m1, m2)
        self.assertEqual(s1, 7/12)
        self.assertEqual(s2, 5/12)

        s1, s2 = run_mismatch_coop(m1, m2)
        self.assertEqual(s1, 5/12)
        self.assertEqual(s2, 5/12)

if __name__ == '__main__':
    ut.main()
