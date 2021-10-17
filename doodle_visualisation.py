#!/usr/bin/env python3
# coding: utf-8


import numpy as np
import cv2


class SupermarketVisualisation:
    """Visualizes the supermarket background"""

    def __init__(self, file_layout, file_tiles):
        """
        layout  : a string with each character representing a tile
        tiles   : a numpy array containing all the tile images
        """
        # split the layout string into a two dimensional matrix
        with open(file_layout) as f:
            layout = f.read().strip().split("\n")
        
        self.grid = [list(row) for row in layout]
        self.width = len(self.grid[0])
        self.height = len(self.grid)
        h = 32 * self.height
        w = 32 * self.width

        self.tiles = cv2.imread(file_tiles)
        self.ground = np.zeros((h, w, 3), np.uint8)
        self.image = np.zeros((h, w, 3), np.uint8)
        self.prepare_map()
        self.img_ghost = self.extract_tile(8, 2)

        p0 = [[15,13], [15,14]] # entrance
        p1 = [[2+i,13+j] for i in range(8) for j in range(2)] # fruit
        p2 = [[2+i,9+j] for i in range(8) for j in range(2)] # spices
        p3 = [[2+i,5+j] for i in range(8) for j in range(2)] # dairy
        p4 = [[2+i,1+j] for i in range(8) for j in range(2)] # drinks
        p5 = [[13,1+3*i] for i in range(4)] # checkout
        p6 = [[15,1], [15,2]] # exit
        lanes = [1,10,11,14]
        self.pos_matrix = [p0, p1, p2, p3, p4, p5, p6, lanes]

        print('initiate supermarket visualisation')


    def extract_tile(self, row, col):
        """extract a tile array from the tiles image"""
        y = 32 * row
        x = 32 * col
        return self.tiles[y:y+32, x:x+32]


    def get_tile(self, char):
        """returns the array for a given tile character"""
        if char == "#":
            return self.extract_tile(0, 0)
        elif char == "G":
            return self.extract_tile(7, 3)
        elif char == "C":
            return self.extract_tile(2, 8)
        else:
            return self.extract_tile(1, 2)


    def prepare_map(self):
        """prepares the entire image as a big numpy array"""
        for row, line in enumerate(self.grid):
            for col, char in enumerate(line):
                bm = self.get_tile(char)
                y = 32 * row
                x = 32 * col
                self.image[y:y+32, x:x+32] = bm


    def get_frame(self):
        """draws the image into a frame"""
        frame = self.ground.copy()
        frame[0:self.image.shape[0], 0:self.image.shape[1]] = self.image
        return frame
    

    def show_frame(self, frame_time=1000, customers=[]):
        """initiates and shows a frame for a certain time"""
        frame = self.get_frame()
        frame = self.place_customers(frame, customers)
        cv2.imshow("DOODLE supermarket", frame)
        key = cv2.waitKey(frame_time)
        if key == 113:
            self.write_image(frame, "supermarket.png")
            print('save image as supermarket.png')


    def write_image(self, frame, filename):
        """writes the image into a file"""
        cv2.imwrite(filename, frame)
    

    def place_customers(self, frame, customers):
        """places customer objects"""
        for c in customers:
            if c.is_active:
                frame[c.y:c.y+32, c.x:c.x+32] = self.img_ghost
        return frame


if __name__ == "__main__":

    market = SupermarketVisualisation("layout.txt", "tiles.png")

    while True:
        frame = market.get_frame()
        cv2.imshow("frame", frame)

        # https://www.ascii-code.com/
        key = cv2.waitKey(10)
        if key == 113: # 'q' key
            break
    
    cv2.destroyAllWindows()
    market.write_image("supermarket.png")
