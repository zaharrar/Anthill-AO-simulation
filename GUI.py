from tkinter import *
from Environment import *
from Ant import *
from copy import deepcopy
from Egg import Egg
import threading

ANT_NUMBER = 15
MAP_WIDTH = 50  # Width of map/maze
MAP_HEIGHT = 50  # Height of map/maze
SQUARE_SIZE = 13  # Size of each box in pixels

class GUI():

    def __init__(self, root, environnement, TASK_DICT, steps=None):
        self.root = root
        self.bgg = PhotoImage(file="images/finalbg.gif")

        self.windowframe = Frame(self.root)
        self.windowframe.pack()

        self.bgcanvas = Canvas(self.windowframe,highlightbackground="#552605")
        self.bgcanvas.pack()
        self.bgcanvas.create_image(150,150,image= self.bgg)

        self.mainframe = Frame(self.bgcanvas, bg ="#552605",borderwidth=0,highlightbackground="#552605")
        self.mainframe.pack()

        self.buttonframe = Frame(self.bgcanvas, bg ="#552605",highlightbackground="#552605")
        self.buttonframe.pack()

        color = "#EDC9AF"
        self.cmap = Canvas(self.mainframe,
                        width=MAP_WIDTH * SQUARE_SIZE,
                        height=MAP_HEIGHT * SQUARE_SIZE,
                        bg=color,highlightbackground="#552605")

        self.cmap.grid(row=1, column=1)

        self.flygif = PhotoImage(file="images/fly.gif")  # 20x20pixel gif of fly
        self.larvagif = PhotoImage(file="images/larva.gif")  # 20x20pixel gif of larva
        self.egggif = PhotoImage(file="images/eggs.gif")  # 20x20pixel gif of larva
        self.wallimage = PhotoImage(file="images/wall.gif")  # 20x20pixel gif of larva
        self.background = PhotoImage(file="images/sand.gif")

        self.pause_button = Button(self.buttonframe, text="Pause / Resume", command=self.pause_simulation)
        self.add_ant_button = Button(self.buttonframe, text="Add ant", command=self.adding_ant_event)
        self.add_larva_button = Button(self.buttonframe, text="Add Larva", command=self.adding_larva_event)
        self.add_egg_button = Button(self.buttonframe, text="Add Egg", command=self.adding_egg_event)
        self.add_food_button = Button(self.buttonframe, text="Add Wall", command=self.adding_wall_event)
        self.add_fly_button = Button(self.buttonframe, text="Add Food", command=self.adding_food_event)
        self.speed_up = Button(self.buttonframe, text="Speed Up", command=self.speed_up_simulation)
        self.slow_down = Button(self.buttonframe, text="Slow Down", command=self.slow_down_simulation)
        self.ants_details_button = Button(self.buttonframe, text="ant details", command=self.print_ants_details)

        self.get_stimulus_button = Button(self.buttonframe, text="get_stimulus", command=self.adding_stimulus_event)
        #self.get_stimulus_button.pack(side=LEFT, padx=10, pady= 10)
        self.pause_button.pack(side=LEFT, padx=10, pady= 10)
        self.add_ant_button.pack(side=LEFT, padx=10, pady= 10)
        self.add_larva_button.pack(side=LEFT, padx=10, pady= 10)
        self.add_egg_button.pack(side=LEFT, padx=10, pady= 10)
        self.add_food_button.pack(side=LEFT, padx=10, pady= 10)
        self.add_fly_button.pack(side=LEFT, padx=10, pady= 10)
        self.speed_up.pack(side=LEFT, padx=10, pady= 10)
        self.slow_down.pack(side=LEFT, padx=10, pady= 10)
        #self.ants_details_button.pack(side=LEFT, padx=10, pady=10)

        self.stop_button = Button(self.buttonframe, text="Stop", command=self.stop_simulation)
        self.stop_button.pack(side=LEFT, padx=10, pady= 10)


        self.show_stimuli_box = IntVar()
        self.check_button = Checkbutton(self.buttonframe, text="Show stimuli", variable=self.show_stimuli_box)
        #self.check_button.pack(side=LEFT, padx=10, pady= 10)


        self.antdirectiongifs = {"N" : PhotoImage(file="images/ant_gifs/normal_state/N.gif"),
                                 "NE" :PhotoImage(file="images/ant_gifs/normal_state/NE.gif"),
                                 "E" : PhotoImage(file="images/ant_gifs/normal_state/E.gif") ,
                                 "SE" :PhotoImage(file="images/ant_gifs/normal_state/SE.gif") ,
                                 "S":  PhotoImage(file="images/ant_gifs/normal_state/S.gif"),
                                 "SO" :PhotoImage(file="images/ant_gifs/normal_state/SO.gif") ,
                                 "O" : PhotoImage(file="images/ant_gifs/normal_state/O.gif") ,
                                 "NO" :PhotoImage(file="images/ant_gifs/normal_state/NO.gif") }

        self.ant_carrying_food = {"N" : PhotoImage(file="images/ant_gifs/carry_food/N.gif"),
                                 "NE" :PhotoImage(file="images/ant_gifs/carry_food/NE.gif"),
                                 "E" : PhotoImage(file="images/ant_gifs/carry_food/E.gif") ,
                                 "SE" :PhotoImage(file="images/ant_gifs/carry_food/SE.gif") ,
                                 "S":  PhotoImage(file="images/ant_gifs/carry_food/S.gif"),
                                 "SO" :PhotoImage(file="images/ant_gifs/carry_food/SO.gif") ,
                                 "O" : PhotoImage(file="images/ant_gifs/carry_food/O.gif") ,
                                 "NO" :PhotoImage(file="images/ant_gifs/carry_food/NO.gif") }

        self.ant_carrying_egg = {"N": PhotoImage(file="images/ant_gifs/carry_egg/N.gif"),
                                  "NE": PhotoImage(file="images/ant_gifs/carry_egg/NE.gif"),
                                  "E": PhotoImage(file="images/ant_gifs/carry_egg/E.gif"),
                                  "SE": PhotoImage(file="images/ant_gifs/carry_egg/SE.gif"),
                                  "S": PhotoImage(file="images/ant_gifs/carry_egg/S.gif"),
                                  "SO": PhotoImage(file="images/ant_gifs/carry_egg/SO.gif"),
                                  "O": PhotoImage(file="images/ant_gifs/carry_egg/O.gif"),
                                  "NO": PhotoImage(file="images/ant_gifs/carry_egg/NO.gif")}

        self.ant_carrying_larva = {"N": PhotoImage(file="images/ant_gifs/carry_larva/N.gif"),
                                 "NE": PhotoImage(file="images/ant_gifs/carry_larva/NE.gif"),
                                 "E": PhotoImage(file="images/ant_gifs/carry_larva/E.gif"),
                                 "SE": PhotoImage(file="images/ant_gifs/carry_larva/SE.gif"),
                                 "S": PhotoImage(file="images/ant_gifs/carry_larva/S.gif"),
                                 "SO": PhotoImage(file="images/ant_gifs/carry_larva/SO.gif"),
                                 "O": PhotoImage(file="images/ant_gifs/carry_larva/O.gif"),
                                 "NO": PhotoImage(file="images/ant_gifs/carry_larva/NO.gif")}

        self.stimulidebug = {1: PhotoImage(file="images/ant_stimuli/1.gif") ,
                             2: PhotoImage(file="images/ant_stimuli/2.gif") ,
                             3: PhotoImage(file="images/ant_stimuli/3.gif"),
                             4: PhotoImage(file="images/ant_stimuli/4.gif") ,
                             5: PhotoImage(file="images/ant_stimuli/5.gif") }

        self.fly_gifs =      {1: PhotoImage(file="images/fly_gifs/1.gif") ,
                              2: PhotoImage(file="images/fly_gifs/2.gif") ,
                              3: PhotoImage(file="images/fly_gifs/3.gif"),
                              4: PhotoImage(file="images/fly_gifs/4.gif") ,
                              5: PhotoImage(file="images/fly_gifs/5.gif") }




        self.stimuli_food = {1: PhotoImage(file="images/food_stimuli/1.gif") ,
                             2: PhotoImage(file="images/food_stimuli/2.gif") ,
                             3: PhotoImage(file="images/food_stimuli/3.gif"),
                             4: PhotoImage(file="images/food_stimuli/4.gif") ,
                             5: PhotoImage(file="images/food_stimuli/5.gif") ,
                             6: PhotoImage(file="images/food_stimuli/6.gif"),
                             7: PhotoImage(file="images/food_stimuli/7.gif"),
                             8: PhotoImage(file="images/food_stimuli/8.gif"),
                             9: PhotoImage(file="images/food_stimuli/9.gif"),
                             10: PhotoImage(file="images/food_stimuli/10.gif")}

        self.cmap.pack(expand=YES, fill=BOTH)

        self.env = environnement
        self.TASK_DICT = TASK_DICT
        self.run_simulation(steps)
        self.update_map()
    def stop_simulation(self):
        self.env.stopped = True

    def get_stimulus(self, eventorigin):
        x,y = self.get_pos(eventorigin)
        print(self.env.map[x][y].stimuli)

    def print_ants_details(self):
        for ant in self.env.ants:
            print(ant.position, ant.has_food, ant.current_stimulus)


    def adding_stimulus_event(self):
        self.cmap.bind("<Button 1>", self.get_stimulus)

    def get_pos(self, eventorigin):
        global x, y
        x = eventorigin.x // SQUARE_SIZE
        y = eventorigin.y // SQUARE_SIZE
        print(x,y)
        return (x,y)

    def check_if_wall(self, position):
        return self.env.map[position[0]][position[1]].free_place

    def add_ant(self, eventorigin):
        x,y = self.get_pos(eventorigin)
        if self.check_if_wall((x,y)):
           Ant((x,y), deepcopy(self.TASK_DICT), self.env)

    def add_larva(self, eventorigin):
        x,y = self.get_pos(eventorigin)
        if self.check_if_wall((x,y)):
           Larva((x,y), self.env)

    def add_wall(self, eventorigin):
        x,y = self.get_pos(eventorigin)

        if self.check_if_wall((x, y)):
            self.env.map[x][y] = Place((x,y), False,self.env)


    def add_food(self, eventorigin):
        x,y = self.get_pos(eventorigin)
        if self.check_if_wall((x, y)):
            self.env.add_food((x,y))

    def add_egg(self,eventorigin):
        x, y = self.get_pos(eventorigin)
        if self.check_if_wall((x, y)):
            Egg((x, y), self.env)

    def adding_egg_event(self):
        self.cmap.bind("<Button 1>", self.add_egg)

    def adding_ant_event(self):
        self.cmap.bind("<Button 1>", self.add_ant)

    def adding_larva_event(self):
        self.cmap.bind("<Button 1>", self.add_larva)

    def adding_wall_event(self):
        self.cmap.bind("<Button 1>", self.add_wall)

    def adding_food_event(self):
        self.cmap.bind("<Button 1>", self.add_food)

    def pause_simulation(self):
        self.env.pause_resume_simulation()

    def slow_down_simulation(self):
        self.env.simulation_speed += 0.05

    def speed_up_simulation(self):
        if (self.env.simulation_speed - 0.05) > 0:
            self.env.simulation_speed -= 0.05

    def update_map(self):
        self.cmap.delete("all")
        self.draw_map()
        self.cmap.update()
        self.root.after(0, self.update_map)

    def draw_map(self):
        """

        for row in self.env.map:
            for place in row:
                if self.show_stimuli_box.get():
                    #checkbox
                    for stimuli in place.stimuli:
                        if place.stimuli[stimuli] > 0:
                            try:
                                self.cmap.create_text(place.position[0] * SQUARE_SIZE, place.position[1] * SQUARE_SIZE, fill="blue", font="Times 8 italic bold",
                                                        text=str(place.stimuli[stimuli]))

                            except:
                                pass
                if not place.free_place :
                    self.cmap.create_image(place.position[0] * SQUARE_SIZE, place.position[1] * SQUARE_SIZE, image=self.wallimage,anchor=NW)

                else :

                    for item in place.items:
                        if isinstance(item, Ant):
                            if item.has_food or item.has_dropped_food:
                                self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE, image=self.ant_carrying_food[item.direction])
                            elif item.has_egg:
                                self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE, image=self.ant_carrying_egg[item.direction])
                            elif item.has_larva:
                                self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE, image=self.ant_carrying_larva[item.direction])
                            else :
                                self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE, image=self.antdirectiongifs[item.direction])

                        elif isinstance(item,Larva):
                            self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE, image=self.larvagif)
                        elif isinstance(item,Egg):
                            self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE, image=self.egggif)


                    if place.food_level > 0 :
                        try:
                            self.cmap.create_image(place.position[0] * SQUARE_SIZE, place.position[1] * SQUARE_SIZE, image=self.fly_gifs[place.food_level])
                        except:
                            self.cmap.create_image(place.position[0] * SQUARE_SIZE, place.position[1] * SQUARE_SIZE, image=self.fly_gifs[5])

                    if place.dropped_food >0 :
                        if place.dropped_food>5:
                            self.cmap.create_image(place.position[0] * SQUARE_SIZE, place.position[1] * SQUARE_SIZE,
                                                   image=self.fly_gifs[5])
                        else:
                            self.cmap.create_image(place.position[0] * SQUARE_SIZE, place.position[1] * SQUARE_SIZE, image=self.fly_gifs[place.dropped_food])
        """

        for item in self.env.ants:
            if item.has_food or item.has_dropped_food:
                self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE,
                                       image=self.ant_carrying_food[item.direction])
            elif item.has_egg:
                self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE,
                                       image=self.ant_carrying_egg[item.direction])
            elif item.has_larva:
                self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE,
                                       image=self.ant_carrying_larva[item.direction])
            else:
                self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE,
                                       image=self.antdirectiongifs[item.direction])

        for item in self.env.eggs :
            self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE, image=self.egggif)

        for item in self.env.larvaes:
            self.cmap.create_image(item.position[0] * SQUARE_SIZE, item.position[1] * SQUARE_SIZE, image=self.larvagif)

        for place in self.env.food_places:
            try:
                self.cmap.create_image(place.position[0] * SQUARE_SIZE, place.position[1] * SQUARE_SIZE,
                                       image=self.fly_gifs[place.food_level])
            except:
                self.cmap.create_image(place.position[0] * SQUARE_SIZE, place.position[1] * SQUARE_SIZE,
                                       image=self.fly_gifs[5])

        for place in self.env.dropped_food:
            try :
                if place.dropped_food > 5:
                    self.cmap.create_image(place.position[0] * SQUARE_SIZE, place.position[1] * SQUARE_SIZE,
                                           image=self.fly_gifs[5])
                else:
                    self.cmap.create_image(place.position[0] * SQUARE_SIZE, place.position[1] * SQUARE_SIZE,
                                           image=self.fly_gifs[place.dropped_food])
            except:
                pass
        for place in self.env.walls:
            self.cmap.create_image(place.position[0] * SQUARE_SIZE, place.position[1] * SQUARE_SIZE,
                                   image=self.wallimage, anchor=NW)

    def run_simulation(self, steps):
        thread = threading.Thread(target=self.env.run,args=(steps,))
        thread.start()

