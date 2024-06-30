#!/usr/bin/env python

'''
exp - Main module for the FSM-Ecosystems experiment.

Classes:
    None.

Functions:
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

def main(options, args):

    numpy.random.seed(options.SEED)

    logging.basicConfig(level=getattr(logging, options.LOGLEVEL.upper()),
                        format="%(asctime)s %(levelname)s: %(message)s")
    logging.info("Start of run")


    # TODO Output the run parameters?
    

    # Run the EcoSystem for N cycles
    
    for i, g in enumerate(EcoSystem.EcoSystem()):
        # TODO Generate output from the data g passed back by EcoSystem.

        # Log the generation.
        if options.INFOGENS >0 and i % options.INFOGENS == 0:
            logging.info("Generation " + str(i))
        if i >= options.GENERATIONS:
            break

    logging.info("End of run")


if __name__ == "__main__":

    parser = optparse.OptionParser(("Usage: %prog [OPTION]...\n"
                                    "Simulate ecosystems of evolving interacting FSM lineages and non-evolving elements."))
    parser.add_option("-l", "--log", choices = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"),
                    action="store", dest="LOGLEVEL", default="DEBUG",
                    help="set minimum logging level to LOGLEVEL; one of DEBUG, INFO, WARNING, ERROR or CRITICAL (default: %default)")
    parser.add_option("-g", "--generations", type="int", action="store", dest="GENERATIONS", default=1000,
                    help="specify the number of generations to run for (default: %default)")
    parser.add_option("-i", "--inform", type="int", action="store", dest="INFOGENS", default=10,
                    help="if not zero, produce a message as a sign of life every INFOGENS generations; ignored if logging level is higher than INFO (default: %default)")
    parser.add_option("-s", "--seed", type="int", action="store", dest="SEED", default=0,
                    help="specifies the starting seed of the random number generator, so runs are repeatable (default: %default)")

    (options, args) = parser.parse_args()

    main(options, args)