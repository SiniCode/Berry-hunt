import pygame
from random import randint

class UI:
    def __init__(self):
        pygame.init()

        self.display = pygame.display.set_mode((640, 480 + 80))
        pygame.display.set_caption("Berry Hunt")

        self.big_font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 20)

        self.clock = pygame.time.Clock()

        self.record = 0

        self.upload_pictures()
        self.starting_point()
        self.loop()

    def upload_pictures(self):
        self.bear = pygame.image.load("./pictures/bear.png")
        self.berry = pygame.image.load("./pictures/berry.png")
        self.tiger = pygame.image.load("./pictures/tiger.png")

    def starting_point(self):
        self.score = 0

        self.bear_x = 10
        self.bear_y = 380
        self.horizontal_movement = 2
        self.vertical_movement = 0

        self.berry_x = 590
        self.berry_y = 10

        self.tigers = []
        self.tigers.append([215, 0, 1])
        self.tigers.append([295, 0, 4])
        self.tigers.append([375, 0, 2])
        for i in range(2):
            x = randint(-80, -50)
            y = randint(5, 300)
            v = randint(1, 5)
            self.tigers.append([x, y, v])

        self.end = False
        self.new_record = False

    def loop(self):
        while True:
            self.check_events()
            self.draw_display()
            self.clock.tick(60)

    def check_events(self):
        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if self.end == False and event.key == pygame.K_RIGHT:
                    if self.horizontal_movement <= 0:
                        self.horizontal_movement = 2
                    elif self.horizontal_movement <= 4:
                        self.horizontal_movement += 2
                    self.vertical_movement = 0

                elif self.end == False and event.key == pygame.K_LEFT:
                    if self.horizontal_movement >= 0:
                        self.horizontal_movement = -2
                    elif self.horizontal_movement >= 4:
                        self.horizontal_movement -= 2
                    self.vertical_movement = 0

                elif self.end == False and event.key == pygame.K_UP:
                    if self.vertical_movement >= 0:
                        self.vertical_movement = -2
                    elif self.vertical_movement >= 4:
                        self.vertical_movement -= 2
                    self.horizontal_movement = 0

                elif self.end == False and event.key == pygame.K_DOWN:
                    if self.vertical_movement <= 0:
                        self.vertical_movement = 2
                    elif self.vertical_movement >= 4:
                        self.vertical_movement -= 2
                    self.horizontal_movement = 0

                if self.end == True and event.key == pygame.K_RETURN:
                    self.starting_point()

            if event.type == pygame.QUIT:
                exit()

    def draw_display(self):
        self.display.fill((0, 100, 100))
        pygame.draw.rect(self.display, (0, 0, 0), (0, 0, 638, 479), width = 10)
        pygame.draw.rect(self.display, (0, 0, 0), (0, 480, 640, 560))

        score = self.big_font.render(f"Berries: {self.score}", True, (0, 90, 90))
        self.display.blit(score, (20, 480))

        record = self.big_font.render(f"Record: {self.record}", True, (0, 90, 90))
        self.display.blit(record, (510, 480))

        instructions = self.small_font("Control the bear with the arrow keys. If you run into a wall or a tiger, the game is over.", True, (0, 140, 140))
        self.display.blit(instructions, (20, 520))

        self.display.blit(self.bear, (self.bear_x, self.bear_y))
        self.bear_x += self.horizontal_movement
        self.bear_y += self.vertical_movement

        self.display.blit(self.berry, (self.berry_x, self.berry_y))
        self.pick_berry()

        for n in range(len(self.tigers)):
            self.display.blit(self.tiger, (self.tigers[n][0], self.tigers[n][1]))

            if n < 3:
                self.tigers[n][1] += self.tigers[n][2]
                if self.tigers[n][1] <= 0 or self.tigers[n][1] >= 480 - self.tiger.get_height():
                    self.tigers[n][2] = -self.tigers[n][2]

            else:
                self.tigers[n][0] += self.tigers[n][2]
                if (self.tigers[n][0] < -80 and self.tigers[n][2] < 0) or (self.tigers[n][0] > 670 and self.tigers[n][2] > 0):
                    left = randint(0, 1)
                    if left == 1:
                        self.tigers[n] = [randint(-80, -50), randint(5, 400), randint(1, 4)]
                    else:
                       self.tigers[n] = [randint(640, 670), randint(5, 400), -randint(1, 4)]

        self.check_hit()

        pygame.display.flip()
        self.clock.tick(60)

    def pick_berry(self):
        pass #siirrä serviceen

    def check_hit(self):
        pass #siirrä serviceen
