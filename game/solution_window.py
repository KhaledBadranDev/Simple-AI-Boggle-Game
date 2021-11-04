
from models import *
from mutual import *
from boggle_game import introduction


def show_best_solution(grid, player, dictionary, enter_button, main_menu_button):
    """
    display all the valid, possible words/solutions
    Args:
        grid (Grid): the main grid 
        player (Player): The Player/user
        dictionary ([str]): dictionary as a list of strings that has all the words 
        enter_button (Button): button to enter/save the typed word in the text box
        main_menu_button (Button): button to go to the main menu
    """
    tmp_solution_grid = TmpGrid()  # temporary small grid so that there would be enough space to show all the possible words
    tmp_solution_player = Player() # the computer (the ideal player that can get all the possible words) 


    play_again_button = Button(width-130-6, 6, 130, grid_off_set_y-15, beer, orange, 16, black, white, "Play Again")
    
    possible_words_buttons = [] # buttons to display the pathes of the possible words when the player hovers over them.
    possible_words_pathes = []  # all the valid pathes for all the possible words stored as tubles.

    # Iterating over the 2 grids at the same time to copy the letters in the main grid and paste it in the temporary grid
    for row1, row2 in zip(tmp_solution_grid.cubes, grid.cubes):
        for cube1,cube2 in zip(row1, row2):
            cube1.text_str = cube2.text_str
            cube1.has_bonus = cube2.has_bonus

    # get all the possible words and their pathes.
    check_all_possible_valid_words(tmp_solution_grid, tmp_solution_player, dictionary, possible_words_buttons, possible_words_pathes)


    while True:
        DISPLAY_SCREEN.fill(gray)
        
        reset_cubes(tmp_solution_grid)
        draw_toolbar(main_menu_button, play_again_button)
        draw_tmp_paper_screen()
        draw_solution_screen(tmp_solution_player)
        draw_player_score(player, tmp_solution_player)
        draw_correctly_guessed_words(grid, player, dictionary, True)
        draw_possible_words_buttons(possible_words_buttons)

        manage_events_for_solution_screen(tmp_solution_grid, main_menu_button, play_again_button, possible_words_buttons, possible_words_pathes)

        draw_cubes(tmp_solution_grid)

        # grid external borders
        pygame.draw.rect(DISPLAY_SCREEN , black, (grid_off_set_x-2, grid_off_set_y-2, grid_width, grid_height), 6)
        pygame.draw.line(DISPLAY_SCREEN , black, (grid_off_set_x + grid_width/2-5, grid_off_set_y) , (grid_off_set_x + grid_width/2-5, grid_height+grid_off_set_y), 6)

        pygame.display.update()


def check_all_possible_valid_words(tmp_solution_grid, tmp_solution_player, dictionary, possible_words_buttons, possible_words_pathes):
    """
    get all the possible words and their pathes.
    Args:
        tmp_solution_grid (Grid): small temporary grid for the solution screen
        tmp_solution_player (Player): computer/ Ideal player
        dictionary ([str]): dictionary as a list of strings that has all the words 
        possible_words_buttons ([Button]): list of buttons to display the pathes of the possible words when the player hovers over them.
        possible_words_pathes ([tuble]): list of all the valid pathes stored as tubles 
    """
    tmp_invisible_textbox = TextBox(14, grid_off_set_y+4, grid_off_set_x-100, 50, notes_color, gray , 16, black, 16)
    
    # inner function
    # bind/connect the words and the buttons together. 
    def bind_words_with_their_buttons():
        word_x = grid_off_set_x + 10
        word_y = grid_off_set_y + 40
        for word in tmp_solution_player.get_correctly_guessed_words():
            tmp_btn = Button(word_x, word_y, 55, 12, orange, beer, 9, black, black, word)
            possible_words_buttons.append(tmp_btn)
            word_y += 15
            if word_y >= height-70:
                word_y = grid_off_set_y  + 40 
                word_x += 60

    # check if every single word in the dictionary is valid or not.
    for word in dictionary:
        if  3 <= len(word) <= 16:
            tmp_invisible_textbox.clear_textbox()
            tmp_invisible_textbox.append_text(word)
            path = []
            if are_all_letter_in_grid(tmp_solution_grid, tmp_invisible_textbox) and is_pattern_valid(tmp_solution_grid, tmp_invisible_textbox, path):
                possible_words_pathes.append(path)
                tmp_solution_player.add_to_correctly_guessed_words(word)
                update_score(tmp_solution_player, word)
    
    bind_words_with_their_buttons()


def draw_tmp_paper_screen():
    """
    draw the green screen/paper/notebook next to the small, temporary grid
    """
    DISPLAY_SCREEN.blit(comparison_icon, (10, 2)) # comparison icon
    font = pygame.font.Font("freesansbold.ttf", 24)
    rendered_text = font.render("Comparison" , True, ryb_red)
    DISPLAY_SCREEN.blit(rendered_text, (95, 20))

    pygame.draw.rect(DISPLAY_SCREEN , notes_color, (6, grid_off_set_y, grid_off_set_x-14, grid_height-2))


def draw_solution_screen(tmp_solution_player):
    """
    draw the words inside the green screen/paper/notebook next to the small, temporary grid
    Args:
        tmp_solution_player (Player): computer/ Ideal player
    """
    pygame.draw.rect(DISPLAY_SCREEN , green_apple, (grid_off_set_x, grid_off_set_y, grid_width/2, grid_height))
    
    font = pygame.font.Font("freesansbold.ttf", 20)
    rendered_text = font.render("All Possible Words:", True, black)
    DISPLAY_SCREEN.blit(rendered_text, (grid_off_set_x+10, grid_off_set_y+10))
    
    
    font = pygame.font.Font("freesansbold.ttf", 9)
    word_x = grid_off_set_x + 10
    word_y = grid_off_set_y + 40
    for word in tmp_solution_player.get_correctly_guessed_words():
        rendered_text = font.render(word, True, black)
        DISPLAY_SCREEN.blit(rendered_text, (word_x, word_y))
        word_y += 15
        if word_y >= height-70:
            word_y = grid_off_set_y  + 40 
            word_x += 60


def draw_possible_words_buttons(possible_words_buttons):
    """
    to display the button when the player hovers over them.
    Args:
        possible_words_buttons ([Button]): list of buttons to display the pathes of the possible words when the player hovers over them.
    """
    mouse_position = pygame.mouse.get_pos() # get the position of the mouse
    for btn in possible_words_buttons:
        if btn.is_hovered_over(mouse_position):
            btn.blit(DISPLAY_SCREEN)


def reset_cubes(tmp_solution_grid):
    """
    reset all the cubes of the temporary grid and draw their standar/default color when the player doesn't hover over them.
    Args:
        tmp_solution_grid (Grid): small temporary grid for the solution screen
    """
    for row in tmp_solution_grid.cubes:
        for cube in row:
            cube.is_being_guessed = False


def manage_events_for_solution_screen(tmp_solution_grid, main_menu_button, play_again_button, possible_words_buttons, possible_words_pathes):
    """

    Args:
        tmp_solution_grid (Grid): small temporary grid for the solution screen
        main_menu_button (Button): button to go to the main menu
        play_again_button (Button): button to play gain and start/restart the whole game.
        possible_words_buttons ([Button]): list of buttons to display the pathes of the possible words when the player hovers over them.
        possible_words_pathes ([tuble]): list of all the valid pathes stored as tubles 
    """
    from game_play_window import start_game

    mouse_position = pygame.mouse.get_pos() # get the position of the mouse

    # manage/handle all the events of the temporary screen
    for event in pygame.event.get():
        # exit game when user/player clicks on the X icon of the displaying windows.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        # manage/handel the events of the mouse and the buttons of the temporary solution screen/window
        if event.type == pygame.MOUSEBUTTONDOWN:
            if main_menu_button.is_clicked(mouse_position, event):
                introduction()
            elif play_again_button.is_clicked(mouse_position, event):
                start_game()

    # display the path when the player hovers over the solution/word with the mouse
    for btn, path in zip(possible_words_buttons, possible_words_pathes):
        if btn.is_hovered_over(mouse_position):
            draw_path(tmp_solution_grid, path)
            draw_cubes(tmp_solution_grid)
    