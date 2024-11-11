# Logbook

This is the place where all the choice for the project will be explained.

## Skeleton

The program, named Simulazoo, will be a python package and will be usable from command line.
The README file contain all the relevant information concerning the installation and usage af the program.

All future decisions have been made assuming that the content of all the stories (#1 to #9) was known from the start. 
I am also assuming that Mr. Rodolphe Delord, the director, is the final client of the project 
and that I am  his only point of contact, as the sole developer of this project.
Therefore, all technical decisions are my responsibility, apart from the specified points of attention, 
and only the functional content of the stories will be considered.

## Story 1

In this story, we will focus on creating the basic structure to simulate an enclosure that can contain animals and plants. We will also need to advance the simulation by one day and display a report on the contents of the enclosure.

Given future needs (carnivorous and herbivorous animals, health points, reproduction, species management, etc.) 
and the potential for additional requests (such as omnivorous animals or carnivorous plants), 
a separation of living beings into Python classes does not seem suitable.
Instead, using the ECS (Entity Component System) design pattern, widely used in video games, appears much more appropriate.

For this, we will use the Python library "snecs," which meets our needs and also includes a serialization/deserialization 
feature that will be particularly useful for Story #9, focused on saving.