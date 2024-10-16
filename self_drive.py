import neat
import time
import os
import random
import pygame
pygame.font.init()

WIN_WIDTH = 360
WIN_HEIGHT = 540
DEADZONE_BUFFER = 50
ROAD_SCROLL_SPEED = 5

CAR_IMG = pygame.transform.scale(pygame.image.load(os.path.join("car.png")), (int(0.08 * pygame.image.load(os.path.join("car.png")).get_width()), int(0.08 * pygame.image.load(os.path.join("car.png")).get_height())))
ROCK_IMG = pygame.transform.scale(pygame.image.load(os.path.join("rock.png")), (int(WIN_WIDTH * 0.15), int(WIN_HEIGHT * 0.1)))
ROAD_IMG = pygame.image.load(os.path.join("road.png"))
COIN_IMG = pygame.transform.scale(pygame.image.load(os.path.join("coin.png")), (int(WIN_WIDTH * 0.15), int(WIN_HEIGHT * 0.1)))
STAT_FONT = pygame.font.SysFont("comicsans", 25)

class Car:
    IMG = CAR_IMG

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vel = 50
        self.img = self.IMG
        self.width = self.img.get_width()
        self.height = self.img.get_height()

    def move(self, left=False, right=False):
        if left:
            self.x -= self.vel
        if right:
            self.x += self.vel
        
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > WIN_WIDTH:
            self.x = WIN_WIDTH - self.width

    def draw(self, win):
        win.blit(self.img, (self.x, self.y))

    def get_mask(self):
        return pygame.mask.from_surface(self.img)
class BigRock:
    VEL = 12
    GAP_WIDTH = 100  # The width of the gap between the two rocks

    def __init__(self):
        self.rock_left = Rock()  # Left rock
        self.rock_right = Rock()  # Right rock
        self.y = -200
        self.passed = False

        # Adjust x-coordinates for left and right rocks to leave a narrow passage
        self.rock_left.x = random.randint(0, WIN_WIDTH // 2 - ROCK_IMG.get_width() - BigRock.GAP_WIDTH)
        self.rock_right.x = self.rock_left.x + ROCK_IMG.get_width() + BigRock.GAP_WIDTH

    def move(self):
        self.rock_left.y += self.VEL
        self.rock_right.y += self.VEL

    def draw(self, win):
        self.rock_left.draw(win)
        self.rock_right.draw(win)

    def collide(self, car):
        # Check collision for both left and right rocks
        return self.rock_left.collide(car) or self.rock_right.collide(car)

    def off_screen(self):
        # Check if the rocks have moved off the bottom of the screen
        return self.rock_left.y > WIN_HEIGHT or self.rock_right.y > WIN_HEIGHT

class Rock:
    VEL = 8

    def __init__(self):
        self.x = random.randint(0, WIN_WIDTH - ROCK_IMG.get_width())
        self.y = -200
        self.ROCK_BOTTOM = ROCK_IMG
        self.passed = False

    def move(self):
        self.y += self.VEL

    def draw(self, win):
        win.blit(self.ROCK_BOTTOM, (self.x, self.y))

    def collide(self, car):
        car_mask = car.get_mask()
        rock_mask = pygame.mask.from_surface(self.ROCK_BOTTOM)
        offset = (self.x - car.x, self.y - round(car.y))
        collision_point = car_mask.overlap(rock_mask, offset)

        return True if collision_point else False

class Coin:
    VEL = 20

    def __init__(self, rock):
        margin = 20
        self.x = random.randint(margin, WIN_WIDTH - COIN_IMG.get_width() - margin)
        while abs(self.x - rock.x) < COIN_IMG.get_width() + ROCK_IMG.get_width():
            self.x = random.randint(margin, WIN_WIDTH - COIN_IMG.get_width() - margin)
        self.y = random.randrange(-500, -250)  # Set initial Y-position of the coin

        self.COIN_BOTTOM = COIN_IMG
        self.passed = False

    def move(self):
        self.y += self.VEL
        # Check if the coin has moved past the bottom of the screen
        if self.y > WIN_HEIGHT:
            self.passed = True  # Mark the coin as passed
            self.reset()  # Reset the coin's position

    def draw(self, win):
        win.blit(self.COIN_BOTTOM, (self.x, self.y))

    def collide(self, car):
        car_mask = car.get_mask()
        coin_mask = pygame.mask.from_surface(self.COIN_BOTTOM)
        offset = (self.x - car.x, self.y - round(car.y))
        collision_point = car_mask.overlap(coin_mask, offset)

        return True if collision_point else False

    def reset(self):
        # Reset the coin's position to the top of the screen after it passes the bottom
        self.x = random.randint(20, WIN_WIDTH - COIN_IMG.get_width() - 20)
        self.y = random.randrange(-500, -250)
        self.passed = False

def draw_window(win, cars, rock, coin, score, road_y):
    win.blit(ROAD_IMG, (0, road_y))
    win.blit(ROAD_IMG, (0, road_y - WIN_HEIGHT))

    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    
    rock.draw(win)
    coin.draw(win)
    
    for car in cars:
        car.draw(win)

    pygame.display.update()

def normalize(value, max_value):
    return value / max_value

def main(genomes, config):
    nets = []
    cars = []
    ge = []

    rock = Rock()
    coin = Coin(rock)
    
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    score = 0
    run = True

    road_y = 0
    
    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car(WIN_WIDTH // 2 - CAR_IMG.get_width() // 2, WIN_HEIGHT - CAR_IMG.get_height()))
        ge.append(genome)

    while run and len(cars) > 0:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        rock.move()
        coin.move()

        # Only reset the rock when it goes off-screen, but do not reset the coin
        if rock.y > WIN_HEIGHT:
            rock = Rock()
            score += 1


        for i, car in enumerate(cars):
            distance_to_left_edge = normalize(car.x, WIN_WIDTH)
            distance_to_right_edge = normalize(WIN_WIDTH - (car.x + car.width), WIN_WIDTH)

            rock_left_edge = rock.x
            rock_right_edge = rock.x + ROCK_IMG.get_width()

            coin_x = normalize(coin.x, WIN_WIDTH)  # Normalized coin X position
            coin_y = normalize(coin.y, WIN_HEIGHT)  # Normalized coin Y position

            output = nets[i].activate((
                distance_to_left_edge,  # Normalized distance from car to the left edge
                distance_to_right_edge,  # Normalized distance from car to the right edge
                rock_left_edge - car.x,  # Distance from car to rock's left edge
                (car.x + car.width) - rock_right_edge,  # Distance from car's right edge to rock's right edge
                rock.y,  # Rock's Y position
                rock.VEL,  # Rock's velocity
                coin_x,  # Coin's X position
                coin_y   # Coin's Y position
            ))

            move_toward_coin = output[1] > 0.5  # New output for whether to prioritize coin collection

            if move_toward_coin:
                if coin.x > car.x:
                    car.move(right=True)
                else:
                    car.move(left=True)
            else:
                if output[0] > 0.5:
                    car.move(right=True)
                else:
                    car.move(left=True)

        to_remove = []
        for i, car in enumerate(cars):
            distance_to_coin = abs(car.x - coin.x)
            
            # Reward the car for proximity to the coin
            ge[i].fitness += (1 - normalize(distance_to_coin, WIN_WIDTH)) * 0.5  # Adjust the factor to tune the reward

            if rock.collide(car):
                ge[i].fitness -= 10
                to_remove.append(i)
            elif coin.collide(car):
                ge[i].fitness += 20  # Increased reward for collecting a coin
                score += 10
                coin.reset()
            elif coin.y > WIN_HEIGHT:
                ge[i].fitness -= 10
                coin.reset()

        for i in reversed(to_remove):
            nets.pop(i)
            cars.pop(i)
            ge.pop(i)

        for genome in ge:
            genome.fitness += 0.1

        road_y += ROAD_SCROLL_SPEED
        if road_y >= WIN_HEIGHT:
            road_y = 0

        draw_window(win, cars, rock, coin, score, road_y)

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 20)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
