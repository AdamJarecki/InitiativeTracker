# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# DM Assistant: Initiative Tracker
# Purpose: The Initiative Tracker is intended to allow the DM to input enemies and players data, and display a tracker that is easy to read and update.
#          It will also allow the DM to roll initiative for all players and enemies, and sort the list based on the results.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import random   # Random Number Generator

class Character():
    def __init__(self, name, initiativeBonus, isPlayer):
        self.name = name
        self.initiativeBonus = initiativeBonus
        self.isPlayer = isPlayer
        self.isIncapacitated = False
        self.totalInitiative = 0
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    #
    # Setter and Getter functions
    # 
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    def setName(self, name):
        self.name = name
        
    def setInitiativeBonus(self, bonus):
        self.initiativeBonus = bonus
        
    def setIsPlayer(self, isPlayer):
        self.isPlayer = isPlayer
        
    def setIsIncapacitated(self, isIncapacitated):
        self.isIncapacitated = isIncapacitated
        
    def setTotalInitiative(self, totalInitiative):
        self.totalInitiative = totalInitiative

    def getName(self):
        return self.name
    
    def getInitiativeBonus(self):
        return self.initiativeBonus
    
    def getIsPlayer(self):
        return self.isPlayer
    
    def getIsIncapacitated(self):
        return self.isIncapacitated
    
    def getTotalInitiative(self):
        return self.totalInitiative

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
    #
    # Function to roll initiative for a specific character
    #
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    def rollInitiative(self):
        self.totalInitiative = self.initiativeBonus + random.randint(1,20)
        return self.totalInitiative
    
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
#
# This is the Initiative Tracker Class, which will add characters, roll initiative for 
#      those characters, and then organize the initiative tracker in initiative order
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

class InitiativeTracker:
    def __init__(self):
        self.characters = []

    def addCharacter(self, character):
        self.characters.append(character)

    def rollInitiative(self):
        for character in self.characters:
            character.rollInitiative()
        self.characters.sort(reverse=True, key=lambda x: x.totalInitiative)

    def displayInitiativeOrder(self):
        print("Initiative Order:")
        for i, character in enumerate(self.characters, start=1):
            print(f"{i}. {character.name} - Initiative: {character.totalInitiative}")


