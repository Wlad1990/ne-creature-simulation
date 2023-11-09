import pygame
import random
from creatures.creature import Creature
from resources.resources import Resource
from world.terrain import Terrain
from numpy import size


class World:
    def __init__(self):
        self.resources = []
        for _ in range(10):
            resource_type = random.choice(list(Resource.TYPES.keys()))
            quantity = random.randint(1, 10)
            regrowth_rate = 1  # Default regrowth rate
            location = (random.randint(0, 10), random.randint(0, 10))
            resource = Resource(resource_type, quantity, regrowth_rate, location)
            self.resources.append(resource)

        for _ in range(10):
            resource_type = random.choice(list(Resource.TYPES.keys()))
            location = (random.randint(0, 100), random.randint(0, 100))
            quantity = random.randint(1, 10)
            resource = Resource(resource_type, quantity, location)
            self.resources.append(resource)

        # Kreaturen erstellen
        tribes = ["Red", "Blue", "Green", "Yellow"]
        for _ in range(num_creatures):
            tribe = random.choice(tribes)
            location = (random.randint(0, size), random.randint(0, size))
            creature = Creature(name=f"{tribe} Creature", tribe=tribe, location=location)
            self.creatures.append(creature)

    def update(self):
        for creature in self.creatures:
            creature.update(self)

    def draw(self, screen):
        for resource in self.resources:
            resource.draw(screen)
        for creature in self.creatures:
            creature.draw(screen)

    def get_resource_at(self, location):
        for resource in self.resources:
            if resource.location == location:
                return resource
        return None

    def move_creature(self, creature, new_location):
        # Check if new location is within bounds
        if 0 <= new_location[0] < self.size and 0 <= new_location[1] < self.size:
            creature.location = new_location

    def update(self):
        # Update each creature
        new_creatures = []
        for creature in self.creatures:
            creature.update(self)

            # Reproduction
            if random.random() < 0.01 and creature.health.is_healthy():
                new_creature = Creature(name=creature.name, tribe=creature.tribe, parent1=creature, parent2=None)
                new_creatures.append(new_creature)
                creature.memory.remember("I have reproduced")

        self.creatures += new_creatures

        # Remove dead creatures
        self.creatures = [creature for creature in self.creatures if creature.is_alive()]

        # Check for resources at creature's location
        resource = self.get_resource_at(creature.location)
        if resource:
            creature.gather(resource)
            for resource in self.resources:
                resource.replenish()
            
            # Update each resource
            for resource in self.resources:
                resource.update(self)

            # Update the day/night cycle
            self.day_night_cycle.update()

