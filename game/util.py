
import pygame
import sys
import random
import time
import webbrowser


# Defining important global variables:-
##########################################################
pygame.init()
clock = pygame.time.Clock()

width = 1000   # width of the window/ displaying screen
height = 700   # height of the window/ displaying screen
DISPLAY_SCREEN = pygame.display.set_mode((width, height))
pygame.display.set_caption(" Boggle Game") # title of the window/ displaying screen

grid_off_set_x  = 356 # offset for the x-coordinate of the grid
grid_off_set_y = 56 # offset for the y-coordinate of the grid
grid_height = grid_width = 642 # the main/ big grid is square ==> width = height
cube_length = 160 # A cube is a symmetrical three-dimensional shape -> that means, length = height = width

tmp_solution_cube_width = 80    # width of the temporary screen to display all the possible words/solution
tmp_solution_cube_height = 160  # height of the temporary screen to display all the possible words/solution 

bonus_letters = []  # list of str that stores all the bonus letters

#colors
white = (255, 255, 255) 
black = (0, 0, 0)
gray = (95, 95, 96) 
orange  = (249, 87, 0)  
green_apple  = (114, 203, 59)
beer = (255, 151, 28)
ryb_red = (255, 50, 19)
notes_color = (255, 255, 153)

# loading the images and the icons
intro_img = pygame.image.load("images/boggle_intro.jpg")       
icon_img = pygame.image.load("images/boggle_icon.png")
sand_timer_icon = pygame.image.load("images/sand_timer.png")
comparison_icon = pygame.image.load("images/comparison.png")
bonus_big_icon = pygame.image.load("images/bonus_big.png")
bonus_small_icon = pygame.image.load("images/bonus_small.png")

pygame.display.set_icon(icon_img) # set the icon of the window/ displaying screen
##########################################################
