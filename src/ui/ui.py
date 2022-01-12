from random import randint
import sys
import pygame


class UI:
    def __init__(self):
        """Initialize the game and start the first round."""
        
        pygame.init()
        self.set_up()
        self.record = self.check_record()
        self.upload_pictures()

        self.score = None
        self.bear_x = None
        self.bear_y = None
        self.horizontal_movement = None
        self.vertical_movement = None
        self.berry_x = None
        self.berry_y = None
        self.tigers = None
        self.end = None
        self.new_record = None

        self.starting_point()
        self.loop()

    def set_up(self):
        """Configure the game display, fonts, and the clock."""
        
        self.display = pygame.display.set_mode((1060, 820))
        pygame.display.set_caption("Berry Hunt")

        self.big_font = pygame.font.SysFont("Arial", 26)
        self.small_font = pygame.font.SysFont("Arial", 20)

        self.clock = pygame.time.Clock()

    def check_record(self):
        """Read the current record from a separate file."""
        
        with open("./data/record.txt") as file:
            record = file.read().strip()
        return int(record)

    def upload_pictures(self):
        """Upload the game characters from a separate directory."""
        
        self.bear = pygame.image.load('./src/pictures/bear.png')
        self.berry = pygame.image.load('./src/pictures/berry.png')
        self.tiger = pygame.image.load('./src/pictures/tiger.png')
        self.bear2 = pygame.image.load('./src/pictures/bear2.png')

    def starting_point(self):
        """Set the correct value to all variables at the beginning of a new round."""
        
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
            x_coord = randint(-80, -50)
            y_coord = randint(5, 520)
            velocity = randint(2, 5)
            self.tigers.append([x_coord, y_coord, velocity])

        self.end = False
        self.new_record = False

    def loop(self):
        while True:
            self.check_events()
            self.draw_display()
            self.clock.tick(60)

    def check_events(self):
        """Specify the necessary key and mouse functions."""
        
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

                if self.end is True and event.key == pygame.K_RETURN:
                    self.starting_point()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if 898 <= mouse_x <= 1040 and 783 <=  mouse_y <= 800:
                    self.record_to_zero()

            if event.type == pygame.QUIT:
                sys.exit()

    def record_to_zero(self):
        """Set the game record back to zero and save the change in the record file."""
        
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
        """Draw the background."""
        pygame.draw.rect(self.display, (0, 0, 0), (0, 0, 1059, 740), width=10)
        pygame.draw.rect(self.display, (0, 0, 0), (0, 742, 1060, 820))
        pygame.draw.rect(self.display, (252, 252, 252), (898, 783, 1040, 800))

    def add_texts(self):
        """Show instructions and the current score, speed, and record on the display."""
        
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

        i = "Control the bear with the arrow keys. If you hit a wall or a tiger, the game is over."
        instructions = self.small_font.render(
            i, True, (252, 252, 252))
        self.display.blit(instructions, (40, 790))

    def draw_pictures(self):
        """Show the game characters on the display.
        The vertically moving tigers bounce back from the walls
        while the horizontally moving tigers disappear and receive a new
        starting spot and speed at random."""
        
        self.display.blit(self.bear, (self.bear_x, self.bear_y))
        self.bear_x += self.horizontal_movement
        self.bear_y += self.vertical_movement

        self.display.blit(self.berry, (self.berry_x, self.berry_y))
        self.pick_berry()

        for index, tiger in enumerate(self.tigers):
            self.display.blit(
                self.tiger, (tiger[0], tiger[1]))

            if index < 3:
                tiger[1] += tiger[2]
                if tiger[1] <= 0 or tiger[1] >= 740 - self.tiger.get_height():
                    self.tigers[index][2] = -tiger[2]

            else:
                tiger[0] += tiger[2]
                if (tiger[0] < -80 and tiger[2] < 0) or (tiger[0] > 1065 and tiger[2] > 0):
                    left = randint(0, 1)
                    if left == 1:
                        self.tigers[index] = [
                            randint(-80, -50), randint(5, 620), randint(2, 5)]
                    else:
                        self.tigers[index] = [
                            randint(1060, 1090), randint(5, 620), -randint(2, 5)]

    def pick_berry(self):
        """If the bear hits the berry, move the berry to a random location on the display
        and add 1 to the score."""
        
        bear = pygame.Rect(self.bear_x+5, self.bear_y+5,
                           self.bear.get_width()-10, self.bear.get_height()-10)
        berry = pygame.Rect(self.berry_x+3, self.berry_y+3,
                            self.berry.get_width()-6, self.berry.get_height()-6)
        if bear.colliderect(berry):
            self.score += 1
            self.berry_x = randint(10, 1050-self.berry.get_width())
            self.berry_y = randint(10, 730-self.berry.get_height())

    def check_hits(self):
        """If the bear hits a tiger or a wall, end the game."""
        
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
        """Stop all movement at the end of the game and and check if the player made a new record.
        Move to the end display."""
        
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
        """Save a new record to a separate file."""
        
        with open("./data/record.txt", "w") as file:
            file.write(str(self.record))

    def draw_end_display(self):
        """Show a game over message to the player."""
        
        self.display.fill((0, 0, 0))

        self.display.blit(self.bear2, (530-self.bear2.get_width()/2, 50))

        if self.score == 1:
            message = "Game over. You picked 1 berry."
        else:
            message = f"Game over. You picked {self.score} berries."

        text = self.big_font.render(message, True, (87, 151, 64))
        self.display.blit(
            text, (530-text.get_width()/2, 400))

        if self.new_record:
            congrats = self.big_font.render(
                "Congratulations, that is a new record!", True, (87, 151, 64))
            self.display.blit(congrats, (530-congrats.get_width()/2, 450))

        new_game = self.small_font.render(
            "Press ENTER to start a new game!", True, (252, 252, 252))
        self.display.blit(new_game, (530-new_game.get_width()/2, 600))

        pygame.display.flip()
