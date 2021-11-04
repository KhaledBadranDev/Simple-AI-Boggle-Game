
from util import *


#                                            ****************************************************
# GAME LOGIC => FINDING THE PATH/PATTERN => * "DEPTH FIRST SEARCH" with "BACK TRACKING" ALGORITHM *
############################################ ****************************************************
def is_pattern_valid(grid, text_box, found_path):
    """

    Args:
        grid (Grid): either the main grid or the temporary grid
        text_box (TextBox): the text box where the player/user types the words/characters
        found_path ([tubles]): the valid path as a list of tubles

    Returns:
        boolean: True if the path/pattern is valid. Otherwise, False.
    """
    rows = cols = len(grid.cubes)
    path = [] # temporary path represented by rows and cols indices and stored as a tuple

    # inner function
    # "DEPTH FIRST SEARCH"
    def dfs(index_row, index_col, index_word):
        # if we reached last letter of the word and everything was valid -> return true
        if index_word == len(text_box.text): return True

        # if the player uses the same letter more than once or
        # if the letter doesn't exist in the word or
        # indices out of bounds 
        # ->  return False  
        elif(   index_row < 0 or  index_col < 0 or
                index_row >= rows or  index_col >= cols or
                text_box.text[index_word] != grid.cubes[index_row][index_col].text_str or
                (index_row, index_col) in path
            ):
            found_path.clear() # to remove the old wrong path
            return False

        # now we can add the indices of the cubes to the path
        path.append((index_row, index_col))
        # now we need to check if the cubes are adjoined
        are_adjoined =  ( dfs(index_row+1, index_col, index_word+1) or   # adjoined as a row (right ->)
                          dfs(index_row-1, index_col, index_word+1) or   # adjoined as a row (left <-)
                          dfs(index_row, index_col-1, index_word+1) or   # adjoined as a col (up)
                          dfs(index_row, index_col+1, index_word+1) or   # adjoined as a col (down)
                          dfs(index_row+1, index_col-1, index_word+1) or # adjoined as a diagonal (up right)
                          dfs(index_row-1, index_col-1, index_word+1) or # adjoined as a diagonal (up left)
                          dfs(index_row+1, index_col+1, index_word+1) or # adjoined as a diagonal (down right)
                          dfs(index_row-1, index_col+1, index_word+1)    # adjoined as a diagonal (down left)
                        )
        found_path.append((index_row, index_col)) # just to draw the cubes in different color if they are being guessed
        path.remove((index_row, index_col))
        return are_adjoined
    
    for index_row in range(rows):
        for index_col in range(cols):
            if dfs(index_row, index_col, 0): return True
    return False
#######################################################


def draw_path(grid, path):
    """
    To change the state of the cubes to change the color of the cube if it belong to the valid/correct path
    Args:
        grid (Grid): either the main grid or the temporary grid
        path ([tubles]): the valid path as a list of tubles
    """
    for row in range(len(grid.cubes)):
        for col in range(len(grid.cubes)):
            if (row, col) in path:
                grid.cubes[row][col].is_being_guessed = True
            else:
                grid.cubes[row][col].is_being_guessed = False


def draw_cubes(grid):
    """
    draw the cubes of the grid
    Args:
        grid (Grid): either the main grid or the temporary grid
    """
    for row in grid.cubes:
        for cube in row:
            if cube.is_being_guessed: 
                cube.blit_while_being_guessed(DISPLAY_SCREEN)
            else:
                cube.blit(DISPLAY_SCREEN, black)


def draw_toolbar(main_menu_button, restart_button, show_solution_button=None):
    """draw the toolbar that has the buttons

    Args:
        main_menu_button (Button): button to go to the main menu
        restart_button (Button): button to get a new grid and restart the time and the whole game
        show_solution_button (Button): button to display all the possible words/solutions. Defaults to None.
    """
    mouse_position = pygame.mouse.get_pos() # get the position of the mouse

    if show_solution_button: # for the main grid (the game play)
        pygame.draw.rect(DISPLAY_SCREEN , gray, (0, 0, width, grid_off_set_y) )
        if main_menu_button.is_hovered_over(mouse_position):
            main_menu_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            main_menu_button.blit(DISPLAY_SCREEN, black)
        if show_solution_button.is_hovered_over(mouse_position):
            show_solution_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            show_solution_button.blit(DISPLAY_SCREEN, black)
        if restart_button.is_hovered_over(mouse_position):
            restart_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            restart_button.blit(DISPLAY_SCREEN, black)

    else: # for the displaying solution screen
        pygame.draw.rect(DISPLAY_SCREEN , gray, (grid_off_set_x-8, 0, width, grid_off_set_y) )
        if main_menu_button.is_hovered_over(mouse_position):
            main_menu_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            main_menu_button.blit(DISPLAY_SCREEN, black)
        if restart_button.is_hovered_over(mouse_position):
            restart_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            restart_button.blit(DISPLAY_SCREEN, black)


def draw_player_score(player, tmp_solution_player = None):
    """
    sisplay the score of the player and the computer (best possible score) during the solution screen
    Args:
        player (Player): the player/user
        tmp_solution_player (Player): the computer (Ideal Player). Defaults to None.
    """
    pygame.draw.line(DISPLAY_SCREEN , gray, (0, height-60) , (grid_off_set_x-8, height-60), 4)
    font = pygame.font.Font("freesansbold.ttf", 18)
    rendered_text = font.render("Score = " + str(player.get_score()), True, black)
    DISPLAY_SCREEN.blit(rendered_text, (18, height-40))
     
    if tmp_solution_player:  # for the displaying solution screen
        pygame.draw.line(DISPLAY_SCREEN , gray, (grid_off_set_x, height-60) , (width - tmp_solution_cube_width*4 -4, height-60), 4)
        font = pygame.font.Font("freesansbold.ttf", 18)
        rendered_text = font.render("Best Possible Score = " + str(tmp_solution_player.get_score()), True, black)
        DISPLAY_SCREEN.blit(rendered_text, (grid_off_set_x+10, height-40))


def draw_correctly_guessed_words(grid, player, dictionary, is_for_solution_screen = None):
    """
    display/draw the valid and correctly typed/guessed words.
    Args:
        grid (Grid): either the main grid or the temporary grid
        player (Player): the player/user
        dictionary ([str]): dictionary as a list of strings that has all the words 
        is_for_solution_screen (boolean): True if we are displaying the solution screen. Defaults to None.
    """
    from game_play_window import update_correctly_guessed_words
    
    font = pygame.font.Font("freesansbold.ttf", 20)
    if is_for_solution_screen: # for the displaying solution screen
        rendered_text = font.render("Player Correct Words:", True, black)
        DISPLAY_SCREEN.blit(rendered_text, (10, grid_off_set_y+10))
        font = pygame.font.Font("freesansbold.ttf", 9)
        word_x = 10
        word_y = grid_off_set_y + 40
        for word in player.get_correctly_guessed_words():
            rendered_text = font.render(word, True, black)
            DISPLAY_SCREEN.blit(rendered_text, (word_x, word_y))
            word_y += 15
            if word_y >= height-70:
                word_y = grid_off_set_y  + 40 
                word_x += 60   
    else:
        rendered_text = font.render("Player Correct Words:", True, black)
        DISPLAY_SCREEN.blit(rendered_text, (10, 150))
        update_correctly_guessed_words(grid, player, dictionary)

        font = pygame.font.Font("freesansbold.ttf", 9)
        word_y = 180
        word_x = 10
        for word in player.get_correctly_guessed_words():
            rendered_text = font.render(word, True, black)
            DISPLAY_SCREEN.blit(rendered_text, (word_x, word_y))
            word_y += 15
            if word_y >= height-70:
                word_y = grid_off_set_y  + 30 
                word_x += 60   


def are_all_letter_in_grid(grid, text_box):
    """

    Args:
        grid (Grid): either the main grid or the temporary grid
        text_box (TextBox): the text box where the player/user types the words/characters

    Returns:
        boolean: True if all letters are in the grid. Otherwise, False
    """
    for char in text_box.text:
        found = False
        for row in grid.cubes:
            if found: break
            for cube in row:
                if char == cube.text_str:
                    found = True
                    break
        
        if not found: return False
    return True


def update_score(player, word):
    """
    increase/update the score of the player based on the number of characters of the word and based on the bonus letters as well.
    Args:
        player (Player): the player/user
        word (str): the correctly typed word that has a valid path in the grid.
    """
    points = 0
    if 3 <= len(word) <= 4:    # NO. OF LETTERS	3 or 4 ===> increase score by 1 
        points = 1
    elif len(word) == 5:  # NO. OF LETTERS	3 or 4 ===> increase score by 2
        points = 2
    elif len(word) == 6:  # NO. OF LETTERS	3 or 4 ===> increase score by 3
        points = 3
    elif len(word) == 7:  # NO. OF LETTERS	3 or 4 ===> increase score by 5
        points = 5
    elif len(word) >= 8:  # NO. OF LETTERS	3 or 4 ===> increase score by 11
        points = 11

    for l in bonus_letters:
        if l in word:
            points *= 2

    player.update_score(points)
