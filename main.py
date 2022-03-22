# coding: utf-8

from Environment import *
from Ant import *
from copy import deepcopy
from GUI import *

TASK_DICT = {
    # Task(name, stimulus_name, des_behavior, weight, treshold)
    "default": Task("default", "default"),
    "food": Task("seek_food", "food", 1, 3, 0),
    "dropped_food": Task("dropped_food", "dropped_food", 0, 3, 0),
    "drop_food" : Task("drop_food", "drop_food", 0, 2, 0),
    "cocoon": Task("carrying_cocoons", "cocoon", 0, 2, 0),
    "egg": Task("carrying_eggs", "egg", 1, 3, 0),
    "drop_egg" : Task("drop_egg", "drop_egg", 0, 3, 0),
    "care_egg": Task("care_of_eggs", "care_egg", 1, 5, 0),

    "larva": Task("carrying_larvaes", "larva", 1, 3, 0),
    "drop_larva" : Task("drop_larva", "drop_larva", 0, 3, 0),
    "hungry_larva": Task("feeding_of_larvae", "hungry_larva", 1, 5, 0)
}

if __name__ == "__main__":


    env = Environment("map_1520160611.csv", TASK_DICT)

    ant1 = Ant((10 , 10), deepcopy(TASK_DICT), env)

    root = Tk()

    g = GUI(root, env, TASK_DICT)
    root.mainloop()



