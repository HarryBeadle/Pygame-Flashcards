# Harry Beadle
# flashcards.py

from random import randint

import Tkinter
import tkFileDialog
root = Tkinter.Tk()
root.withdraw()

import pygame
pygame.init()

DEBUG = True
FPS = 20

X = 400
Y = 200
display = pygame.display.set_mode((X, Y))
pygame.display.set_caption("Flashcards")
font = pygame.font.SysFont("ubuntu", 20)
clock = pygame.time.Clock()


class flashcard:

    def __init__(self, question, answer, bg, fg):
        global X, Y

        self.question = question
        self.answer = answer

        self.back = pygame.Surface((X, Y))
        self.front = pygame.Surface((X, Y))
        self.back.fill(bg)
        pygame.draw.rect(self.back, fg, (10, 10, X - 20, Y - 20))
        self.front.fill(fg)
        pygame.draw.rect(self.front, bg, (10, 10, X - 20, Y - 20))

        if (sum(fg) / 3 < 255 / 2):
            frontfontcolor = (000, 000, 000)
        else:
            frontfontcolor = (255, 255, 255)

        if (sum(bg) / 3 < 255 / 2):
            backfontcolor = (000, 000, 000)
        else:
            backfontcolor = (255, 255, 255)

        self.front.blit(
            font.render(question, True, frontfontcolor),
            (
                (X - font.size(question)[0]) / 2,
                (Y - font.size(question)[1]) / 2
            )
        )
        self.back.blit(
            font.render(answer, True, backfontcolor),
            (
                (X - font.size(answer)[0]) / 2,
                (Y - font.size(answer)[1]) / 2
            )
        )


def random_color():
    return randint(0, 255), randint(0, 255), randint(0, 255)


def convert(file_):
    list_ = []
    for line in file_:
        split = line.index(":")
        list_.append(
            flashcard(line[:split], line[split + 1:-1], random_color(), random_color()))
    return list_


def handleinput():
    list_ = []
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE and DEBUG:
                pygame.quit()
                quit()
            if event.key == pygame.K_SPACE:
                list_.append("space")
    return list_

if __name__ == '__main__':
    display.fill((255, 255, 255))
    display.blit(
        font.render("Please open a file...", True, (0, 0, 0)),
        (
                (X - font.size("Please open a file...")[0]) / 2,
                (Y - font.size("Please open a file...")[1]) / 2
        )
    )
    pygame.display.flip()

    with open(tkFileDialog.askopenfilename()) as file_:
        cards = convert(file_)

    display.fill((255, 255, 255))
    display.blit(
        font.render("Press space to start", True, (0, 0, 0)),
        (
                (X - font.size("Press space to start")[0]) / 2,
                (Y - font.size("Press space to start")[1]) / 2
        )
    )
    pygame.display.flip()

    card_index = 0
    card_state = True

    while True:
        keystrokes = handleinput()
        if len(keystrokes) > 0:
            if card_state:
                display.blit(cards[card_index].front, (0, 0))
                card_state = not card_state
            else:
                display.blit(cards[card_index].back, (0, 0))
                card_state = not card_state
                card_index += 1
                if card_index == len(cards):
                    card_index = 0
        pygame.display.flip()
        clock.tick(FPS)