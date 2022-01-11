import pygame
from random import randint

class UI:
    def __init__(self):
        pygame.init()

        self.display = pygame.display.set_mode((1060, 820))
        pygame.display.set_caption("Berry Hunt")

        self.big_font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 20)

        self.clock = pygame.time.Clock()

        self.record = 0

        self.upload_pictures()
        self.starting_point()
        self.loop()

    def upload_pictures(self):
        self.bear = pygame.image.load('./src/pictures/bear.png')
        self.bear.convert_alpha()
        self.berry = pygame.image.load('./src/pictures/berry.png')
        self.berry.convert_alpha()
        self.tiger = pygame.image.load('./src/pictures/tiger.png')
        self.tiger.convert_alpha()

    def starting_point(self):
        self.score = 0

        self.bear_x = 20
        self.bear_y = 580
        self.horizontal_movement = 2
        self.vertical_movement = 0

        self.berry_x = 900
        self.berry_y = 40

        self.tigers = []
        self.tigers.append([400, 0, 2])
        self.tigers.append([500, 0, 5])
        self.tigers.append([600, 0, 3])
        for i in range(2):
            x = randint(-80, -50)
            y = randint(5, 620)
            v = randint(2, 5)
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
                    elif self.horizontal_movement >= -4:
                        self.horizontal_movement -= 2
                    self.vertical_movement = 0

                elif self.end == False and event.key == pygame.K_UP:
                    if self.vertical_movement >= 0:
                        self.vertical_movement = -2
                    elif self.vertical_movement >= -4:
                        self.vertical_movement -= 2
                    self.horizontal_movement = 0

                elif self.end == False and event.key == pygame.K_DOWN:
                    if self.vertical_movement <= 0:
                        self.vertical_movement = 2
                    elif self.vertical_movement <= 4:
                        self.vertical_movement += 2
                    self.horizontal_movement = 0

                if self.end == True and event.key == pygame.K_RETURN:
                    self.starting_point()

            if event.type == pygame.QUIT:
                exit()

    def draw_display(self):
        #screen 1060, 820
        self.display.fill((87, 151, 64))
        pygame.draw.rect(self.display, (0, 0, 0), (0, 0, 1059, 740), width = 10)
        pygame.draw.rect(self.display, (0, 0, 0), (0, 742, 1060, 820))

        score = self.big_font.render(f"Berries: {self.score}", True, (108, 184, 135))
        self.display.blit(score, (40, 755))

        record = self.big_font.render(f"Record: {self.record}", True, (108, 184, 135))
        self.display.blit(record, (900, 755))

        instructions = self.small_font.render("Control the bear with the arrow keys. If you run into a wall or a tiger, the game is over.", True, (252, 252, 252))
        self.display.blit(instructions, (40, 790))

        self.display.blit(self.bear, (self.bear_x, self.bear_y))
        self.bear_x += self.horizontal_movement
        self.bear_y += self.vertical_movement

        self.display.blit(self.berry, (self.berry_x, self.berry_y))
        self.pick_berry()

        for n in range(len(self.tigers)):
            self.display.blit(self.tiger, (self.tigers[n][0], self.tigers[n][1]))

            if n < 3:
                self.tigers[n][1] += self.tigers[n][2]
                if self.tigers[n][1] <= 0 or self.tigers[n][1] >= 740 - self.tiger.get_height():
                    self.tigers[n][2] = -self.tigers[n][2]

            else:
                self.tigers[n][0] += self.tigers[n][2]
                if (self.tigers[n][0] < -80 and self.tigers[n][2] < 0) or (self.tigers[n][0] > 1065 and self.tigers[n][2] > 0):
                    left = randint(0, 1)
                    if left == 1:
                        self.tigers[n] = [randint(-80, -50), randint(5, 620), randint(2, 5)]
                    else:
                       self.tigers[n] = [randint(1060, 1090), randint(5, 620), -randint(2, 5)]

        self.check_hit()

        pygame.display.flip()
        self.clock.tick(60)

    def pick_berry(self):
        pass #siirrä serviceen

    def check_hit(self):
        pass #siirrä serviceen

    def game_over(self):
        self.horizontal_movement = 0
        self.vertical_movement = 0
        for tiger in self.tigers:
            tiger[2] = 0

        if self.score > self.record:
            self.record = self.score
            self.new_record = True

        self.end = True
        self.draw_end_display()

    def draw_end_display(self):
        self.display.fill((0, 0, 0))

        text = self.big_font.render(f"Game over. You picked {self.score} berries!", True, (87, 151, 64))
        self.display.blit(text, (530-text.get_width()/2, 410-text.get_height()/2))

        if self.new_record:
            congrats = self.big_font.render("Congratulations, that is a new record!", True, (87, 151, 64))
            self.display.blit(congrats, (530-congrats.get_width()/2, 500))

        new_game = self.small_font.render("Press ENTER to start a new game!", True, (252, 252, 252))
        self.display.blit(new_game, (530-new_game.get_width()/2, 600))

        pygame.display.flip()
