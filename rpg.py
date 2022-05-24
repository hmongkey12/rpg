#!/usr/bin/python3

# Replace RPG starter project with this code when new instructions are live
import random

#Player class will contain the attack method to reduce enemy life
class Player:
    #constructor, initializes player health and command list
    def __init__(self):
       self.life = 100
       self.moves = ["punch", "kick"] 

    #The attack method, takes in the enemy so that the enemy life can be reduced, inventory is used
    #to check for armor and weapon which can modify user attack and damage mitagation
    #The move is passed into the method, so the proper attack can be applied
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
    #Some rooms will have a combat key with a pokemon type value
    #That type is used to initialize the pokemon since the pokemon will only appear when the player 
    #enters the room
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


    #Pokemon attack method, similar to the player attack method
    #Damage will be random depending on the attack choosen
    #armor will reduce the attack and will be checked via the inventory
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
    
    #The Loot System, whenever the pokemon is defeated, it will drop a random item
    #and that item will be added automatically to the inventory
    def drop(self, inventory):
        rng = random.randint(1, 2)
        droppedItem = ""
        if(rng == 1):
            droppedItem = "armor"
        elif(rng == 2):
            droppedItem = "weapon"
        inventory.append(droppedItem)
        print(f"{self.name} dropped {droppedItem} in your inventory!!!")


#the combat function that gets triggered whenever the player enters a room that 
#has a "Combat" key in it.  This method will keep looping until either the player or the pokemon have no more life.
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

#this will be used to check for a win condition, after a pokemon is defeated, the value is set to false
#which also prevents the pokemon from appearing again when the player reenters the room
enemiesLeft = {"bellsprout": True, "meowth": True, "charizard": True}

#Instantiate a player object
player = Player()

#a dictionary linking a room to other rooms
## A dictionary linking a room to other rooms
### The combat key is added because it will be used to create a pokemon
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
      
  #If a room has combat in it
  if 'combat' in rooms[currentRoom]:
    enemy = None
    #The Kitchen will have Meowth, Garden will have a bellsprout, and pantry will have a charizard
    if(currentRoom == "Kitchen" and enemiesLeft['meowth']):
        enemy = Enemy("meowth")    
    elif(currentRoom == "Garden" and enemiesLeft['bellsprout']):
        enemy = Enemy("bellsprout")
    elif(currentRoom == "Pantry" and enemiesLeft['charizard']):
        enemy = Enemy("charizard")
    #Will enter combat only if the enemy has been created
    if(enemy != None):
        enterCombat(enemy, player, inventory)
        #losing condition is if the player's life drops below 0
        if(player.life <= 0):
            print("---------------------------")
            print("You have lost the combat... Game Over!!!")
            print("---------------------------")
            break
        #if enemies life drops below 0, end the combat
        elif(enemy.life <= 0):
            print("---------------------------")
            print(f"You have defeated {enemy.name}")
            enemy.drop(inventory)
            print("---------------------------")
            player.life += 100
            enemiesLeft[enemy.name] = False
    #The winning condition is if all pokemon have been defeated 
    if(not enemiesLeft['bellsprout'] and not enemiesLeft['charizard'] and not enemiesLeft['meowth']):
        print("---------------------------")
        print("\nAll pokemon have been brutally beaten to death.  You Win :(\n\nNo Pokemon were harmed in the making of this game.")
        print("---------------------------")
        break
