#!/usr/bin/python3

# Replace RPG starter project with this code when new instructions are live
import random

class Player:
    def __init__(self):
       self.life = 100
       self.moves = ["punch", "kick"] 

    def attack(self, enemy, move, inventory):
        damage = 0
        if('weapon' in inventory):
            damage = 2
        if(move == "punch"):
            damage += random.randint(1, 10)
        elif(move == "kick"):
            damage += random.randint(15, 30)
        enemy.life -= damage 
        print(f"You {move} {enemy.name} for {damage}")

class Enemy:
    def __init__(self, type):
        if(type == "bellsprout"):
            self.name = "bellsprout"
            self.life = 50
            self.moves = ["absorb", "vine whip"] 
        elif(type == "meowth"):
            self.name = "meowth"
            self.life = 80
            self.moves = ["scratch", "fury swipes"]
        elif(type == "charizard"):
            self.name = "charizard"
            self.life = 120
            self.moves = ["flame blast", "flamethrower"]



    def attack(self, player, move, inventory):
        damage = 0
        if 'armor' in inventory:
            damage = -2
        if(self.name == "bellsprout"):
            if(move == "absorb"):
                damage += 10
                self.life += damage 
            elif(move == "vine whip"):
                damage += random.randint(10, 20) 
        elif(self.name == "meowth"):
            if(move == "scratch"):
                damage += random.randint(1, 15)
            elif(move == "fury swipes"):
                damage += random.randint(15, 30)
        elif(self.name == "charizard"):
            if(move == "flame blast"):
                damage += random.randint(35, 50)
            elif(move == "flamethrower"):
                damage += random.randint(20, 30)
        player.life -= damage
        print(f"{self.name} attacked you with {move} for {damage}")
    
    def drop(self, inventory):
        rng = random.randint(1, 2)
        droppedItem = ""
        if(rng == 1):
            droppedItem = "armor"
        elif(rng == 2):
            droppedItem = "weapon"
        inventory.append(droppedItem)
        print(f"{self.name} dropped {droppedItem} in your inventory!!!")


def enterCombat(enemy, player, inventory):
    print(f"You have encountered an {enemy.name}")
    while(True):
        attack = input(f"Available commands:\n{player.moves[0]}\n{player.moves[1]}\n")
        player.attack(enemy, attack, inventory)
        if(enemy.life <= 0):
            break
        randomAttack = random.randint(0, 1)
        enemy.attack(player, enemy.moves[randomAttack], inventory)
        if(player.life <= 0):
            break
        print(f"Player Life: {player.life}\n{enemy.name} Life: {enemy.life}\n")
        print('---------------------------')


def showInstructions():
  #print a main menu and the commands
  print('''
RPG Game
There are only 3 Pokemon left in this world. You gotta beat em all to win!
========
Commands:
  go [direction]
  get [item]
''')



def showStatus():
  #print the player's current status
  print('---------------------------')
  print('You are in the ' + currentRoom)
  #print the current inventory
  print('Inventory : ' + str(inventory))
  #print an item if there is one
  if "item" in rooms[currentRoom]:
    print('You see a ' + rooms[currentRoom]['item'])
  print("---------------------------")

#an inventory, which is initially empty
inventory = []
enemiesLeft = {"bellsprout": True, "meowth": True, "charizard": True}

#player
player = Player()

#a dictionary linking a room to other rooms
## A dictionary linking a room to other rooms
rooms = {

            'Hall' : {
                  'south' : 'Kitchen',
                  'east'  : 'Dining Room',
                  'item'  : 'key'
                },

            'Kitchen' : {
                  'north' : 'Hall',
                  'item'  : 'monster',
                  'combat': 'meowth'
                },
            'Dining Room' : {
                  'west' : 'Hall',
                  'south': 'Garden',
                  'item' : 'potion',
                  'north' : 'Pantry',
               },
            'Garden' : {
                  'north' : 'Dining Room',
                  'combat': 'bellsprout'
               },
            'Pantry' : {
                  'south' : 'Dining Room',
                  'item' : 'cookie',
                  'combat': "charizard"
            }
         }

#start the player in the Hall
currentRoom = 'Hall'

showInstructions()

#loop forever
while True:

  showStatus()
  #get the player's next 'move'
  #.split() breaks it up into an list array
  #eg typing 'go east' would give the list:
  #['go','east']
  move = ''
  while move == '':
    move = input('>')

  # split allows an items to have a space on them
  # get golden key is returned ["get", "golden key"]          
  move = move.lower().split(" ", 1)

  #if they type 'go' first
  if move[0] == 'go':
    #check that they are allowed wherever they want to go
    if move[1] in rooms[currentRoom]:
      #set the current room to the new room
      currentRoom = rooms[currentRoom][move[1]]
    #there is no door (link) to the new room
    else:
        print('You can\'t go that way!')


  #if they type 'get' first
  if move[0] == 'get' :
    #if the room contains an item, and the item is the one they want to get
    if "item" in rooms[currentRoom] and move[1] in rooms[currentRoom]['item']:
      #add the item to their inventory
      inventory += [move[1]]
      #display a helpful message
      print(move[1] + ' got!')
      #delete the item from the room
      del rooms[currentRoom]['item']
    #otherwise, if the item isn't there to get
    else:
      #tell them they can't get it
      print('Can\'t get ' + move[1] + '!')
      
  ## Define how a player can win
  if 'combat' in rooms[currentRoom]:
    enemy = None
    if(currentRoom == "Kitchen" and enemiesLeft['meowth']):
        enemy = Enemy("meowth")    
    elif(currentRoom == "Garden" and enemiesLeft['bellsprout']):
        enemy = Enemy("bellsprout")
    elif(currentRoom == "Pantry" and enemiesLeft['charizard']):
        enemy = Enemy("charizard")
    if(enemy != None):
        enterCombat(enemy, player, inventory)
        if(player.life <= 0):
            print("---------------------------")
            print("You have lost the combat... Game Over!!!")
            print("---------------------------")
            break
        elif(enemy.life <= 0):
            print("---------------------------")
            print(f"You have defeated {enemy.name}")
            enemy.drop(inventory)
            print("---------------------------")
            player.life += 100
            enemiesLeft[enemy.name] = False
    if(not enemiesLeft['bellsprout'] and not enemiesLeft['charizard'] and not enemiesLeft['meowth']):
        print("---------------------------")
        print("\nAll pokemon have been brutally beaten to death.  You Win :(\n\nNo Pokemon were harmed in the making of this game.")
        print("---------------------------")
        break
