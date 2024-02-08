# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 
# 
# DM Assistant: Initiative Tracker
# Purpose: The Initiative Tracker is intended to allow the DM to input enemies and players data, and display a tracker that is easy to read and update.
#          It will also allow the DM to roll initiative for all players and enemies, and sort the list based on the results.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

import random   # Random Number Generator

class Character():
    def __init__(self, name, initiativeBonus, isPlayer, armorClass):
        self.name = name
        self.initiativeBonus = initiativeBonus
        self.isPlayer = isPlayer
        self.armorClass = armorClass
        self.isIncapacitated = False
        self.totalInitiative = 0

