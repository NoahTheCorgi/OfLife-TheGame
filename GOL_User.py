# import arcade
# import os, sys, time #, random, math
from different_world_physics import *

""" The user currently is the most basic cell that affects other cells but is not affected """
""" As the project became more interested in different world physics, this portion is kept simple for now ... """

# A User that interacts with the world of game of life,,,
# The player is made of cells but the cells behave slighly differently than normal cells,,,
# Important: property of user is that they affect the logic but is affected only by it's own cells,,,


class User:
    def __init__(self):

        self.color = (0, 255, 0)
        self.decoration = None  # for now,,,

        # for now user is just a breathing cell
        self.shape_location = [
            [int(n / 2), int(n / 2)]
        ]  # [[int(n/2 - 1), int(n/2)], [int(n/2), int(n/2)], [int(n/2 + 1), int(n/2)]]

        # will need to update this and use it if user becomes more than a green cell
        """ note: self.center is either a whole number or a half a whole number """
        self.center = [int(n / 2), int(n / 2)]

        """ very important to update these """
        """ by calling update_most_type_locations whenever shape_location changes """
        self.most_right = None  # the indexed x location of the most right cell
        self.most_left = None  # the indexed x location of the most left cell
        self.most_top = None  # the indexed y location of the most top cell
        self.most_bottom = None  # the indexed y location of the most bottom cell

        self.life = 10  # if a cell of user would disappear, deduct from life instead
        self.energy = 100  # future: every move or action costs energy

    def update_most_type_locations(self):
        self.most_right = 0
        self.most_left = n - 1
        self.most_top = 0
        self.most_bottom = n - 1
        for i in range(0, len(self.shape_location)):
            if self.shape_location[i][0] > self.most_right:
                self.most_right = self.shape_location[i][0]
            if self.shape_location[i][0] < self.most_left:
                self.most_left = self.shape_location[i][0]
            if self.shape_location[i][1] > self.most_top:
                self.most_top = self.shape_location[i][1]
            if self.shape_location[i][1] < self.most_bottom:
                self.most_bottom = self.shape_location[i][1]
        self.center[0] = self.most_right + self.most_left
        self.center[1] = self.most_top + self.most_bottom

    # future tasks outline:

    # def createAdjacentCell(self): # costs One Energy point
    # 	pass

    # def pauseTheWorld(self): # costs 1000 energy point
    # 	pass

    # def metamorph(self, objectName): # costs 500 energy point just to become a Glider,,,
    # 	pass

    # def eatEntropy(self): # costs nothing
    # 	pass

    # def detectEntropyAroundSelf(self): # costs nothing #this is the AI part,,,
    # 	pass

    # def createObject(self, objectName): # costs A LOT of energy to make happen
    # 	objectList = [["Block", "celldataForBlock", "energyCostForBlock"], ["Beehive", "", ""],
    # 					["Loaf", "", ""], ["Boat", "", ""], ["Tub", "", ""],
    # 					["Blinker", "", ""], # this is the same as the default user shape for now,,,
    # 					["Toad", "", ""], ["Beacon", "", ""], ["Pulsar", "", ""], ["Pentadecathlon", "", ""],
    # 					["Glider", "", ""], ["LightWeightSpaceship", "", ""],
    # 					["MiddleWeightSpaceship", "", ""], ["HeavyWeightSpaceship", "", ""]]
    # 	pass
