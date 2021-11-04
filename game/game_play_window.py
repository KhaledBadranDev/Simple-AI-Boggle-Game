
from models import *
from mutual import *
from solution_window import *
from boggle_game import introduction


def start_game():    
    """start the game
    """
    # open the dictionary file and store all these words in a list and convert all words to upper case
    words_file = open("words_alpha.txt")
    dictionary = list([word.strip().upper() for word in words_file])

    # make sure that the grid doesn't have too many possible words/solution, because the screen won't be big/wide enough to display all of them.
    grid = Grid()
    n = get_number_all_possible_solution(grid, dictionary) # n = number of all possible solutions/words
    while n > 180:
        grid = Grid()
        n = get_number_all_possible_solution(grid, dictionary)
     
    player = Player()
    
    # check the bonus letters.
    update_bonus_letters(grid)

    # define the buttons and the text box.
    text_box = TextBox(14, grid_off_set_y+4, grid_off_set_x-100, 50, notes_color, gray , 16, black, 16)
    enter_button = Button(grid_off_set_x-75, grid_off_set_y+4, 60, 50, beer, orange, 18, black, white, "Enter")
    main_menu_button = Button( grid_off_set_x, 6, 130, grid_off_set_y-15, beer, orange, 16, black, white, "Main Menu")
    show_solution_button = Button( (width+grid_off_set_x)//2 - 130//2, 6, 130, grid_off_set_y-15, beer, orange, 16, black, white, "Show Solution")
    restart_button = Button(width-130-6, 6, 130, grid_off_set_y-15, beer, orange, 16, black, white, "Restart")

    flashing_index = 0 # to flash the cursor of the textbox and the caution messages intermittently
    
    player.start_time = pygame.time.get_ticks() # to start the timer exactly from 3 minutes
    while True:
        if flashing_index > 60:
            flashing_index = 0
        flashing_index += 1

        manage_game(grid, player, dictionary, text_box, flashing_index, enter_button, main_menu_button, show_solution_button, restart_button)
        manage_events(grid, player, dictionary, text_box, flashing_index, enter_button, main_menu_button, show_solution_button, restart_button)

        clock.tick(60)


def get_number_all_possible_solution(grid, dictionary):
    """
    get number of all the possible solutions/words
    Args:
        grid (Grid): the main grid 
        dictionary ([str]): dictionary as a list of strings that has all the words 

    Returns:
        int: number of all the possible solutions/words
    """
    tmp_invisible_textbox = TextBox(14, grid_off_set_y+4, grid_off_set_x-100, 50, notes_color, gray , 16, black, 16)
    
    n = 0
    for word in dictionary:
        if  3 <= len(word) <= 16:
            tmp_invisible_textbox.clear_textbox()
            tmp_invisible_textbox.append_text(word)
            if are_all_letter_in_grid(grid, tmp_invisible_textbox) and is_pattern_valid(grid, tmp_invisible_textbox, []):
                n += 1
    return n                


def manage_game(grid, player, dictionary, text_box, flashing_index, enter_button, main_menu_button, show_solution_button, restart_button):
    """
    main method of the game. To manage the whole game
    Args:
        grid (Grid): the main grid 
        player (Player): The Player/user
        dictionary ([str]): dictionary as a list of strings that has all the words 
        text_box (TextBox): the text box where the player/user types the words/characters
        flashing_index (index): to draw the cautions messages in an intermittent wat => to make the cautions messages flash
        enter_button (Button): button to enter/save the typed word in the text box
        main_menu_button (Button): button to go to the main menu
        show_solution_button (Button): button to display all the possible words/solutions. Defaults to None.
        restart_button (Button): button to get a new grid and restart the time and the whole game
    """
    # background 
    DISPLAY_SCREEN.fill(gray)

    # toolbar and buttons:
    draw_toolbar(main_menu_button, restart_button, show_solution_button)
 
    # draw cubes
    draw_cubes(grid)

    # grid external borders
    pygame.draw.rect(DISPLAY_SCREEN , black, (grid_off_set_x-2, grid_off_set_y-2, grid_width, grid_height), 6)

    draw_paper_screen()
    
    # draw time
    draw_timer(grid, player, dictionary, enter_button, main_menu_button)

    draw_correctly_guessed_words(grid, player, dictionary)
    draw_player_score(player)
    draw_text_box(text_box, flashing_index, enter_button)
    draw_input_match_grid(grid, text_box, flashing_index)

    pygame.display.update()


def draw_timer(grid, player, dictionary, enter_button, main_menu_button):
    """
    calculate the remaining time and to draw it. 
    Args:
        grid (Grid): the main grid 
        player (Player): The Player/user
        dictionary ([str]): dictionary as a list of strings that has all the words 
        enter_button (Button): button to enter/save the typed word in the text box
        main_menu_button (Button): button to go to the main menu
    """
    player.time_since_start_in_milli_sec = pygame.time.get_ticks() - player.start_time
    remaining_time_in_milli_sec = player.end_time_in_milli_sec-player.time_since_start_in_milli_sec
    remaining_minutes = remaining_time_in_milli_sec//1000 //60
    remaining_seconds = (remaining_time_in_milli_sec//1000) % 60

    font = pygame.font.Font("freesansbold.ttf", 24)
    rendered_text = font.render(f"Time Remaining = {remaining_minutes} : {remaining_seconds}" , True, black)
    DISPLAY_SCREEN.blit(rendered_text, (50, 17))
    DISPLAY_SCREEN.blit(sand_timer_icon, (10,12)) # sand timer icon]]
    if is_time_over(remaining_time_in_milli_sec): # check if time is over.
        show_best_solution(grid, player, dictionary, enter_button, main_menu_button)


def draw_input_match_grid(grid, text_box, flashing_index):
    """
    manage the input and draw the cubes of the valid path with different colors
    Args:
        grid (Grid): the main grid 
        text_box (TextBox): the text box where the player/user types the words/characters
        flashing_index (index): to draw the cautions messages in an intermittent wat => to make the cautions messages flash
    """
    if len(text_box.text) == 0:
        for row in grid.cubes:
            for cube in row:
                cube.is_being_guessed = False
        return

    if not are_all_letter_in_grid(grid, text_box): # if there is any letter that doesn't exist in the grid, tell the player.
        draw_caution(flashing_index, "letters are not in grid!")
        return

    found_path = [] # just to draw the cubes in different color if they are being guessed
    if is_pattern_valid(grid, text_box, found_path):
        draw_path(grid, found_path)
    else: # if the pattern/ path is wrong, tell the player
        draw_caution(flashing_index, "path/pattern is not valid!")


def draw_caution(flashing_index, caution_message:str):
    """
    draw caution messages to tell the player what he has done wrong.
    Args:
        flashing_index (index): to draw the cautions messages in an intermittent wat => to make the cautions messages flash
        caution_message (str): a caution message to tell the player what he has done wrong.
    """
    if flashing_index  % 30 < 15:
        font = pygame.font.Font("freesansbold.ttf", 18)
        rendered_text = font.render(caution_message , True, ryb_red)
        DISPLAY_SCREEN.blit(rendered_text, (grid_off_set_x-270, 120))
    clock.tick(60)


def draw_text_box(text_box, flashing_index, enter_button):
    """
    draw the text box, the cursor and the numbers of characters under it. 
    Args:
        text_box (TextBox): the text box where the player/user types the words/characters
        flashing_index (index): to draw the cautions messages in an intermittent wat => to make the cautions messages flash
        enter_button (Button): button to enter/save the typed word in the text box
    """
    text_box.blit(DISPLAY_SCREEN)

    if flashing_index  % 30 < 15:
        text_box.blit_cursor(DISPLAY_SCREEN)
    clock.tick(60)

    text_box.blit_number_of_chars(DISPLAY_SCREEN)
    mouse_position = pygame.mouse.get_pos() # get the position of the mouse
    if enter_button.is_hovered_over(mouse_position):
        enter_button.blit_hovered_over(DISPLAY_SCREEN)
    else:
        enter_button.blit(DISPLAY_SCREEN, gray)


def draw_paper_screen():
    """
    draw the yellow screen/notebook/paper on the left.
    """
    pygame.draw.rect(DISPLAY_SCREEN , gray, (2, 2, grid_off_set_x-8, height-4), 6)
    pygame.draw.rect(DISPLAY_SCREEN , notes_color, (6, 6, grid_off_set_x-14, height-11))


def update_correctly_guessed_words(grid, player, dictionary):
    """
    update the list of the correctly typed words for the player
    Args:
        grid (Grid): the main grid 
        player (Player): The Player/user
        dictionary ([str]): dictionary as a list of strings that has all the words 
    """
    tmp_invisible_textbox = TextBox(14, grid_off_set_y+4, grid_off_set_x-100, 50, notes_color, gray , 16, black, 16)
    for word in player.get_all_guessed_words():
        tmp_invisible_textbox.text = word
        if (is_pattern_valid(grid, tmp_invisible_textbox, [])) and (word in dictionary) and (word not in player.get_correctly_guessed_words()):
            player.add_to_correctly_guessed_words(word)
            update_score(player, word)


def is_time_over(remaining_time_in_milli_sec): 
    """
    check whether the time is over or not.
    Args:
        remaining_time_in_milli_sec (int): the remaining time in milliseconds.
    Returns:
        boolean: True if remaining time is over. Otherwise, False.
    """
    return True if remaining_time_in_milli_sec <= 0 else False


def update_bonus_letters(grid):
    """
    iterate over the grid and if any bonus letter will be found, it will be added to the list of bonus letters.
    Args:
        grid (Grid): the main grid 
    """
    global bonus_letters
    bonus_letters.clear()

    for row in grid.cubes:
        for cube in row:
            if cube.has_bonus:
                bonus_letters.append(cube.text_str)


def is_input_valid(player, text_box):
    """
    check whether the word/characters that the player is trying to enter/save are valid or not.
    Args:
        player (Player): The Player/user
        text_box (TextBox): the text box where the player/user types the words/characters

    Returns:
        boolean: True the word/characters that the player is trying to enter/save are valid. Otherwise, False.
    """
    if len(text_box.text) > 2 and text_box.text not in player.get_all_guessed_words():
        return True
    else:
        if len(text_box.text) <= 2:
            pygame.draw.rect(DISPLAY_SCREEN, notes_color, (grid_off_set_x-270, 120, 240, 30))
            draw_caution(0, "go for 3 letters at least!")
            pygame.display.update()
            time.sleep(1)
        if text_box.text in player.get_all_guessed_words():
            pygame.draw.rect(DISPLAY_SCREEN, notes_color, (grid_off_set_x-270, 120, 240, 30))
            draw_caution(0, "word was entered before!")
            pygame.display.update()
            time.sleep(1)    
        return False


def manage_events(grid, player, dictionary, text_box, flashing_index, enter_button, main_menu_button, show_solution_button, restart_button):
    """
    manage all possible events of the game.
    Args:
        grid (Grid): the main grid 
        player (Player): The Player/user
        dictionary ([str]): dictionary as a list of strings that has all the words 
        text_box (TextBox): the text box where the player/user types the words/characters
        flashing_index (index): to draw the cautions messages in an intermittent wat => to make the cautions messages flash
        enter_button (Button): button to enter/save the typed word in the text box
        main_menu_button (Button): button to go to the main menu
        show_solution_button (Button): button to display all the possible words/solutions. Defaults to None.
        restart_button (Button): button to get a new grid and restart the time and the whole game

    """
    mouse_position = pygame.mouse.get_pos() # get the position of the mouse

    # check for events     
    for event in pygame.event.get():
        # exit game when user/player clicks on the X icon of the displaying windows.
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # manage/handel the events of the mouse and the buttons of the game
        if event.type == pygame.MOUSEBUTTONDOWN:
            if enter_button.is_clicked(mouse_position, event) and is_input_valid(player, text_box):
                player.add_to_guessed_words(text_box.text)
                text_box.clear_textbox()
            elif main_menu_button.is_clicked(mouse_position, event):
                introduction()
            elif show_solution_button.is_clicked(mouse_position, event):
                show_best_solution(grid, player, dictionary, enter_button, main_menu_button)
            elif restart_button.is_clicked(mouse_position, event):
                start_game()

        # manage/handel the events of the keys of the keyboard 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                text_box.append_text("A")
            elif event.key == pygame.K_b:
                text_box.append_text("B")
            elif event.key == pygame.K_c:
                text_box.append_text("C")
            elif event.key == pygame.K_d:
                text_box.append_text("D")
            elif event.key == pygame.K_e:
                text_box.append_text("E")
            elif event.key == pygame.K_f:
                text_box.append_text("F")
            elif event.key == pygame.K_g:
                text_box.append_text("G")
            elif event.key == pygame.K_h:
                text_box.append_text("H")
            elif event.key == pygame.K_i:
                text_box.append_text("I")
            elif event.key == pygame.K_j:
                text_box.append_text("J")
            elif event.key == pygame.K_k:
                text_box.append_text("K")
            elif event.key == pygame.K_l:
                text_box.append_text("L")
            elif event.key == pygame.K_m:
                text_box.append_text("M")
            elif event.key == pygame.K_n:
                text_box.append_text("N")
            elif event.key == pygame.K_o:
                text_box.append_text("O")
            elif event.key == pygame.K_p:
                text_box.append_text("P")
            elif event.key == pygame.K_q:
                text_box.append_text("Q")
            elif event.key == pygame.K_r:
                text_box.append_text("R")
            elif event.key == pygame.K_s:
                text_box.append_text("S")
            elif event.key == pygame.K_t:
                text_box.append_text("T")
            elif event.key == pygame.K_u:
                text_box.append_text("U")
            elif event.key == pygame.K_v:
                text_box.append_text("V")
            elif event.key == pygame.K_w:
                text_box.append_text("W")
            elif event.key == pygame.K_x:
                text_box.append_text("X")
            elif event.key == pygame.K_y:
                text_box.append_text("Y")
            elif event.key == pygame.K_z:
                text_box.append_text("Z")
            
            # if the player pressed on the backspace key
            elif event.key == pygame.K_BACKSPACE:
                text_box.backspace()

            # if the player pressed on the enter key
            elif event.key == pygame.K_RETURN and is_input_valid(player, text_box):
                enter_button.blit_hovered_over(DISPLAY_SCREEN)
                pygame.display.update()
                clock.tick(60)
                player.add_to_guessed_words(text_box.text)
                text_box.clear_textbox()
            