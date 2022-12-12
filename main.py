import pygame
import time
from pygame.locals import *
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)


"""
Apple class
"""
class Apple:
    def __init__(self, parent_screen) -> None:
        self.image = pygame.image.load("resources/apple.jpg").convert()
        self.parent_screen = parent_screen
        self.x = SIZE * 3
        self.y = SIZE * 3
    
    # Show the apple on the board
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()
    
    # Initialize a new apple after one is eaten
    def move(self):
        self.x = random.randint(1, 29) * SIZE
        self.y = random.randint(1, 19) * SIZE


"""
Snake class
"""
class Snake:
    def __init__(self, parent_screen, length) -> None:
        self.length = length
        self.block = pygame.image.load("resources/block.jpg").convert()
        self.parent_screen = parent_screen
        self.x = [SIZE] * length
        self.y = [SIZE] * length
        self.direction = 'down'
    
    # Increase the length of the snake when snake eats an apple
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)
    
    # Draw the blocks of snake
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()
    
    # Functions for moving the snake in four directions
    def move_left(self):
        self.direction = 'left'
    
    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'
            
    def move_down(self):
        self.direction = 'down'
    
    # Maintain the current direction and move
    def walk(self):
        for i in range(self.length - 1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= SIZE
        if self.direction == 'right':
            self.x[0] += SIZE
        if self.direction == 'up':
            self.y[0] -= SIZE
        if self.direction == 'down':
            self.y[0] += SIZE
        self.draw()


"""
Game class
"""
class Game:
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("CodeBasics Snake and Apple Game")
        pygame.mixer.init()
        self.play_background_music()
        # Initialize a window or screen to play
        self.surface = pygame.display.set_mode((1200, 800))
        self.surface.fill((110, 110, 5))
        self.snake = Snake(self.surface, 2)
        self.snake.draw()
        self.apple = Apple(self.surface)
    
    # Eat apple
    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 <= x2 + SIZE:
            if y1 >= y2 and y1 <= y2 + SIZE:
                return True
        return False

    # Play sound effect
    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)
    
    # Play background music
    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()
    
    def render_background(self):
        bg = pygame.image.load("resources/background.jpg")
        self.surface.blit(bg, (0, 0))

    # Do all the drawing
    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

        # Snake eats apple
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding")
            # print("Collision occurred")
            self.snake.increase_length()
            self.apple.move()
        
        # Snake collides with itself
        for i in range(3, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                # print("Game Over")
                # exit(0)
                raise "Game Over"
        
        # Snake collides with the boarders
        if self.snake.x[0] < 0 or self.snake.x[0] >= 1200 or self.snake.y[0] < 0 or self.snake.y[0] >= 800:
            raise "Game Over"
    
    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game Over! Your Score is {self.snake.length}", True, (255, 255, 255))
        self.surface.blit(line1, (200, 300))
        line2 = font.render(f"Press Enter to play again. Press Escape to exit!", True, (255, 255, 255))
        self.surface.blit(line2, (200, 350))
        pygame.display.flip()

        pygame.mixer.music.pause()
    
    # Display the current score
    def display_score(self):
        font = pygame.font.SysFont('arial', 30)
        score = font.render(f"Score: {self.snake.length - 2}", True, (200, 200, 200))
        self.surface.blit(score, (1000, 10))
    
    # Reset the game
    def reset(self):
        self.snake = Snake(self.surface, 2)
        self.apple = Apple(self.surface)

    # Run the program
    # Exit if click the exit or press ESC
    def run(self):
        running = True
        pause = False

        while running:
            # Observe the event of keyboard and mouse
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    
                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    # change block position
                    if not pause:
                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()
                            
                        if event.key == K_LEFT:
                            self.snake.move_left()
                            
                        if event.key == K_RIGHT:
                            self.snake.move_right()
                        
                elif event.type == QUIT:
                    running = False
            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.play_sound("crash")
                self.show_game_over()
                pause = True
                self.reset()

            time.sleep(0.2)

if __name__ == '__main__':
    game = Game()
    game.run()