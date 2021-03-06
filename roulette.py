import random
import pygame
from classes import Player, Bet, Button, Spot, Table, Wheel

WIDTH, HEIGHT = 800, 700
TABLE_WIDTH, TABLE_HEIGHT = 750, 300
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Roulette")

GREEN = (5, 130, 5)
GREEN_LIGHT = (55, 130, 55)
WHITE = (255, 255, 255)
GREY = (155, 155, 155)
BLACK = (0, 0, 0)

FPS = 60

TABLE = Table(TABLE_HEIGHT, HEIGHT, TABLE_WIDTH, WIDTH)
WHEEL = Wheel(TABLE)
TABLE.addWheel(WHEEL)

TABLE.image = pygame.transform.scale(TABLE.image, (TABLE_WIDTH, TABLE_HEIGHT))
WHEEL.image = pygame.transform.scale(WHEEL.image, (WIDTH//2,WIDTH//2))


def drawButtons():
    mouse = pygame.mouse.get_pos()

    for button in TABLE.buttons:
        if button.is_active:
            color, x, y = button.isHover(mouse)  # button hover listener
            if button.type == "payout":
                button.text_bool = True

            if button.box_bool: # draw button rectangle
                pygame.draw.rect(WIN, color, [x, y, button.width, button.height])

            if button.text_bool: # draw button text
                if button.type == "payout":
                    i = 0
                    for _text in button.text:
                        _font = pygame.font.SysFont('Corbel',35)
                        text = _font.render(_text, True, BLACK)
                        (_x, _y) = button.origin()
                        _y_offset = 0.05*TABLE.height_win*i
                        _y = _y + _y_offset
                        WIN.blit(text, (_x, _y))
                        i += 1
                else:
                    _text = button.text
                    _font = pygame.font.SysFont('Corbel',35)
                    text = _font.render(_text, True, BLACK)
                    WIN.blit(text, button.origin())


def drawWindow():
    # draw table
    WIN.fill(GREEN)
    WIN.blit(TABLE.image, ((WIDTH/2-TABLE_WIDTH/2), (HEIGHT-TABLE_HEIGHT)))
    WIN.blit(WHEEL.image, (1,1))

    # draw bets
    if len(TABLE.bets) > 0:
        _string = "Bets: {}".format(len(TABLE.bets))
        _font = pygame.font.SysFont('Corbel',35)
        _text = _font.render(_string, True, WHITE)
        WIN.blit(_text, (0, 0))

    # draw stacks
    # if len(TABLE.players) > 0:
    #     count = 0
    #     for player in TABLE.players:
    #         count += 1
    #         _font = pygame.font.SysFont('Corbel',35)
    #         _name = _font.render(player.name+": ", True, WHITE)
    #         _stack = _font.render("$"+str(player.stack), True, WHITE)
    #         WIN.blit(_name,(WIDTH//2+50, 50*count))
    #         WIN.blit(_stack,(WIDTH//2+250, 50*count))


def main():
    pygame.init()
    clock = pygame.time.Clock()
    run = True
    is_click = False
    
    while run:
        clock.tick(FPS)
        TABLE.is_click = False
        if len(TABLE.players) > 0 and not TABLE.current_player:
            TABLE.current_player = TABLE.players[0]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN: # mouse click listener
                TABLE.is_click = True

            if event.type == pygame.KEYDOWN: # key listener
                key = pygame.key.name(event.key)

                if TABLE.key_catch and TABLE.input_select:
                    TABLE.input_select.text_bool = True

                    if len(key) == 1:
                        if TABLE.input_select.input:
                            TABLE.input_select.input += key

                        else:
                            TABLE.input_select.input = key

                    elif key == "backspace":
                        if TABLE.input_select.input:
                            TABLE.input_select.input = TABLE.input_select.input[:-1]

                        else:
                            TABLE.input_select.input = None

                    TABLE.input_select.text = TABLE.input_select.input
            

        drawWindow()
        drawButtons()

        pygame.display.update()

    pygame.quit()

if __name__=="__main__":
    main()
