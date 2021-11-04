
from models import *
from game_play_window import *


def introduction():
    """ 
    Display the introductory screen of the game
    """
    button_width = 290
    button_height = 60
    play_button = Button(-400, height/(1.5), button_width, button_height, beer, orange, 32, black, white, "PLAY")
    instructions_button = Button(width+150, height/(1.5)+button_height+10, button_width,button_height, beer, orange, 32, black, white, "INSTRUCTIONS")
    quit_button = Button(-400, height/(1.5)+button_height*2+20, button_width,button_height, beer, orange, 32, black, white, "QUIT")
    

    # To centre the button in the middle of the screen -> width/2 - button_width/2
    # To draw the buttons in an animated way.
    while play_button.x < width/2-button_width/2 or instructions_button.x > width/2-button_width/2:
        DISPLAY_SCREEN.blit(intro_img, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if play_button.x < width/2-button_width/2:
            play_button.x += 3
            quit_button.x += 3
        if instructions_button.x > width/2-button_width/2 :    
            instructions_button.x -= 3

        play_button.blit(DISPLAY_SCREEN)
        instructions_button.blit(DISPLAY_SCREEN)
        quit_button.blit(DISPLAY_SCREEN)
        pygame.display.update()

    # The introductory screen
    run = True
    while run:
        DISPLAY_SCREEN.blit(intro_img, (0, 0))

        mouse_position = pygame.mouse.get_pos() # to get the position of the mouse
        for event in pygame.event.get(): # to manage/handle the events e.g clicking on a button 
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.is_clicked(mouse_position, event):
                    from game_play_window import start_game
                    start_game()
                    run = False
                elif instructions_button.is_clicked(mouse_position, event):
                    # instructions()
                    webbrowser.open_new("https://www.ultraboardgames.com/boggle/game-rules.php")
                elif quit_button.is_clicked(mouse_position, event):
                    pygame.quit()
                    sys.exit()
        
        if play_button.is_hovered_over(mouse_position): # change the color of the button when the player/user hovers over it
            play_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            play_button.blit(DISPLAY_SCREEN, gray)
        if instructions_button.is_hovered_over(mouse_position):
            instructions_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            instructions_button.blit(DISPLAY_SCREEN, gray)
        if quit_button.is_hovered_over(mouse_position):
            quit_button.blit_hovered_over(DISPLAY_SCREEN)
        else:
            quit_button.blit(DISPLAY_SCREEN, gray)

        clock.tick(60)
        pygame.display.update()


if __name__ == "__main__": # To avoid runing the game, if this file is imported.
    introduction()
 