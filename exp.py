#!/usr/bin/env python

'''
exp - Main module for the FSM-Ecosystems experiment.

Classes:
    None.

Functions:
    main - receives command line parameter values from the main program, runs an ecosystem and produces output.
'''

__author__ = "Gabor 'Tony' Zoltai"
__copyright__ = "Copyright 2023, Gabor Zoltai"
__credits__ = ["Gabor Zoltai"]
__license__ = "GPL"
__version__ = "0.1"
__maintainer__ = "Tony Zoltai"
__email__ = "tony.zoltai@gmail.com"
__status__ = "Prototype"

import numpy
import logging
import optparse

import EcoSystem
import scenarios

def main(options, args):

    rng = numpy.random.default_rng(options.SEED)

        # Create the named ecosystem scenario

    if options.SCENARIO == "CONTROL":
        eco = scenarios.create_CONTROL(options.POPULATION, rng)
    elif options.SCENARIO == "COMP":
        eco = scenarios.create_COMP(options.POPULATION, rng)
    elif options.SCENARIO == "COOP":
        eco = scenarios.create_COOP(options.POPULATION, rng)
    else:
        raise NotImplementedError("This scenario has not yet been implemented.")

    logging.basicConfig(level=getattr(logging, options.LOGLEVEL.upper()),
                        format="%(asctime)s %(levelname)s: %(message)s")
    logging.info("Start of run")

    print('comment,"Lines start with a type indicator."')
    print('comment,"A header line precedes matching data lines."')
    print('header,"Parameter name","Parameter value"')
    print('parameter,scenario,', options.SCENARIO)
    print('parameter,population,', options.POPULATION)
    print('parameter,generations,', options.GENERATIONS)
    print('parameter,seed,', options.SEED)

    print('header,Generation,Element,"Median complexity","Median states","Median latent states"')

    # Run the EcoSystem for N cycles
    
    for i, g in enumerate(eco.generations()):
        # Log the generation.
        if options.INFOGENS >0 and i % options.INFOGENS == 0:
            logging.info("Generation " + str(i))

        # g is a list of elements
        for j, el in enumerate(g):
            raw_states = [a.state_count() for a in el.individuals]
            complexities = [a.complexity() for a in el.individuals]
            latent_states = [raw_states[i] - complexities[i] for i in range(len(el.individuals))]
            #logging.info(raw_states)
            #logging.info(complexities)
            #logging.info(latent_states)

            print('output,', i, ',', j, ',', numpy.median(complexities), ',', numpy.median(raw_states), ',', numpy.median(latent_states))

        if i >= options.GENERATIONS - 1:
            break

    logging.info("End of run")


if __name__ == "__main__":

    parser = optparse.OptionParser(("Usage: %prog [OPTION]...\n"
                                    "Simulate a scenario of ecosystems of evolving interacting FSM lineages and non-evolving elements."))
    parser.add_option("-l", "--log", choices = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
                    action="store", dest="LOGLEVEL", default="DEBUG",
                    help="set minimum logging level to LOGLEVEL; one of DEBUG, INFO, WARNING, ERROR or CRITICAL (default: %default)")
    parser.add_option("-g", "--generations", type="int", action="store", dest="GENERATIONS", default=2,
                    help="specify the number of generations to run for (default: %default)")
    parser.add_option("-i", "--inform", type="int", action="store", dest="INFOGENS", default=1,
                    help="if not zero, produce a message as a sign of life every INFOGENS generations; ignored if logging level is higher than INFO (default: %default)")
    parser.add_option("-s", "--seed", type="int", action="store", dest="SEED", default=0,
                    help="specifies the starting seed of the random number generator, so runs are repeatable (default: %default)")
    parser.add_option("-p", "--population", type="int", action="store", dest="POPULATION", default=2,
                    help="the number of individuals of each replicator lineage (default: %default)")
    parser.add_option("-e", "--ecoscenario", choices = ("CONTROL", "COMP", "COOP"),
                    action="store", dest="SCENARIO", default="CONTROL",
                    help="run the SCENARIO identified (default: %default)")
    
    (options, args) = parser.parse_args()

    main(options, args)