#!//usr/bin/env python

'''Tools to minimise Canonical Finite Automata. Includes Hopcroft's algorithm, 
   as well as a slower, naive method.'''

#TODO:
# - Find a case that does "add Y \ X to W"
# - Refactor as function
# - Create unit tests

#http://i.stanford.edu/pub/cstr/reports/cs/tr/71/190/CS-TR-71-190.pdf

# Example FSM with n^2 minimisation:
#
#       |Input|
# State | 0 1 | Output
#-------+-----+-------
#     1 | 2 1 | 0
#     2 | 3 2 | 0
#     3 | 4 3 | 0
#     4 | 5 4 | 0
#     5 | 6 5 | 0
#     6 | 6 6 | 1
#
# Iteration 0 split: {1,2,3,4,5}, {6}
# Iteration 1: {1,2,3,4}, {5}, {6}
# Iteration 2: {1,2,3}, {4}, {5}, {6}
# Iteration 3: {1,2}, {3}, {4}, {5}, {6}
# Iteration 4: {1}, {2}, {3}, {4}, {5}, {6}
#
#
# Hopcroft rearranges the trainsition table to be the "where from", not the "where to" states:
#
#       | Prev. |
# Next  | St. on|
# State | 0   1 | Output
#-------+-------+-------
#     1 |  -  1 | 0
#     2 |  1  2 | 0
#     3 |  2  3 | 0
#     4 |  3  4 | 0
#     5 |  4  5 | 0
#     6 | 5,6 6 | 1
#
# Iteration 0 split: {1,2,3,4,5}, {6}
# Iteration 1: {1,2,3,4}, {5}, {6}
# Iteration 2:

# ALGORITHM:
# Let A = (S,I,delta,F) be a finite automaton where S is a finite set of states, I is a finite set of inputs, 6 is a mapping from S x I into S and F c S is the set of final states.
# No initial state is specified since it is of no importance in what follows.
# The mapping delta is extended to SxI* in the usual manner where I* denotes the set of all finite length strings of symbols from I.
# States s and t are * said to be equivalent if for each x in I , delta(s,x) is in F if and only if delta(t,x) is in F.
# The algorithm for finding the equivalence classes of S is described below.
# Step 1. For all s in S and a in I, construct invdelta(s,a) = {t | delta(t,a) = s}.
# Step 2. Construct B(1) = F , B(2) = S-F and for each a in I and 1 <= i <= 2 construct a(i) = {s | s in B(i) and invdelta(s,a) # {}}.
# Step 3. Set k=3
# Step 4. For all a in I construct L(a) = (if |a(1)| <= |a(2)| then {1} else {2}).
# Step 5. Select a in I and i in L(a) . The algorithm terminates when L(a) = $ for each a in I .

# Step 6. Delete i from L(a) . Step 7. Vj < k st 3% in B(j) with s(t,a) es(i) perform steps 7a, 7b,a7c, and 7d. Step 7a. Partition B(j) into B'(j) = {tls(t,a) e&(i)] and B"(j) = B(j)-B'(j) . 7b. Step Replace B(j) by B'(j) and construct B(k) = B"(j) . Construct corresponding a(j) and a(k) for each a in I .7 c . Step TagI modify L(a) as follows. L(a) U Cjl L(a) = if j{L(a) and 0 < la(j)1 _< la(k)\ L(a) U ikj otherwise Step 7d. Set k = k+l . 8 . Step Return to Step 5.


from automata import *

def ReachableStatesFrom(M: CanonicalMooreMachine, q):
  '''Return the subset of states of A that are reachable from the state q.'''

  #the set of all states that have not yet been reached
  S = set(M.states())
  #the set of all states that HAVE been reached
  R = set()
  #the set of states to be added to R in this cycle
  A = {q}

  #stop when no new states have been reached in the current cycle of one-step extension
  while A:
    #Add the newly reached states to R
    R = R | A
    #and subtract them from S
    S = S - A

    #create the next set to be added: all the states reachable from the prior cycle's states in one step
    An = set()
    for a in M.inputs():
      for s in A:
        An.add(M.next_state(s, a))
    #states already in R don't need to be added again
    A = An - R
  return R

def Hopcroft_minimised(A: CanonicalMooreMachine):
  #TODO: exhaustive testing?
  '''Return the minimised form of the CanonicalMooreMachine A.  Generalised from Hopcroft 1971, as presented by Xu 2009.'''

  # Yu's paper, re-presenting Hopcroft's algorithm:
  # https://www.irif.fr/~carton/Enseignement/Complexite/ENS/Redaction/2008-2009/yingjie.xu.pdf

  #Remove unreachable states.

  #Q = frozenset(A.states())
  #F = frozenset(q for q in Q if A.output(q) == 1)

  Q = ReachableStatesFrom(A, A.starting_state())

  Sigma = frozenset(A.inputs())
  delta = A.next_state
  #1: W ← {F,Q−F}
  #Generalise this to Moore Machines:  initial partitioning is by output
  #W = {F, Q - F}
  partition = dict()
  for q in Q:
    o = A.output(q)
    if not(o in partition):
      partition[o] = {q}
    else:
      partition[o].add(q)
  W = {frozenset(partition[o]) for o in partition}

  #2: P ← {F,Q−F}
  #P = {F, Q - F}
  P = {frozenset(partition[o]) for o in partition}

  #3: while W is not empty do
  while W:
    #4:   select and remove S from W]
    S = W.pop()

    #5:   for all a ∈ Σ do
    for a in Sigma:
      #6:     l_a ← δ^−1(S,a)
      l_a = frozenset(q for q in Q if delta(q,a) in S)

      #7:     for all R in P such that R ∩ l_a != ∅ and R̸⊆l_a do
      for R in P:
        if (R & l_a) and (R - l_a):
          #8:       partition R into R_1 and R_2: R_1 ← R ∩ l_a and R_2 ← R − R1
          R1 = R & l_a
          R2 = R - R1

          #9:       replace R in P with R_1 and R_2
          P = (P - {R}) | {R1, R2}

          #10:      if R ∈ W then
          if R in W:
            #11:        replace R in W with R_1 and R_2
            W = (W - {R}) | {R1, R2}

          #12:      else
          else:
            #13:        if |R1| ≤ |R2| then
            if len(R1) >= len(R2):
              #14:          add R_1 to W
              W.add(R1)
            #15:        else
            else:
              #16:          add R_2 to W
              W.add(R2)
            #17:        endif
          #18:      endif
      #19:    endfor
    #20:  endfor
  #21:endwhile
  #print("Partitioned:", P)

  #Construct the minimised Moore Machine from the partitioning
  #Firstly, create a dictionary to map old states to new states
  d = dict()

  #Construct a list of the partitioned sets in order of their lowest member
  ord = sorted([sorted(s) for s in P])

  #Add the replacement state to the dictionary with the key being the original state.
  for n, s in enumerate(ord):
      for st in s:
        d[st] = n

  #Create the minimised Moore Machine
  m = CanonicalMooreMachine(len(P),A.input_count(),A.output_count())
  for n, s in enumerate(ord):
    m.set_output(n, A.output(ord[n][0]))
    for a in Sigma:
      m.set_arc(n, a, d[A.next_state(s[0],a)])

  return m


# Unit testing code
import unittest as ut

def different_for_n(a: MooreMachineRun, b: MooreMachineRun, n, prefix):
  '''Compare two MooreMachineRuns for all strings up to n more symbols after given prefix.'''
  a_state = a.state()
  b_state = b.state()
  alphabet = a._machine.inputs()
  
  if n != 0:
    for c in alphabet:
      a.move_to(a_state)
      b.move_to(b_state)
      a.step(c)
      b.step(c)
      if a.output() != b.output():
        return prefix + [c]
      else:
        d = different_for_n(a, b, n - 1, prefix + [c])
        if d is not None:
          return d

  # if we get here, the two MooreMachineRuns are equivalent for all strings of n symbols
  return None



class TestHopcroft(ut.TestCase):

  #Two Canonical Moore Machines can only be equivalent if the highest-numbered input that is mapped to at least one non-self-loop arc is the same for both.
  # (i.e. if their actually used alphabets are the same)
  #We can (a bit lazily) just test pretending that they both use the same alphabet (with self-loops for the automaton with a smaller alphabet).
  #The aggregate of two CMMs with N and M states will loop in at most NM - 1 steps.
  # Prove that if a state in a DFA with N states is not reachable in N - 1 steps, then it is not reachable at all.
  # a. Let D = (Q,S,D,F,q0) be a DFA.
  # b. Let N = |Q| be the cardinality of Q, i.e. the number of states of D.
  # c. All strings of N or more symbols must pass through a state more than once.
  # d. Therefore, all states reachable by a string of N or more symbols must also be reachable by a shorter string (by removing a looping substring).
  # e. Therefore, a state that is not reachable by a string of at most N - 1 symbols is also not reachable by any longer string, Q.E.D.

  # It follows that a test run of all strings from the input alphabet up to length N - 1 will reach all reachable states.
  # Applying this to the compound automaton of two automata running in parallel on the same input:
  # If one automaton has N reachable states and the other M reachable states, then test-running all strings up to length NM-1 will reach all states.
  # Therefore, by running such a test, we can establish if two automata are equivalent.


  def test_different_for_n(self):
    # Each line of the automaton string is a state, starting from state 0 (implicit).
    # Format of each line has the output of the state, then ALL of its transitions, starting from symbol 0:
    # output on_0 on_1 on_2...
    cfa_string = ("0 0 1 5\n"
                  "1 0 6 2\n"
                  "2 1 0 2\n"
                  "3 0 2 6\n"
                  "4 0 7 5\n"
                  "3 0 2 6\n"
                  "6 0 6 4\n"
                  "7 0 6 2\n")
    alpha = MooreMachineRun(CanonicalMooreMachine.from_string(cfa_string))
    beta = MooreMachineRun(CanonicalMooreMachine.from_string(cfa_string))

    #expecting that this automaton's two copies differ for NO strings up to N.
    self.assertIs(different_for_n(alpha, beta, 8, []), None)



  def test_One(self):
    Q = frozenset(range(6))
    Sigma = frozenset(range(2))
    delta = [[1, 2], [0, 3], [4, 5], [4, 5], [4, 5], [5, 5]]
    q0 = 0
    F = frozenset({2, 3, 4})

    semiaut = CanonicalMooreMachine()

    for state, trans in enumerate(delta):
      for input, next in enumerate(trans):
        semiaut.set_arc(state, input, next)

    for state in F:
      semiaut.set_output(state, 1)

    # util.pit(naive_minimisation(semiaut))

    h = Hopcroft_minimised(semiaut)
    print("Test one - original")
    print(semiaut)
    print("Test one - minimised")
    print(h)
    r1 = MooreMachineRun(semiaut)
    r2 = MooreMachineRun(h)
    self.assertIs(different_for_n(r1, r2, semiaut.state_count() * h.state_count(), []), None)
    print()

  def test_Two(self):
    cfa_string = ("0 0 1 5\n"
                  "1 0 6 2\n"
                  "2 1 0 2\n"
                  "3 0 2 6\n"
                  "4 0 7 5\n"
                  "3 0 2 6\n"
                  "6 0 6 4\n"
                  "7 0 6 2\n")
    cfa = CanonicalMooreMachine.from_string(cfa_string)
    # util.pit(naive_minimisation(cfa))

    h = Hopcroft_minimised(cfa)
    print("Test two - original")
    print(cfa)
    print("Test two - minimised")
    print(h)
    r1 = MooreMachineRun(cfa)
    r2 = MooreMachineRun(h)
    self.assertIs(different_for_n(r1, r2, 12, []), None)
    print()

  def test_Three(self):
    cfa_string = ("0 1 0\n"
                  "0 2 1\n"
                  "0 3 2\n"
                  "0 4 3\n"
                  "0 5 4\n"
                  "1 5 5\n")
    cfa = CanonicalMooreMachine.from_string(cfa_string)
    h = Hopcroft_minimised(cfa)
    print("Test three - original")
    print(cfa)
    print("Test three - minimised")
    print(h)
    r1 = MooreMachineRun(cfa)
    r2 = MooreMachineRun(h)
    self.assertIs(different_for_n(r1, r2, 18, []), None)
    print()

  def test_Four(self):
    cfa_string = ("0 1 0\n"
                  "0 2 1\n"
                  "0 3 2\n"
                  "0 4 3\n"
                  "0 5 4\n"
                  "1 5 5\n")
    cfa = CanonicalMooreMachine.from_string(cfa_string)

    cfa_string2 = ("0 1 0\n"
                   "0 2 1\n"
                   "0 3 2\n"
                   "0 4 5\n"
                   "0 5 4\n"
                   "1 5 5\n")
    cfa2 = CanonicalMooreMachine.from_string(cfa_string2)
   
    print("Test four - first")
    print(cfa)
    print("Test four - second")
    print(cfa2)
    r1 = MooreMachineRun(cfa)
    r2 = MooreMachineRun(cfa2)
    self.assertEqual(different_for_n(r1, r2, 18, []), [0, 0, 0, 1])
    print()

if __name__ == '__main__':
  ut.main()