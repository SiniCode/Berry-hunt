from random import randint
import pygame

class UI:
    def __init__(self):
        pygame.init()
        self.set_up()
        self.record = self.check_record()
        self.upload_pictures()
        self.starting_point()
        self.loop()

    def set_up(self):
        self.display = pygame.display.set_mode((1060, 820))
        pygame.display.set_caption("Berry Hunt")

        self.big_font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 20)

        self.clock = pygame.time.Clock()

    def check_record(self):
        with open("./data/record.txt") as file:
            record = file.read().strip()
        return int(record)

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
            X = randint(-80, -50)
            Y = randint(5, 520)
            V = randint(2, 5)
            self.tigers.append([X, Y, V])

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
                if self.end is False and event.key == pygame.K_RIGHT:
                    if self.horizontal_movement <= 0:
                        self.horizontal_movement = 2
                    elif self.horizontal_movement <= 6:
                        self.horizontal_movement += 2
                    self.vertical_movement = 0

                elif self.end is False and event.key == pygame.K_LEFT:
                    if self.horizontal_movement >= 0:
                        self.horizontal_movement = -2
                    elif self.horizontal_movement >= -6:
                        self.horizontal_movement -= 2
                    self.vertical_movement = 0

                elif self.end is False and event.key == pygame.K_UP:
                    if self.vertical_movement >= 0:
                        self.vertical_movement = -2
                    elif self.vertical_movement >= -6:
                        self.vertical_movement -= 2
                    self.horizontal_movement = 0

                elif self.end is False and event.key == pygame.K_DOWN:
                    if self.vertical_movement <= 0:
                        self.vertical_movement = 2
                    elif self.vertical_movement <= 6:
                        self.vertical_movement += 2
                    self.horizontal_movement = 0

                if self.end == True and event.key == pygame.K_RETURN:
                    self.starting_point()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if mouse_x > 898 and mouse_x < 1040 and mouse_y > 783 and mouse_y < 800:
                    self.record_to_zero()

            if event.type == pygame.QUIT:
                exit()

    def record_to_zero(self):
        self.record = 0
        with open("./data/record.txt", "w") as file:
            file.write("0")

    def draw_display(self):
        self.display.fill((87, 151, 64))
        self.draw_rects()
        self.add_texts()
        self.draw_pictures()

        self.check_hits()

        pygame.display.flip()
        self.clock.tick(60)

    def draw_rects(self):
        pygame.draw.rect(self.display, (0, 0, 0), (0, 0, 1059, 740), width=10)
        pygame.draw.rect(self.display, (0, 0, 0), (0, 742, 1060, 820))
        pygame.draw.rect(self.display, (252, 252, 252), (898, 783, 1040, 800))

    def add_texts(self):
        score = self.big_font.render(
            f"Berries: {self.score}", True, (108, 184, 135))
        self.display.blit(score, (40, 755))

        if self.horizontal_movement != 0:
            speed = abs(self.horizontal_movement//2)
        elif self.vertical_movement != 0:
            speed = abs(self.vertical_movement//2)
        else:
            speed = 0
        speed_text = self.big_font.render(
            f"Current speed: {speed}", True, (108, 184, 135))
        self.display.blit(speed_text, (530-speed_text.get_width()/2, 755))

        record = self.big_font.render(
            f"Record: {self.record}", True, (108, 184, 135))
        self.display.blit(record, (900, 755))

        set_to_zero = self.small_font.render(
            "Set back to zero", True, (108, 184, 135))
        self.display.blit(set_to_zero, (905, 790))

        i = "Control the bear with the arrow keys. If you run into a wall or a tiger, the game is over."
        instructions = self.small_font.render(
            i, True, (252, 252, 252))
        self.display.blit(instructions, (40, 790))

    def draw_pictures(self):
        self.display.blit(self.bear, (self.bear_x, self.bear_y))
        self.bear_x += self.horizontal_movement
        self.bear_y += self.vertical_movement

        self.display.blit(self.berry, (self.berry_x, self.berry_y))
        self.pick_berry()

        for n in range(len(self.tigers)):
            tiger = self.tigers[n]
            self.display.blit(
                self.tiger, (tiger[0], tiger[1]))

            if n < 3:
                tiger[1] += tiger[2]
                if tiger[1] <= 0 or tiger[1] >= 740 - self.tiger.get_height():
                    self.tigers[n][2] = -tiger[2]

            else:
                tiger[0] += tiger[2]
                if (tiger[0] < -80 and tiger[2] < 0) or (tiger[0] > 1065 and tiger[2] > 0):
                    left = randint(0, 1)
                    if left == 1:
                        self.tigers[n] = [
                            randint(-80, -50), randint(5, 620), randint(2, 5)]
                    else:
                        self.tigers[n] = [
                            randint(1060, 1090), randint(5, 620), -randint(2, 5)]

    def pick_berry(self):
        bear = pygame.Rect(self.bear_x+5, self.bear_y+5,
                           self.bear.get_width()-10, self.bear.get_height()-10)
        berry = pygame.Rect(self.berry_x+3, self.berry_y+3,
                            self.berry.get_width()-6, self.berry.get_height()-6)
        if bear.colliderect(berry):
            self.score += 1
            self.berry_x = randint(10, 1050-self.berry.get_width())
            self.berry_y = randint(10, 730-self.berry.get_height())

    def check_hits(self):
        bear = pygame.Rect(self.bear_x+7, self.bear_y+5,
                           self.bear.get_width()-14, self.bear.get_height()-10)

        for tiger in self.tigers:
            spot = pygame.Rect(
                tiger[0]+7, tiger[1]+7, self.tiger.get_width()-14, self.tiger.get_height()-14)
            if bear.colliderect(spot):
                self.game_over()

        hits_left_wall = self.bear_x < 5
        hits_right_wall = self.bear_x + self.bear.get_width() > 1055
        hits_upper_wall = self.bear_y < 5
        hits_lower_wall = self.bear_y + self.bear.get_height() > 730
        if hits_left_wall or hits_right_wall or hits_upper_wall or hits_lower_wall:
            self.game_over()

    def game_over(self):
        self.horizontal_movement = 0
        self.vertical_movement = 0
        for tiger in self.tigers:
            tiger[2] = 0

        if self.score > self.record:
            self.record = self.score
            self.new_record = True
            self.save_record()

        self.end = True
        self.draw_end_display()

    def save_record(self):
        with open("./data/record.txt", "w") as file:
            file.write(str(self.record))

    def draw_end_display(self):
        self.display.fill((0, 0, 0))

        if self.score == 1:
            message = "Game over. You picked 1 berry."
        else:
            message = f"Game over. You picked {self.score} berries."

        text = self.big_font.render(message, True, (87, 151, 64))
        self.display.blit(
            text, (530-text.get_width()/2, 410-text.get_height()/2))

        if self.new_record:
            congrats = self.big_font.render(
                "Congratulations, that is a new record!", True, (87, 151, 64))
            self.display.blit(congrats, (530-congrats.get_width()/2, 500))

        new_game = self.small_font.render(
            "Press ENTER to start a new game!", True, (252, 252, 252))
        self.display.blit(new_game, (530-new_game.get_width()/2, 600))

        pygame.display.flip()
