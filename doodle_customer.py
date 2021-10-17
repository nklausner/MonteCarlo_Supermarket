#!/usr/bin/env python3
# coding: utf-8


from random import choices
import numpy as np


class Customer:
    """customer taking part in supermarket simulation"""

    def __init__(self, id, pos_matrix=[]):
        self.id = id
        self.state = 0 #entrance
        self.x = 0
        self.y = 0
        self.xn = 0
        self.yn = 0
        if pos_matrix:
            self.x, self.y = self.__get_random_pos(pos_matrix[0])
        self.speed = 16
        self.is_active = True


    def decide_step(self, prob_matrix, pos_matrix=[]):
        """decides per random choice and probability matrix, where to go next"""
        if self.state == 5: #checkout
            self.is_active = False
        else:
            s = choices([0, 1, 2, 3, 4, 5], prob_matrix[self.state])[0]
            if self.state != s:
                self.state = s
                if pos_matrix:
                    self.xn, self.yn = self.__get_random_pos(pos_matrix[s])
    

    def move(self, crosslist):
        """moves the customer if current location is not the destination"""
        dy = self.yn - self.y
        dx = self.xn - self.x

        if dx:
            # move y to cross connection to change x coordinate
            dycross = self.__choose_y_cross_connection(crosslist) - self.y
            if dycross != 0:
                dymove = min(self.speed, abs(dycross))
                self.y += np.sign(dycross) * dymove
            else:
                dxmove = min(self.speed, abs(dx))
                self.x += np.sign(dx) * dxmove
        elif dy:
            dymove = min(self.speed, abs(dy))
            self.y += np.sign(dy) * dymove
        else:
            # no positional difference, reached destination
            return
    

    def __choose_y_cross_connection(self, crosslist):
        """choose the y_coordinate of the next cross connection"""
        if self.state < 5:
            dy0 = abs(self.y - 32 * crosslist[0])
            dy1 = abs(self.y - 32 * crosslist[1])
            if dy0 < dy1:
                return 32 * crosslist[0]
            else:
                return 32 * crosslist[1]
        elif self.state == 5:
            return 32 * crosslist[2]
        else:
            return 32 * crosslist[3]


    def __get_random_pos(self, pos_list):
        """chooses random position of list"""
        p = choices(pos_list)[0]
        return 32 * p[1], 32 * p[0]
