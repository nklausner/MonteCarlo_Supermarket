#!/usr/bin/env python3
# coding: utf-8


from doodle_customer import Customer
from doodle_visualisation import SupermarketVisualisation
import numpy as np
from time import sleep


class SupermarketSimulation:
    """markov chain monte carlo simulation of customer movement in a supermarket"""

    def __init__(self, visualisation=None, frame_time=10):
        """
        visualisation: SupermarketVisualisation object
        frame_time: wait time for frame in milliseconds
        the states are:
        (0) entrance, (1) fruit, (2) spices, (3) dairy, (4) drinks, (5) checkout
        """
        self.visualisation = visualisation
        self.frame_time = frame_time
        self.time = 7*3600
        self.closing_time = 21*3600

        self.customers = []
        self.customer_id = 1
        self.states = ['entrance', 'fruit', 'spices', 'dairy', 'drinks', 'checkout', 'inactive']
        self.counts = [0 for i in range(7)]
        self.prob_matrix = [
            [0.0, 0.3774345198119543, 0.18146406984553393, 0.2875755540631296, 0.15352585627938214, 0.0],
            [0.0, 0.5972003774771941, 0.05064485687323057, 0.09586347908147216, 0.05481283422459893, 0.20147845234350426],
            [0.0, 0.09089461954791468, 0.402419611588666, 0.19309137217446673, 0.16300541228907992, 0.15058898439987264],
            [0.0, 0.049803260258572235, 0.051320966835300734, 0.7369870713884205, 0.05851602023608769, 0.10337268128161889],
            [0.0, 0.08789966073815153, 0.08697440115143415, 0.010897501799115862, 0.5985401459854015, 0.21568829032589698],
            [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
        ]
        if visualisation:
            self.pos_matrix = visualisation.pos_matrix
        else:
            self.pos_matrix = []
        self.__print_head()
    

    def add_customers(self):
        """add customers randomly following the poisson distribution"""
        n = np.random.poisson(2) #1.667
        for _ in range(n):
            another_customer = Customer(self.customer_id, self.pos_matrix)
            self.customers.append(another_customer)
            self.customer_id += 1
        return n
    
    
    def simulate_step(self):
        """simulate a time step (minute) with customers making the decision where to go next"""
        self.counts = [0 for i in range(7)]
        self.counts[0] = self.add_customers()
        for c in self.customers:
            if c.is_active:
                c.decide_step(self.prob_matrix, self.pos_matrix)
                self.counts[c.state] += 1
            else:
                self.counts[6] += 1
        self.__print_step()
    

    def move_customers(self):
        for c in self.customers:
            if c.is_active:
                c.move(self.pos_matrix[-1])
    

    def run_time(self):
        """run simulation in a loop until given time or keyboard interrupt"""
        while self.time < self.closing_time:
            if(self.time%60 == 0):
                self.simulate_step()
            if self.visualisation:
                self.move_customers()
                self.visualisation.show_frame(self.frame_time, self.customers)
            else:
                sleep(0.002)
            self.time += 1
    

    def __print_head(self):
        str2 = '  '.join(self.states)
        print("--:--:-- " + str2)


    def __print_step(self):
        """display time and customer distribution in terminal"""
        str1 = self.__get_time_str()
        str2 = ' '.join([f"{x:7}" for x in self.counts])
        print(str1 + " " + str2)


    def __get_time_str(self):
        """display time and customer distribution in terminal"""
        hrs = self.time//3600
        min = self.time%3600//60
        sec = self.time%60
        return f"{hrs:02}:{min:02}:{sec:02}"



if __name__ == '__main__':
    supervis = SupermarketVisualisation("layout.txt", "tiles.png")
    supersim = SupermarketSimulation(supervis, 10)
    supersim.run_time()