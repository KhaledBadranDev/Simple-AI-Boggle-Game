
from util import *


class Button:
    """
    represents a button
    """

    def __init__(self, x, y, width, height, button_color, button_hover_over_color, text_size,  text_color, text_hover_over_color = None, text_str=""):
        """ constructor of Button class

        Args:
            x (int): x-coordinate of start point of the button.
            y (int): y-coordinate of start point of the button.
            width (int): width of the button.
            height (int): height of the button.
            button_color ((R,G,B) tuple): color of the button.
            button_hover_over_color ((R,G,B) tuple): temporary color of the button when the user hovers over it with the mouse.
            text_size (int): size of text
            text_color ((R,G,B) tuple): color of the text inside the button.
            text_hover_over_color ((R,G,B) tuple): temporary color of the text when the user hovers over the button. Default = None.
            text_str (str): text inside the button. Default = "".
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.button_color = button_color
        self.button_hover_over_color = button_hover_over_color

        self.text_size = text_size
        self.text_color = text_color

        if text_hover_over_color:
            self.text_hover_over_color = text_hover_over_color
        else:
            self.text_hover_over_color =  text_color
 
        self.text_str = text_str


    def blit(self, display_screen, outline_color=None):
        """ draw the button on the display_screen/display_window while the player does not hover over it.  

        Args:
            display_screen (pygame.display.set-mode): display_screen/display_window to draw the button on it.
            outline_color  ((R,G,B) tuple): color of the outline-borders of the button
        """
        if outline_color: 
            pygame.draw.rect(display_screen, outline_color, (self.x-3, self.y-3, self.width+6, self.height+6))
        
        pygame.draw.rect(display_screen, self.button_color, (self.x, self.y, self.width, self.height))

        if self.text_str != "": 
            font = pygame.font.Font("freesansbold.ttf", self.text_size)
            text = font.render(self.text_str, True, self.text_color)
            # to center the text in the middle of the button based on the size of the button
            text_position = (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2))
            display_screen.blit(text, text_position)


    def is_hovered_over(self, mouse_position):
        """ check whether the user hovers over the button with the mouse or not. 
        Args:
            mouse_position ((x,y) tuple): position of the mouse on the screen.

        Returns:
            boolean: True if the user hovers over the button with the mouse. False otherwise.
        """
        if self.x < mouse_position[0] < self.x+self.width and self.y < mouse_position[1] < self.y+self.height:
            return True
        return False


    def blit_hovered_over(self, display_screen):
        """ draw the button on the display_screen/display_window, when the user hovers over it with the mouse.

        Args:
            display_screen (pygame.display.set-mode): display_screen/display_window to draw the button on it.
        """
        pygame.draw.rect(display_screen, self.button_hover_over_color, (self.x, self.y, self.width, self.height))

        if self.text_str != "":
            font = pygame.font.Font("freesansbold.ttf", self.text_size)
            text = font.render(self.text_str, True, self.text_hover_over_color)
            # to center the text in the middle of the button based on the size of the button
            text_position = (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2))
            display_screen.blit(text, text_position)


    def is_clicked(self, mouse_position, event):
        """ check whether the user clicks on the button with the left button of the mouse or not. 
        Args:
            event (pygame.event): event of pygame.
            mouse_position ((x,y) tuple): position of the mouse on the screen.

        Returns:
            boolean: True if the user clicks on the button with the left button of the mouse. False otherwise.
        """
        if self.is_hovered_over(mouse_position):
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                return True
        return False


class Cube(Button): 
    """
    Cube represents one cell of the playing grid.
    Cube inherits from the Button class.
    Args:
        Button : The base class
    """
    def __init__(self, x, y, width, height, cube_color, cube_focused_color, text_size, text_color, text_focused_color=None, text_str=''):
        """
        constructor of Cube class
        Args: 
            kindly see the button class
        """
        super().__init__(x, y, width, height, cube_color, cube_focused_color, text_size, text_color, text_focused_color, text_str)
        
        self.is_being_guessed = False
        self.has_bonus = False

    def blit_while_being_guessed(self, display_screen):
        """
        change the color of the cube while the user/player is guessing/typing the character inside this cube
        Args:
            display_screen (pygame.display.set-mode): display_screen/display_window to draw the cube on it.
        """
        super().blit_hovered_over( display_screen)

    def blit(self, display_screen, outline_color=None):
        """
        draw the cube
        Args:
            display_screen (pygame.display.set-mode): display_screen/display_window to draw the cube on it.
            outline_color ((R,G,B) tuple): color of the outline-borders of the button
        """
        super().blit(display_screen, outline_color=outline_color)
        if self.has_bonus:
            if self.width > 80:
                DISPLAY_SCREEN.blit(bonus_big_icon, (self.x+2, self.y+2)) # comparison icon
            else:
                DISPLAY_SCREEN.blit(bonus_small_icon, (self.x+2, self.y+2)) # comparison icon

    # To override and suppress the super().is_hovered_over(......)
    def is_hovered_over(self, mouse_position):
        return None;


    # To override and suppress the super().is_clicked(......)
    def is_clicked(self, mouse_position, event):
        return None;


    # To override and suppress the super().blit_hovered_over(......)
    def blit_hovered_over(self, display_screen):
        return None;


class Grid:
    """
    represents the main/big playing grid of the game.
    """
    def __init__(self):
        """
        constructor of Grid class
        """
        self.cubes = [
            [],
            [],
            [],
            []
        ]
        
        # configuration of the cubes/dice of the playing grid/ playing field
        self.letters = [
            "R", "I", "F", "O", "B", "X", # cube/dice 1 Configuration
            "I", "F", "E", "H", "E", "Y", # cube/dice 2 Configuration
            "D", "E", "N", "O", "W", "S", # cube/dice 3 Configuration
            "U", "T", "O", "K", "N", "D", # cube/dice 4 Configuration
            "H", "M", "S", "R", "A", "O", # cube/dice 5 Configuration
            "L", "U", "P", "E", "T", "S", # cube/dice 6 Configuration
            "A", "C", "I", "T", "O", "A", # cube/dice 7 Configuration
            "Y", "L", "G", "K", "U", "E", # cube/dice 8 Configuration
            "Q", "B", "M", "J", "O", "A", # cube/dice 9 Configuration
            "E", "H", "I", "S", "P", "N", # cube/dice 10 Configuration
            "V", "E", "T", "I", "G", "N", # cube/dice 11 Configuration
            "B", "A", "L", "I", "Y", "T", # cube/dice 12 Configuration
            "E", "Z", "A", "V", "N", "D", # cube/dice 13 Configuration
            "R", "A", "L", "E", "S", "C", # cube/dice 14 Configuration
            "U", "W", "I", "L", "R", "G", # cube/dice 15 Configuration
            "P", "A", "C", "E", "M", "D" # cube/dice 16 Configuration
        ]

        self.__init_grid__()


    def __init_grid__(self):
        """
        initialize the main/big grid
        """
        cube_y = grid_off_set_y
        for row in range(4):
            cube_x = grid_off_set_x
            for column in range(4):
                rand_has_bonus = random.randrange(0, 1000) >= 950 
                cube_to_add = Cube(cube_x, cube_y,cube_length, cube_length, white, orange, 80, black, black, self.get_random_letter())
                cube_to_add.has_bonus = rand_has_bonus
                self.cubes[row].append(cube_to_add)
                cube_x += cube_length
            cube_y += cube_length


    def get_random_letter(self):
        """
        get a random letter from the cubes configurations
        Returns:
            str: random letter from the cubes
        """
        while True:
            repeated = False
            random_letter = self.letters[random.randrange(0, len(self.letters))]
            for row in self.cubes:
                for cube in row:
                    if random_letter == cube.text_str:
                        repeated = True
            if not repeated:
                return random_letter 


class TmpGrid(Grid):
    """
    represents a temporary grid to show all the possible solutions/words.
    TmpGrid inherits from Grid.
    Args:
        Grid : the base class
    """
    def ___init__(self):
        """
        constructor of TmpGrid class
        """
        super().__init__(self)

    def __init_grid__(self):
        """
        override the __init_grid__() method from the base class
        """
        cube_y = grid_off_set_y
        for row in range(4):
            cube_x = width - tmp_solution_cube_width*4 -4
            for column in range(4):
                cube_to_add = Cube(cube_x, cube_y, tmp_solution_cube_width, tmp_solution_cube_height, white, orange, 22, black, black, self.get_random_letter())
                self.cubes[row].append(cube_to_add)
                cube_x += tmp_solution_cube_width
            cube_y += tmp_solution_cube_height
    

class TextBox():
    """
    represents the textbox where the player/user is going to type the letters/word.
    """
    def __init__(self, x, y, width, height, bg_color, outline_color, text_size,  text_color, max_characters):
        """
        constructor of TextBox class
        Args:
            x (int): x-coordinate of start point of the text box.
            y (int): y-coordinate of start point of the text box.
            width (int): width of the text box.
            height (int): height of the text box.
            bg_color ((R,G,B) tuple): color of the text box.
            outline_color ((R,G,B) tuple): color of the border/outline of the text box.
            text_size (int): size of the text inside the text box.
            text_color  ((R,G,B) tuple): color of the text inside the text box.
            max_characters (int): the maximum allowed number of characters inside the text box.
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.outline_color = outline_color
        self.text_size = text_size
        self.text_color = text_color
        self.max_characters = max_characters

        self.font = pygame.font.Font("freesansbold.ttf", self.text_size)
        self.text = "" 
        self.used_characters = 0


    def blit(self, display_screen):
        """
        Draw the text box
        Args:
            display_screen (pygame.display.set-mode): display_screen/display_window.
        """
        pygame.draw.rect(display_screen, self.outline_color, (self.x-5, self.y-5, self.width+10, self.height+10))
        
        pygame.draw.rect(display_screen, self.bg_color, (self.x, self.y, self.width, self.height))

        if self.text != "": 
            rendered_text = self.font.render(self.text, True, self.text_color)
            # to center the text in the middle of the button based on the size of the button
            text_position = (self.x + (self.width/2 - rendered_text.get_width()/2), self.y + (self.height/2 - rendered_text.get_height()/2))
            display_screen.blit(rendered_text, text_position)


    def blit_cursor(self, display_screen):
        """
        draw the cursor of the text_box (that looks like this |)
        Args:
            display_screen (pygame.display.set-mode): display_screen/display_window.
        """
        current_rendered_text = self.font.render(self.text, True, self.text_color)
        rendered_text = self.font.render("|", True, self.text_color)
        # to center the text in the middle of the button based on the size of the button
        text_position = (self.x + (self.width/2 + current_rendered_text.get_width()/2) + 5, self.y + (self.height/2 - rendered_text.get_height()/2))
        display_screen.blit(rendered_text, text_position)

    def blit_number_of_chars(self, display_screen):
        """
        draw the number of character that has been typed and the number of the maximum characters 
        Args:
            display_screen (pygame.display.set-mode): display_screen/display_window.
        """
        font = pygame.font.Font("freesansbold.ttf", self.text_size-5)
        rendered_text = font.render(f"{self.used_characters}/{self.max_characters}", True, gray)
        text_position = (self.x + 15, self.y + self.height+10)
        display_screen.blit(rendered_text, text_position)

    def append_text(self, text):
        """
        append the last typed character to the end of the text box.
        Args:
            text (str): the last typed character
        """
        if len(text) + self.used_characters <= self.max_characters:
            self.text += text
            self.used_characters += len(text)

    def backspace(self):
        """
        delete last typed character
        """
        last_index = len(self.text)-1
        self.text = self.text[0: last_index]
        if self.used_characters > 0:
            self.used_characters -= 1


    def clear_textbox(self):
        """reset the text box
        """
        self.text = ""
        self.used_characters = 0


class Player:
    """
    represents the user/player
    """
    def __init__(self):
        """
        constructor of Player class
        """
        self.start_time = pygame.time.get_ticks()
        self.end_time_in_milli_sec = 3*60*1000 + 60*5 # converting (3 mintues+ 5 second) into milliseconds
                                                    # added 5 seconds more because the computer takes some time to start the game
        self.time_since_start_in_milli_sec = 0
        
        # private fields
        self.__score__ = 0 
        self.__guessed_words__ = []
        self.__correctly_guessed_words__ = []


    def get_score(self):
        return self.__score__

    def get_all_guessed_words(self):
        return self.__guessed_words__

    def get_correctly_guessed_words(self):
        return self.__correctly_guessed_words__
    

    def update_score(self, score):
        self.__score__ += score


    def add_to_guessed_words(self, word):
        self.__guessed_words__.append(word)


    def add_to_correctly_guessed_words(self, word):
        self.__correctly_guessed_words__.append(word)
