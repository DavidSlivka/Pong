import pygame
import random

pygame.init()
WIDTH = 800
HEIGHT = 600

GAME_FONT = pygame.font.SysFont('arial', 40)
MENU_FONT = pygame.font.SysFont('Cooper black', 30)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
background_color = (0, 0, 0)


class Player:
    def __init__(self, x, y, width, height, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.wins = 0
        self.pos = (self.x, self.y, self.width, self.height)
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    def win(self):
        self.wins += 1
        
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

    def collide(self, object):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(object)


class Ball:
    def __init__(self, x, y, radius, color, difficulty_level):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.difficulty_level = int(difficulty_level)
        self.dx = random.choice([-difficulty_level, difficulty_level])
        self.dy = 0
        self.rect = pygame.Rect(self.x-self.radius, self.y-self.radius, 2*self.radius, 2*self.radius)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.rect = pygame.Rect(self.x - self.radius, self.y - self.radius, 2 * self.radius, 2 * self.radius)

    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)


class Button:
    def __init__(self, x, y, width, height, round_border, text, FONT):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = (96, 96, 96)
        self.round_border = round_border
        self.text = text
        self.text_col = (0, 0, 0)
        self.hover_col = (66, 66, 66)
        self.clicked = False
        self.font = FONT

    def draw(self):
        pos = pygame.mouse.get_pos()
        button_rect = pygame.Rect(self.x, self.y, self.width, self.height)

        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                self.clicked = True
                pygame.draw.rect(screen, self.hover_col, button_rect, 0, self.round_border)
            elif pygame.mouse.get_pressed()[0] == 0 and self.clicked == True:
                self.clicked = False
            else:
                pygame.draw.rect(screen, self.hover_col, button_rect, 0, self.round_border)
        else:
            pygame.draw.rect(screen, self.color, button_rect, 0, self.round_border)

        text_img = self.font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        screen.blit(text_img, (self.x + self.width // 2 - text_len // 2, self.y + self.height//2 - text_img.get_height()//2))


class Menu:
    def __init__(self, Button):
        self.btn1 = Button(WIDTH//5, HEIGHT // 10 * 2, WIDTH//5*3, WIDTH // 10, 25, "Easy", MENU_FONT)
        self.btn2 = Button(WIDTH//5, HEIGHT // 10 * 4, WIDTH//5*3, WIDTH // 10, 25, "Medium", MENU_FONT)
        self.btn3 = Button(WIDTH//5, HEIGHT // 10 * 6, WIDTH//5*3, WIDTH // 10, 25, "Hard", MENU_FONT)
        self.difficulty_level = 0

    def draw(self):
        self.btn1.draw()
        self.btn2.draw()
        self.btn3.draw()

    def click(self):
        if self.btn1.clicked:
            init_rackets()
            self.difficulty_level = 1

        if self.btn2.clicked:
            init_rackets()
            self.difficulty_level = 2

        if self.btn3.clicked:
            init_rackets()
            self.difficulty_level = 3


def draw_menu(menu):
    screen.fill(background_color)
    menu.draw()
    menu.click()
    pygame.display.update()
    return True if menu.difficulty_level != 0 else False


def init_rackets():
    racket1 = Player(50, HEIGHT / 2 - 35, 20, 70, (255, 128, 0))
    racket2 = Player(730, HEIGHT / 2 - 35, 20, 70, (171, 139, 237))
    return racket1, racket2


def init_menu():
    menu = Menu(Button)
    return menu


def start_game(difficulty_level):
    ball = Ball(WIDTH / 2, HEIGHT / 2, 10, (255, 255, 255), difficulty_level)
    return ball


def update_screen(racket1, racket2, ball):
    win_text = GAME_FONT.render(f"{racket1.wins} : {racket2.wins}", True, (255, 255, 100))

    screen.fill(background_color)
    pygame.draw.line(screen, (255, 255, 255), (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    screen.blit(win_text, (WIDTH / 2 - win_text.get_width() / 2, HEIGHT//15))
    racket1.draw()
    racket2.draw()
    ball.draw()
    pygame.display.update()


def game_loop(difficulty_level):
    screen.fill((0, 0, 0))
    racket1, racket2 = init_rackets()
    ball = start_game(difficulty_level)
    game_over = False
    running = False
    update_screen(racket1, racket2, ball)

    while not game_over:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_over = True
                elif event.key == pygame.K_w:
                    if racket1.y > 0:
                        racket1.y -= 5
                elif event.key == pygame.K_s:
                    if racket1.y + racket1.height < HEIGHT:
                        racket1.y += 5
                elif event.key == pygame.K_UP:
                    if racket2.y > 0:
                        racket2.y -= 5
                elif event.key == pygame.K_DOWN:
                    if racket2.y + racket2.height < HEIGHT:
                        racket2.y += 5
                else:
                    if not running:
                        ball = start_game(menu.difficulty_level)
                        update_screen(racket1, racket2, ball)
                        running = True

        if running:
            ball.move()

            if ball.y > HEIGHT - ball.radius or ball.y - ball.radius < 0:
                ball.dy *= -1

            if ball.x - ball.radius > WIDTH:
                racket1.win()
                running = False

            if ball.x - ball.radius < 0:
                racket2.win()
                running = False

            if racket2.collide(ball.rect) and racket2.x <= ball.x + ball.radius + ball.dx:
                if racket2.y + racket2.height // 2 < ball.y:
                    ball.dy = 1
                elif racket2.y + racket2.height // 2 == ball.y:
                    ball.dy = 0
                else:
                    ball.dy = -1
                ball.dx *= -1

            if racket1.collide(ball.rect) and racket1.x + racket1.width <= ball.x - ball.radius - ball.dx:
                if racket1.y + racket1.height // 2 < ball.y:
                    ball.dy = 1
                elif racket1.y + racket1.height // 2 == ball.y:
                    ball.dy = 0
                else:
                    ball.dy = -1
                ball.dx *= -1

            update_screen(racket1, racket2, ball)
            game_clock.tick(100)

    return False


game_over = False
selected = False

pygame.key.set_repeat(10)
game_clock = pygame.time.Clock()

menu = init_menu()


def main():
    run = True
    selected = False
    while run:
        pygame.time.delay(30)
        game_clock.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()
                break
        if not selected:
            selected = draw_menu(menu)
        else:
            run = game_loop(menu.difficulty_level)

        pygame.display.update()

    pygame.quit()


if __name__ == '__main__':
    main()
