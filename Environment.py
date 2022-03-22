# coding: utf-8

from random import shuffle, randint
import time
from Ant import Ant
from Larvae import Larva
from Egg import Egg
from copy import deepcopy


class Place:

    def __init__(self, position, free_place, env):

        self.position = position
        self.env = env
        self.free_place = free_place
        self.current_stimulus = "default" #TODO optimiser si ça ram dans propagate()
        self.stimuli = {stimuli_name : 0 for stimuli_name in self.env.TASK_DICT}
        self.items = []
        self.food_level = 0
        self.dropped_food = 0

        if self.free_place == False :
            self.env.signal_wall(self)

    def propagate(self, sn, ss ):
        for x in range(self.position[0] - ss+1, self.position[0] + ss):
            for y in range(self.position[1] - ss+1, self.position[1] + ss):
                if self.env.size > x >= 0 and self.env.size > y >= 0:
                    current_stimulus = ss - max(abs(self.env.map[x][y].position[0] - self.position[0]),abs(self.env.map[x][y].position[1] - self.position[1]))
                    if self.env.map[x][y].free_place and  current_stimulus > self.env.map[x][y].stimuli[sn]:
                        self.env.map[x][y].current_stimulus = sn
                        self.env.map[x][y].stimuli[sn] = current_stimulus

    def append(self, item):
        self.items.append(item)

    def remove(self, item):
        self.items.remove(item)


    def __str__(self):

        return "0" if self.free_place else "1"


class Environment:

    def __init__(self, filename, TASK_DICT):
        self.TASK_DICT = TASK_DICT
        self.walls = []
        self.map = Environment.build_map(filename, self)
        self.size = len(self.map)
        self.stimuli_queue = []
        self.ants = []
        self.larvaes = []
        self.eggs = []
        self.drop_egg_zone = [self.map[45][6]]
        self.drop_larva_zone = [self.map[45][30]]
        self.drop_food_zone = [self.map[42][37]]
        self.simulation_speed = 0.2
        self.is_paused = True
        self.stopped = False
        self.food_places = []
        self.dropped_food = []



    def run(self, steps=None):

        if steps == None:
            round = 0
            while True and not self.stopped :
                time.sleep(0.05)
                if round % 100 == 0:
                    self.spawn_food()
                if round%150 == 0:
                    if len(self.eggs) < 10:
                        self.spawn_egg()
                round += 1
                while self.is_paused:
                    time.sleep(0.5)

                time.sleep(self.simulation_speed)
                for ant in self.ants:
                    ant.move()
                shuffle(self.ants)

                to_remove = []
                for larva in self.larvaes:
                    if larva.hunger_level == 0:
                        to_remove.append(larva)
                        self.ants.append(Ant(larva.position, deepcopy(self.TASK_DICT), self))
                for larva in to_remove:
                    self.map[larva.position[0]][larva.position[1]].items.remove(larva)
                    self.larvaes.remove(larva)
                to_remove = []
                for egg in self.eggs:
                    if egg.need_cares == 0:
                        to_remove.append(egg)
                        larva = Larva(egg.position, self)
                        self.larvaes.append(larva)
                        self.map[egg.position[0]][egg.position[1]].items.append(larva)
                for egg in to_remove:
                    self.map[egg.position[0]][egg.position[1]].items.remove(egg)
                    self.eggs.remove(egg)

                self.compute_stimuli()
            for ant in self.ants:
                print(ant.activity_dict)
    def spawn_egg(self):

        Egg((randint(17, 26),randint(1, 18)), self)
        Egg((randint(17, 26),randint(1, 18)), self)
        Egg((randint(17, 26),randint(1, 18)), self)
        Egg((randint(17, 26),randint(1, 18)), self)

    def spawn_food(self):
        self.add_food( (randint(51, 56),randint(37, 42)))
        self.add_food( (randint(41, 46),randint(51, 56)))


    def compute_stimuli(self):
        for y in range(self.size):
            for x in range(self.size):
                #clear stimuli
                self.map[y][x].stimuli = {task : 0 for task in self.TASK_DICT}
        #
        # for i in range(len(self.stimuli_queue)):
        #     #object stimuli in queue:
        #     #tuple(position, sn, ss)
        #
        #     self.map[self.stimuli_queue[i][0][0]][self.stimuli_queue[i][0][1]].propagate(self.stimuli_queue[i][1], self.stimuli_queue[i][2] )

        # self.stimuli_queue = []


        for drop_egg_zone in self.drop_egg_zone:
            drop_egg_zone.propagate("drop_egg", 25)

        for drop_egg_zone in self.drop_larva_zone:
            drop_egg_zone.propagate("drop_larva", 25)


        for drop_food_zone in self.drop_food_zone:
            if len(self.dropped_food) <= 5:
                drop_food_zone.propagate("drop_food",40)

        fp_to_remove = []
        for food_place in self.food_places:
            if food_place.food_level != 0:
                if len(self.dropped_food) <= 5 :
                    food_place.propagate("food", 40)
            else:
                fp_to_remove.append(food_place)

        for fp in fp_to_remove:
            self.food_places.remove(fp)

        fp_to_remove = []
        for food_place in self.dropped_food:
            if food_place.dropped_food != 0:
                food_place.propagate("dropped_food", 40)
            else:
                fp_to_remove.append(food_place)

        for fp in fp_to_remove:
            self.dropped_food.remove(fp)

        for larva in self.larvaes:
            if larva.moved:
                self.map[larva.position[0]][larva.position[1]].propagate("hungry_larva", 20)
            else:
                self.map[larva.position[0]][larva.position[1]].propagate("larva", 50)


        for egg in self.eggs:
            if egg.moved:
                self.map[egg.position[0]][egg.position[1]].propagate("care_egg", 20)
            else :
                self.map[egg.position[0]][egg.position[1]].propagate("egg", 50)




    def add_food(self, position):
        self.map[position[0]][position[1]].food_level += 5
        self.food_places.append(self.map[position[0]][position[1]])

    def get_neighborhood(self, position):
        neighborhood = []
        for x in range(position[0]-1, position[0]+2):
            for y in range(position[1]-1, position[1]+2):
                if (x,y) != position and self.size > x  >= 0 and self.size > y >= 0:
                    neighborhood.append(self.map[x][y])
        return neighborhood

    def notify_existence(self, object):
        """ an object notify his existence to the env to update the map"""

        if isinstance(object, Ant):
            self.ants.append(object)

        elif isinstance(object, Larva):
            self.larvaes.append(object)

        elif isinstance(object, Egg):
            self.eggs.append(object)

        self.map[object.position[0]][object.position[1]].append(object)


    # def notify_move(self, ant, old_position, new_position, sn, ss):

        # self.stimuli_queue.append((new_position, sn, ss))
        # self.map[old_position[0]][old_position[1]].remove(ant)
        # self.map[new_position[0]][new_position[1]].append(ant)

    def pause_resume_simulation(self):
        if self.is_paused :
            self.is_paused = False
        else :
            self.is_paused = True

    def signal_wall(self,place):
        self.walls.append(place)

    @staticmethod
    def build_map(filename, env):
        bitmap = Environment.parse_map(filename)
        size = len(bitmap)
        return [[Place((x,y), True, env) if bitmap[x][y] == '0' else Place((x,y), False, env) for y in range(size)] for x in range(size)]

    @staticmethod
    def parse_map(filename):

        map = []
        with open(filename, 'r') as map_file:
            new_line = map_file.readline()

            while new_line:
                map.append(new_line.split(',')[:-1])
                new_line = map_file.readline()
        return map
