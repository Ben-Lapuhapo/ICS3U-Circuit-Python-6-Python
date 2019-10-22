#!/usr/bin/env python3

# Created by: Ben Lapuhapo
# Created on: OCT 2019
# This program is the "Space Alien" game
#   for CircuitPython

import ugame
import stage

import constants


def game_scene():
    # this function keeps the information of the buttons
    a_button_pressed = constants.button_state["button_up"]
    b_button_pressed = constants.button_state["button_up"]
    start_button_pressed = constants.button_state["button_up"]
    select_button_pressed = constants.button_state["button_up"]
    
    # get sound ready
    pew_sound = open("pew.wav", 'rb')
    sound = ugame.audio
    sound.stop()
    sound.mute(False)

    # an image bank for CircuitPython
    image_bank_1 = stage.Bank.from_bmp16("space_aliens.bmp")

    # sets the background to image 0 in the bank
    background = stage.Grid(image_bank_1, constants.SCREEN_X, constants.SCREEN_Y)
    
    # a list of sprites that will be updated every frame
    sprites = []
    
    ship = stage.Sprite(image_bank_1, 5, int(constants.SCREEN_X / 2 - constants.SPRITE_SIZE / 2),
                        int(constants.SCREEN_Y - constants.SPRITE_SIZE + constants.SPRITE_SIZE / 2))
    sprites.append(ship) # Insert at the top of the sprite list

    # create a stage for the background to show up on
    #   and set the frame rate to 60fps
    game = stage.Stage(ugame.display, constants.FPS)
    # set the layers, items show up in order
    game.layers = sprites + [background]
    # render the background and initial location of sprite list
    # most likely you will only render background once per scene
    game.render_block()

    # repeat forever, game loop
    while True:
        # get user input
        keys = ugame.buttons.get_pressed()
        # print(keys)
        # A button to fire
        if keys & ugame.K_X != 0:
            if a_button_pressed == constants.button_state["button_up"]:
                a_button_pressed = constants.button_state["button_just_pressed"]
            elif a_button_pressed == constants.button_state["button_just_pressed"]:
                a_button_pressed = constants.button_state["button_still_pressed"]
        else:
            a_button_pressed = constants.button_state["button_up"]
        
        # update game logic
        
        # move ship right
        if keys & ugame.K_RIGHT != 0:
            if ship.x > constants.SCREEN_X - constants.SPRITE_SIZE:
                ship.move(constants.SCREEN_X - constants.SPRITE_SIZE, ship.y)
            else:
                ship.move(ship.x + 1, ship.y)

        # move ship left
        if keys & ugame.K_LEFT != 0:
            if ship.x < 0:
                ship.move(0, ship.y)
            else:
                ship.move(ship.x - 1, ship.y)
                
        # play sound if A is pressed
        if a_button_pressed == constants.button_state["button_just_pressed"]:
            sound.play(pew_sound)

        # redraw sprite list
        game.render_sprites(sprites)
        game.tick()  # wait until refresh rate finishes


if __name__ == "__main__":
    game_scene()

