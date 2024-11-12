# Logbook

This is the place where all the choice for the project will be explained.

## Skeleton

The program, named Simulazoo, will be a python package and will be usable from command line.
The README file contain all the relevant information concerning the installation and usage af the program.

All future decisions have been made assuming that the content of all the stories (#1 to #9) was known from the start.
I am also assuming that Mr. Rodolphe Delord, the director, is the final client of the project
and that I am his only point of contact, as the sole developer of this project.
Therefore, all technical decisions are my responsibility, apart from the specified points of attention,
and only the functional content of the stories will be considered.

## Story 1

In this story, we will focus on creating the basic structure to simulate an enclosure that can contain animals and
plants. We will also need to advance the simulation by one day and display a report on the contents of the enclosure.

Given future needs (carnivorous and herbivorous animals, health points, reproduction, species management, etc.)
and the potential for additional requests (such as omnivorous animals or carnivorous plants),
a separation of living beings into Python classes does not seem suitable.
Instead, using the ECS (Entity Component System) design pattern, widely used in video games, appears much more
appropriate.

For this, we will use the Python library "snecs," which meets our needs and also includes a
serialization/deserialization
feature that will be particularly useful for Story #9, focused on saving.

## Story 2

In this story, we need to add the concept of species as well as dietary habits.
Since the concept of species applies to all living organisms, this property will also be added to plants for the
sake of consistency (this may enable better identification later if needed).
A specific component will be created to represent it.

As for dietary habits, there are many types. For now, only carnivorous (the correct term being zoophage)
and herbivorous (the correct term being phytophage) diets will be considered.
Each dietary habit will be represented by a distinct component.

## Story 3

In this story, we need to manage the animals' meals. This story is not very clear on how the "meal" is chosen:

- Is it selected from all entities in the enclosure (plants and animals, regardless of their species),
  or only from valid entities based on their diet?
- Can an entity both eat and be eaten during the same day?
- Furthermore, what happens if two animals target the same entity for their meal (i.e., can an entity be eaten multiple
  times)?
- What happens if there is no target that meets the eating criteria?

So I made the following choices:

- Entities choose their meal only from all valid options.
- An entity can both eat and be eaten during the same day.
- An entity can be eaten multiple times (after all, a meal can be shared).
- An entity that cannot eat dies.

To do this, we will implement systems.

## Story 4

The concept of a living being was already introduced in Story 3, so we will reuse the component and add
the health points (HP). We will also add a new system to handle the death of entities due to a lack of HP.

Another system for managing plants and animals will also be introduced.

We will also modify the report to display the HP information.

## Story 5

We will modify the report to display the age information.

## Story 6

Regarding the creation of a new plant, during the process, the parent plant loses half of its HP.
It is not specified whether this should be rounded or not.
Here, I have chosen that the total HP of both plants (new and parent) remains the same as before the creation.

It is also not specified when reproduction and division should occur.
The choice has been made to perform them at the same time as the daily life cycle update.
This implies that the newly created entities at that moment will be able to feed and can also be targeted as a meal.
We also assume that only animals that were not just born can reproduce, and we will generate their names randomly.

## Story 7

Empty, so nothing

## Story 8

The concept of software configuration is not very precise.
We will therefore assume that the configuration allows for creating species and associating characteristics with them.

The configuration file will consist of a set of species names, each associated with the components that compose it,
and a list of entity of this species to create with their attributes.

See `config.json` for an example of config file.

## Story 9

For the final story, we will use the serialization/deserialization capabilities of snecs,
making it incompatible to load both a configuration and a save at the same time.


## Story 10

For this story, we will configure Docker for the project to make its usage easier.
A prompt CLI will also be added for a more user-friendly experience.
