import sys
import pygame
from network import Network
import pathlib

pygame.font.init()

width = 1280
height = 720
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Rock, paper, scissors')
background = pygame.image.load('assets/background.jpg')
image = pygame.image.load('assets/scissors.png')
pygame.display.set_icon(image)

FONT = pathlib.Path('assets/Montserrat-Bold.ttf')
FONT_SIZE = 40
WHITE = (255, 255, 255)


class Button:
    """Simple class to draw text-buttons"""

    def __init__(self, text, x, y):
        """
        :param text: text on button
        :param x: x position
        :param y: y position
        """
        self.text = text
        self.x = x
        self.y = y
        self.width = 300
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, color=(0, 0, 0, 255),
                         rect=(self.x, self.y, self.width, self.height),
                         border_radius=25,
                         width=1)
        font = pygame.font.Font(FONT, FONT_SIZE)
        text = font.render(self.text, True, WHITE)
        win.blit(text, (self.x + round(self.width / 2) - round(text.get_width() / 2),
                        self.y + round(self.height / 2) - round(text.get_height() / 2)))

    def click(self, position: tuple):
        """
        Checks if button was clicked


        :param position: (x, y) of mouse position
        :return True / False
        """
        x1 = position[0]
        y1 = position[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False


buttons = [Button('Rock', 55, 480), Button('Scissors', 490, 480), Button('Paper', 920, 480)]


def redraw_window(win, game, player):
    """
    Redrawing window according to made players' moves

    :param win: current window
    :param game: received game from server
    :param player: current player
    """
    win.blit(background, [0, 0])

    font = pygame.font.Font(FONT, FONT_SIZE)

    if not (game.connected()):
        text = font.render("Waiting for opponent", True, WHITE)
        win.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
    else:
        text = font.render("Your Move", True, WHITE)
        win.blit(text, (155, 140))
        text = font.render("Opponent move", True, WHITE)
        win.blit(text, (784, 140))

        move1 = game.get_player_move(0)
        move2 = game.get_player_move(1)
        if game.both_made_move():
            text1 = font.render(move1, True, WHITE)
            text2 = font.render(move2, True, WHITE)
        else:
            if game.player1_made_move and player == 0:
                text1 = font.render(move1, True, WHITE)
            elif game.player1_made_move:
                text1 = font.render("In", True, WHITE)
            else:
                text1 = font.render("Waiting", True, WHITE)

            if game.player2_made_move and player == 1:
                text2 = font.render(move2, True, WHITE)
            elif game.player2_made_move:
                text2 = font.render("In", True, WHITE)
            else:
                text2 = font.render("Waiting", True, WHITE)

        if player == 1:
            win.blit(text2, (155, 310))
            win.blit(text1, (958, 310))
        else:
            win.blit(text1, (155, 350))
            win.blit(text2, (958, 350))

        for button in buttons:
            button.draw(win)

    pygame.display.update()


def game_screen():
    """Main game screen"""

    run = True
    clock = pygame.time.Clock()
    n = Network()
    player = int(n.get_player_id())
    print("You are player", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("__get")
        except Exception as e:
            run = False
            print(f"{e} --- Couldn't get game")
            break

        if game.both_made_move():
            redraw_window(screen, game, player)
            pygame.time.delay(500)
            try:
                game = n.send("__reset")
            except Exception as e:
                run = False
                print(f"{e} --- Couldn't get game")
                break

            font = pygame.font.Font(FONT, FONT_SIZE)
            if (game.winner() == 1 and player == 1) or (game.winner() == 0 and player == 0):
                text = font.render("You won!", True, WHITE)
            elif game.winner() == -1:
                text = font.render("Tie!", True, WHITE)
            else:
                text = font.render("You lost!", True, WHITE)

            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in buttons:
                    if btn.click(pos) and game.connected():
                        if player == 0:
                            if not game.player1_made_move:
                                n.send(btn.text)
                        else:
                            if not game.player2_made_move:
                                n.send(btn.text)

        redraw_window(screen, game, player)


if __name__ == "__main__":
    while True:
        run = True
        clock = pygame.time.Clock()

        while run:
            clock.tick(60)
            screen.blit(background, [0, 0])
            font = pygame.font.Font(FONT, 64)
            text = font.render("Click to start", True, WHITE)
            screen.blit(text, (width / 2 - text.get_width() / 2, height / 2 - text.get_height() / 2))
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    run = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    run = False

        game_screen()
