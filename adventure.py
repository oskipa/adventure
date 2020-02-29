# Adventure
# A game implementation in python for the osbourn book from the 80s
import os
from collections import deque

class Console:
    def clear(self):
        command = "clear"

        if os.name == "nt":
            command = "cls"

        os.system(command)

class Room:
    def __init__(self, i_d, name, description, objects, edges):
        self.id = i_d
        self.name = name
        self.description = description
        self.objects = objects
        self.edges = edges

    def describe(self, rooms):
        print("You have entered into the " + self.name)
        print(self.description)
        self._directions(rooms)

    def _directions(self,rooms):
        point = 0
        cardinal = ["north", "south", "west", "east"]

        for direction in self.edges:
            if direction is None:
                point += 1
                continue

            print(cardinal[point] + " is the " + rooms[direction].name)
            point += 1

class Player:
    def __init__(self):
        self.points = 0
        self.objects = []
        self.position = 1

class Commands:
    def __init__(self):
        self.cardinal = ["north", "south", "west", "east"]
        self.cardinal_index = { "north" : 0, "south" : 1, "west" : 2, "east" : 3 }

    def move(self, player, direction, room, rooms):
        if direction in self._valid_directions(room):
            player.position = room.edges[self.cardinal_index[direction]]
        else:
            print("You cannot move " + direction)

    def _valid_directions(self, room):
        result = []
    
        for idx, item in enumerate(room.edges):
            if item is not None:
                result.append(self.cardinal[idx])

        return result

    def look(self, room):
        message = "You see "
       
        if len(room.objects) > 0:
            for item in room.objects:
                message = message +  item +  " "
        else:
            message += "nothing"

        print(message)

    def pick(self, player, item, room):
        if item in room.objects:
            room.objects.remove(item)
            player.objects.append(item)
            print("You have picked a " + item)
        else:
            print("There is no " + item + " in this room.")

    def drop(self, player, item, room):
        if item in player.objects:
            player.objects.remove(item)
            room.objects.append(item)
            print("You have dropped a " + item)
        else:
            print("You don't have a  " + item )

    def describe(self, room, rooms):
        room.describe(rooms)

    def inventory(self, player):
        print("You are carrying")

        for item in player.objects:
            print(item)

    def points(self, player):
        print("Score: " + str(player.points))

    def help(self):
        print("'look' to see what is in a room")
        print("'pick [item]' to pick an object found in a room")
        print("'drop [item]' to drop an object found in a room")
        print("'describe' to describe the room")
        print("'inventory' to see what you are carrying")
        print("'points' to see what your score is")
        print("'[direction]' to move in the cardinal direction North, South, East, or West")

class Game:
    def __init__(self, console, commands, rooms):
        self.console = console
        self.commands = commands
        self.rooms = rooms
        self.state = "no game" 
        self.player = Player()

    def tick(self, command):
        self._parse(command)
        print("press h for help") 

    def _current_room(self):
        return self.rooms[self.player.position]

    def _parse(self, user_input):
        expression = deque(user_input.split(" "))
        command = expression.popleft()

        print("the command: " + command + " the state: " + self.state)

        if self.state == "no game":
            self.state = "playing"
            self._intro_screen()
            self.commands.describe(self._current_room(), self.rooms)
        elif self.state == "playing":
            if command == "h":
                self._help()
            if command == "points":
                self.commands.points(self.player)
            elif command == "describe":
                self.commands.describe(self._current_room(), self.rooms)
            elif command == "look":
                self.commands.look(self._current_room())
            elif command == "drop":
                item  = expression.popleft()
                self.commands.drop(self.player, item, self._current_room()) 
            elif command == "pick":
                item  = expression.popleft()
                self.commands.pick(self.player, item, self._current_room()) 
            elif command == "inventory":
                self.commands.inventory(self.player)
            elif command == "move":
                direction  = expression.popleft()
                self._move(direction)
            elif command == "n":
                self._move("north")
            elif command == "s":
                self._move("south")
            elif command == "e":
                self._move("east")
            elif command == "w":
                self._move("west")
            else:
                print("I don't know how to " + command )

    def _move(self, direction):
        self.commands.move(self.player, direction, self._current_room(), self.rooms)
        self.commands.describe(self._current_room(), self.rooms)

    def _clear(self):
        self.console.clear() 

    def _intro_screen(self):
        self._clear();
        
        print("Adventure")
        print("h for help")
        print("q for quit")



    def _help(self):
        self.commands.help()
        print("'q' to quit")

class Adventure:
    def __init__(self, game):
        self.game = game
        self.first_loop = True
   
    def start(self):
        while True:
            user_command = self._read()
            
            if user_command == "q":
                break

            self.game.tick(user_command)
     
    def _read(self):
        result = ""

        if self.first_loop: 
            self.first_loop = False
        else:
            raw_user_input  = input(">")
            result = raw_user_input.lower().strip() 
           
        return result

if __name__ == "__main__":  

    # Here is where we describe and load the map
    # each array has the inputs for a room
    # each room is has the id of its location in the array, which is made 
    # The format is [id, name,  description, objects, edges]
    # edges cover North, South, West, East. if none, 
    data  =  [
                [0, "Game Intro" ,  "Welcome to adventure", ["pen", "woopie cushion"], [1, None, None, None]],
                [1, "Dark corner",  "", [], [None, 9, None, 2 ]],
                [2, "Overgrown garden",  "", ["axe"], [None, None, 1, 3 ]],
                [3, "By large woodpile",  "", [], [None,None, 2, 4 ]],
                [4, "Yard",  "", [], [None, 12, 3, 5 ]],
                [5, "Weedpatch",  "", ["shovel"], [None,None, 4, 6 ]],
                [6, "Forest",  "", [], [None,None, 5, 7 ]],
                [7, "Thick forest",  "", [], [None, 15, 6, 8 ]],
                [8, "Blasted tree",  "", ["rope"], [None, 16, 7, None ]],
                [9, "Corner of house",  "", [], [1, 17, None, None ]],
                [10, "Entrance to kitchen",  "", [], [None,18, None, 11]],
                [11, "Kitchen with grimy cooker",  "", ["matches"], [None,None, 10, 12 ]],
                [12, "Scullery",  "", [], [4,None, 11, None ]],
                [13, "Dusty room",  "", [], [None, 21, None, 14 ]],
                [14, "Rear turret room",  "", ["scroll"], [None,None, 13, None ]],
                [15, "Clearing",  "", [], [7,None, None, 16 ]],
                [16, "Path",  "", [], [8, 24, 15, None ]],
                [17, "Side of house",  "", [], [9, 25, None, None ]],
                [18, "Back hallway",  "", [], [10, 26, None, None ]],
                [19, "Dark alcove",  "", ["bag of coins"], [None, 27, None, 20 ]],
                [20, "Small dark room",  "", [], [None,None, 19, 21 ]],
                [21, "Spiral staircase",  "", [], [13, None, 20, None ]],
                [22, "Wide passage",  "", [], [None, 30, None, 23]],
                [23, "Slippery steps",  "", [], [None,31, 22, None ]],
                [24, "Clifftop",  "", [], [16, 32, None, None ]],
                [25, "Crumbling wall",  "", [], [17,None, None, None ]],
                [26, "Gloomy passage",  "", ["vacuum cleaner"], [18, 34, None, None ]],
                [27, "Pool of light",  "", ["batteries"], [ 19 , 35, None, 28 ]],
                [28, "Vaulted hall",  "", [], [None,None, 27, 29 ]],
                [29, "Hall with locked door",  "", ["statue"], [None,None, 27, 30 ]],
                [30, "Trophy room",  "", [], [22, 38, 29, None ]],
                [31, "Cellar room",  "", [], [23 , 39, None, None ]],
                [32, "Cliff path",  "", [], [24 ,40, None, None ]],
                [33, "Cupboard",  "", ["key"], [None, 41, None, None ]],
                [34, "Front hall",  "", [], [26, 42, None, 35  ]],
                [35, "Sitting room",  "", [], [27, 43, 34, None ]],
                [36, "Secret room",  "", ["book of spells"], [None, 44, None, None ]],
                [37, "Steep Marble Stairs",  "", [], [29, 45, None, None ]],
                [38, "Dinning room",  "", [], [30,None, None, None ]],
                [39, "Deep celar",  "", ["ring"], [31, None, None, None ]],
                [40, "Cliff path",  "", [], [32, 48, None, None ]],
                [41, "Closet",  "", [], [33,None, None, 42 ]],
                [42, "Front lobby",  "", [], [34, None, 41, None ]],
                [43, "Library",  "", ["candlestick"], [35, None , None, 44 ]],
                [44, "Study",  "", ["candle"], [None,None, 43, None ]],
                [45, "Cobwebby room one way",  "", [], [37, 53, None, 46 ]],
                [46, "Cold chamber",  "", [], [None,None, 45, 47 ]],
                [47, "Spooky room",  "", ["painting"], [None, None, 46, None ]],
                [48, "Cliff path my marsh",  "", ["boat"], [40, 56, None, None ]],
                [49, "Verandah",  "", [], [None, 57, None, 50 ]],
                [50, "Front porch",  "", [""], [42, 58, 49, None ]],
                [51, "Front tower",  "", ["goblet"], [None,None, None, 52 ]],
                [52, "Sloping corridor",  "", [], [None,None, 51, 53 ]],
                [53, "Upper gallery",  "", [], [45, None, 52, None ]],
                [54, "Marsh by wall",  "", [], [None, 62, None, None ]],
                [55, "Marsh",  "", [], [None, 63, 54, None ]],
                [56, "Soggy path",  "", [], [48, None, 55, None ]],
                [57, "Twisted railings",  "", [], [49, None, None, 57 ]],
                [58, "Path",  "", [], [50,None, 57, 59 ]],
                [59, "Path by railings",  "", [], [None, None, 58, 60 ]],
                [60, "Beneath tower",  "", [], [None,None, 59, 61]],
                [61, "Debris",  "", ["aerosol can"], [None,None, 60, 62 ]],
                [62, "Fallen brickwork",  "", [], [54, None, 61, 63 ]],
                [63, "Stone arch",  "", [], [55, None, 62, 64 ]],
                [64, "Crumbling clifftop",  "", [], [None,None, 63, None ]],
            ]

    rooms = []
    for record in data:
        id, name, description, objects, edges = record
        room = Room(id, name, description, objects, edges)
        rooms.append(room)

    # This is where the final manual inversion of control happens
    commands = Commands()
    console = Console()
    game = Game(console, commands, rooms)

    action = Adventure(game)
    action.start()
