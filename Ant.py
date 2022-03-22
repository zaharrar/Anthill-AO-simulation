from random import randint
from Larvae import Larva
from random import shuffle
from Egg import Egg
from copy import deepcopy


class Task:

    def __init__(self, name, stimuli_name, desactivation_behavior=1, weight=1, treshold=1):
        self.name = name
        self.stimuli_name = stimuli_name
        self.weight = weight
        self.treshold = treshold
        self.activation_behavior = None
        self.desactivation_behavior = desactivation_behavior

    def __str__(self):

        s = self.name+": "
        s += "stimuli_name: " + self.stimuli_name + " "
        s += "weight: " + str(self.weight) + " "
        s += "treshold: " + str(self.treshold) + '\n'
        return s


class Ant:

    directions = {"S": (0, 1), "SE": (1, 1), "E": (1, 0),
                  "NE": (1, -1), "N": (0, -1), "NO": (-1, -1),
                  "O": (-1, 0), "SO": (-1, 1)}


    def __init__(self, position, task_dict, env):

        self.position = position
        self.task_dict = task_dict
        self.current_stimulus = "default"
        self.env = env
        self.env.notify_existence(self)
        self.has_food = False
        self.has_dropped_food = False
        self.has_egg = False
        self.has_larva = False
        self.default_counter = 0
        self.direction = "S"

        self.activity_dict ={
    "default": 0,
    "food": 0,
    "dropped_food": 0,
    "drop_food" : 0,
    "cocoon": 0,
    "egg": 0,
    "drop_egg" : 0,
    "care_egg": 0,
    "larva": 0,
    "drop_larva" : 0,
    "hungry_larva": 0
}


    def move(self):

        # Task(name, activity_level, weight, treshold)
        old_position = self.position
        old_stimulus = self.current_stimulus
        best_neighbhour = None

        neighborhood = self.env.get_neighborhood(self.position)
        shuffle(neighborhood)
        max=0
        tss=1
        tsn="default"
        for neighbour in neighborhood:
            tasks = deepcopy(self.task_dict)


            for stimuli in neighbour.stimuli:
                ttsn = stimuli
                ttss = neighbour.stimuli[stimuli]

                if ttss*self.task_dict[stimuli].weight*self.task_dict[stimuli].desactivation_behavior > max :
                    tsn = ttsn
                    tss = ttss*self.task_dict[stimuli].weight
                    max = tss
                    best_neighbhour = neighbour

        self.current_stimulus = self.task_dict[tsn].stimuli_name
        self.task_dict[tsn].activity_level = tss #here

        if best_neighbhour != None:
            self.default_counter = 0
            self.position = best_neighbhour.position
            self.activity_dict[self.current_stimulus] +=1
            if self.current_stimulus == "food": #LOOKING FOR FOOD CASE
                if best_neighbhour.food_level >= 1:
                    best_neighbhour.food_level -= 1
                    self.has_food = True
                    self.task_dict["food"].desactivation_behavior = 0
                    self.task_dict["egg"].desactivation_behavior = 0
                    self.task_dict["larva"].desactivation_behavior = 0

                    self.task_dict["hungry_larva"].desactivation_behavior = 1
                    self.task_dict["drop_food"].desactivation_behavior = 1
                    self.task_dict["dropped_food"].desactivation_behavior = 0
                    self.update_weight("food")


            elif self.current_stimulus == "hungry_larva":
                if self.has_dropped_food :
                    for item in best_neighbhour.items:
                        if isinstance(item, Larva):
                            if item.hunger_level >= 1 :
                                item.hunger_level -= 1
                                self.has_dropped_food = False
                                self.task_dict["dropped_food"].desactivation_behavior = 1
                                self.task_dict["hungry_larva"].desactivation_behavior = 0
                                self.task_dict["drop_food"].desactivation_behavior = 0
                                self.update_weight("hungry_larva")

                                break

                else:
                    self.task_dict["dropped_food"].desactivation_behavior = 1
                    self.task_dict["hungry_larva"].desactivation_behavior = 0

            elif self.current_stimulus == "care_egg":
                for item in best_neighbhour.items:
                    if isinstance(item, Egg):
                        if item.need_cares >= 1:
                            item.need_cares -= 1
                            break

            elif self.current_stimulus == "egg": #CARRY egg
                egg = None
                for item in best_neighbhour.items:

                    if isinstance(item, Egg):
                        egg = item
                        self.has_egg = True
                        for task in self.task_dict:
                            self.task_dict[task].desactivation_behavior = 0
                        self.task_dict["drop_egg"].desactivation_behavior = 1
                        self.update_weight("egg")

                if egg != None:
                    best_neighbhour.items.remove(egg)
                    self.env.eggs.remove(egg)

            elif self.current_stimulus == "larva": #CARRY larva
                larva = None
                for item in best_neighbhour.items:
                    if isinstance(item, Larva):
                        if item.moved == False:
                            larva = item
                            self.has_larva = True
                            best_neighbhour.items.remove(larva)
                            self.env.larvaes.remove(larva)

                            for task in self.task_dict:
                                self.task_dict[task].desactivation_behavior = 0
                            self.task_dict["drop_larva"].desactivation_behavior = 1
                            self.update_weight("larva")

                if larva != None:
                    try:
                        best_neighbhour.items.remove(larva)
                        self.env.larvaes.remove(larva)
                    except:
                        print("excption")

                    larva.moved = True

            elif self.current_stimulus == "drop_larva":
                if best_neighbhour.stimuli["drop_larva"] > 20 and len(best_neighbhour.items) < 3 :
                    larva = Larva(best_neighbhour.position, self.env)
                    larva.moved = True
                    self.has_larva = False
                    for task in self.task_dict:
                        self.task_dict[task].desactivation_behavior = 1
                    self.task_dict["drop_larva"].desactivation_behavior = 0
                    self.task_dict["drop_food"].desactivation_behavior = 0



            elif self.current_stimulus == "drop_egg":
                if best_neighbhour.stimuli["drop_egg"] > 20 and len(best_neighbhour.items) < 1 :
                    egg = Egg(best_neighbhour.position, self.env)
                    egg.moved = True
                    self.has_egg = False
                    for task in self.task_dict:
                        self.task_dict[task].desactivation_behavior = 1
                    self.task_dict["drop_egg"].desactivation_behavior = 0
                    self.task_dict["drop_food"].desactivation_behavior = 0


            elif self.current_stimulus == "drop_food":
                self.task_dict["care_egg"].desactivation_behavior = 0
                if self.has_food and best_neighbhour.stimuli["drop_food"] > 35 and best_neighbhour.dropped_food < 4 :
                    if 42 > self.position[0] > 38:
                        best_neighbhour.dropped_food += 1
                        self.env.dropped_food.append(best_neighbhour)
                        self.has_food = False
                        for task in self.task_dict:
                            self.task_dict[task].desactivation_behavior = 1
                        self.task_dict["drop_food"].desactivation_behavior = 0
                        self.task_dict["drop_egg"].desactivation_behavior = 0
                        self.task_dict["care_egg"].desactivation_behavior = 1
                        self.update_weight("drop_food")



            elif self.current_stimulus == "dropped_food":
                if best_neighbhour.dropped_food >= 1:
                    best_neighbhour.dropped_food -= 1
                    self.has_dropped_food = True
                    for task in self.task_dict:
                        self.task_dict[task].desactivation_behavior = 0
                    self.task_dict["hungry_larva"].desactivation_behavior = 1
                    self.update_weight("dropped_food")




                    # if self.current_stimulus == "food":  # LOOKING FOR FOOD CASE
                    #     if best_neighbhour.food_level >= 1:
                    #         best_neighbhour.food_level -= 1
                    #         self.has_food = True
                    #         self.task_dict["food"].activity_level = 0
                    #         self.task_dict["food"].desactivation_behavior = 0
                    #         self.task_dict["hungry_larva"].desactivation_behavior = 1
                    #         self.task_dict["drop_food"].desactivation_behavior = 1

        else:
            # if self.has_food:
            #     print("m'encule pas stp")
            sn, ss = "default", 1
            self.default_counter += 1
            if self.default_counter > 20:
                self.reset()
            self.position = self.default(neighborhood)

        # if self.has_food:
        #     print()
        #     print(self.position, self.current_stimulus)
        #     for item in self.task_dict:
        #         print(self.task_dict[item])


        self.update_cardinal_direction(old_position, self.position)
        # self.env.notify_move(self, old_position, self.position, tsn, tss)

        # dans tes fesses Jurgen


    def reset(self):
        self.task_dict = deepcopy(self.env.TASK_DICT)

    def default(self, neighborhood):

        possibilities = [n for n in neighborhood if n.free_place == True]
        return possibilities[randint(0, len(possibilities)-1)].position

    def update_cardinal_direction(self,oldpos, newpos):

        for key in Ant.directions:
            if (oldpos[0] + Ant.directions[key][0] , oldpos[1] + Ant.directions[key][1]) == newpos:
                self.direction = key
                break
    def update_weight(self, sn):
        self.task_dict[sn].weight = self.task_dict[sn].weight * 1.05




