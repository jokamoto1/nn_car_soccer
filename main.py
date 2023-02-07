from car import Car
from ball import Ball
from goal import Goal
from game import Game
import pygame
import math
import os
import neat
import pickle
import random
from sys import exit

pygame.init()

screen = pygame.display.set_mode((500, 600))
pygame.display.set_caption('Ai Goal')
clock = pygame.time.Clock()

def run(config_file):
    """
    :param config_file: location of config file
    :return: None
    # """
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    # p.add_reporter(neat.Checkpointer(500))

    # Run for up to 50 generations.
    winner = p.run(eval_genomes, 30)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

    # show final stats
    print('\nBest genome:\n{!s}'.format(winner))

def eval_genomes(genomes, config_file):

     for i, (genome_id1, genome1) in enumerate(genomes):
        # print(round(i/len(genomes) * 100), end=" ")
        genome1.fitness = 0
        for genome_id2, genome2 in genomes[min(i+1, len(genomes) - 1):]:
            genome2.fitness = 0 if genome2.fitness == None else genome2.fitness
            game =  Game(screen,clock)
            game.train_ai(genome1, genome2,config_file)
            genome1.fitness += game.top_score -  game.bottom_score
            genome2.fitness += game.bottom_score -  game.top_score
       
run("config-feedforward.txt")



