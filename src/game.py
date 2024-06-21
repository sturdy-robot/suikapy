import pygame
import pymunk
import random


def convert_pygame_pos_to_pymunk(pos: tuple[float, float]) -> tuple[float, float]:
    return pos[0], -pos[1] + 600


FRUITS = [
    ("brown4", 20),
    ("blue", 30),
    ("red", 50),
    ("antiquewhite3", 70),
    ("green", 100),
    ("darkorange", 150),
]


class Container(pygame.sprite.Sprite):
    def __init__(self, *args):
        super().__init__(*args)
        size_x = 1200 - 250
        size_y = 1200 - 300
        self.image = pygame.Surface((size_x, size_y))
        self.image.fill("black")
        self.rect = self.image.get_rect()
        self.rect.center = (600, 700)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.shapes = [
            pymunk.Segment(self.body, convert_pygame_pos_to_pymunk(self.rect.topleft), convert_pygame_pos_to_pymunk(self.rect.bottomleft), 0),
            pymunk.Segment(self.body, convert_pygame_pos_to_pymunk(self.rect.bottomleft), convert_pygame_pos_to_pymunk(self.rect.bottomright), 0),
            pymunk.Segment(self.body, convert_pygame_pos_to_pymunk(self.rect.topright), convert_pygame_pos_to_pymunk(self.rect.bottomright), 0),
        ]
        for shape in self.shapes:
            shape.friction = 0.99
            shape.collision_type = 0

    def update(self, dt: float):
        self.body.update_position(self.body, dt)

    def draw(self):
        display = pygame.display.get_surface()
        pygame.draw.rect(display, "black", self.rect)


class Fruit(pygame.sprite.Sprite):
    def __init__(self, radius: int, color: str, pos: tuple[float, float], *args):
        super().__init__(*args)
        self.radius = radius
        self.size = (self.radius, self.radius)
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_frect()
        self.rect.center = pos
        self.body = pymunk.Body(10, 200, body_type=pymunk.Body.DYNAMIC)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.friction = 0.5
        self.shape.collision_type = 2
        self.body.position = convert_pygame_pos_to_pymunk(pos)
        self.color = color

    def update(self):
        self.rect.center = convert_pygame_pos_to_pymunk((self.body.position.x, self.body.position.y))

    def draw(self):
        display = pygame.display.get_surface()
        pygame.draw.circle(display, self.color, self.rect.center, self.radius)


class Spawner(pygame.sprite.Sprite):
    def __init__(self, pos, *args):
        super().__init__(*args)
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_frect()
        self.color = "brown3"
        self.rect.center = pos
        self.radius = 50

    def update(self, xpos: int, dt: float):
        if 125 + self.radius < xpos < 950 - self.radius:
            self.rect.x = xpos

    def get_next_fruit(self, radius: int, color: str):
        self.color = color
        self.radius = radius

    def spawn_fruit(self, space, fruits):
        fruit = Fruit(self.radius, self.color, self.rect.center)
        space.add(fruit.body, fruit.shape)
        fruits.append(fruit)

    def draw(self):
        display = pygame.display.get_surface()
        pygame.draw.line(display, "blue4", (self.rect.center[0], 1200), (self.rect.centerx, self.rect.centery), 2)
        pygame.draw.circle(display, self.color, self.rect.center, self.radius)


def collision_handler(*args):
    return True


class Game:
    def __init__(self):
        pygame.init()
        self.window = pygame.display.set_mode((1200, 1200))
        pygame.display.set_caption("Suikapy")
        self.running = True
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.space = pymunk.Space()
        self.fruits = []
        self.container = Container()
        self.spawner = Spawner((600, 100))
        self.reset_space()

    def run(self):
        while self.running:
            dt = self.clock.tick(self.fps) / 1000
            self.handle_events()
            self.update(dt)
            self.draw()

        pygame.quit()

    def reset_space(self):
        self.space = pymunk.Space()
        self.space.gravity = 0.0, -981.0
        self.fruits = []
        self.container = Container()
        self.space.add(self.container.body)
        for shape in self.container.shapes:
            self.space.add(shape)
        self.space.add_collision_handler(0, 2).pre_solve = collision_handler

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.spawner.spawn_fruit(self.space, self.fruits)
                next_fruit = random.choice(FRUITS)
                self.spawner.get_next_fruit(next_fruit[1], next_fruit[0])
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                self.reset_space()

    def update(self, dt: float):
        self.container.update(dt)
        xpos, _ = pygame.mouse.get_pos()
        self.spawner.update(xpos, dt)
        for body in self.fruits:
            body.update()
        dt = 1.0 / self.fps
        self.space.step(dt)
        pygame.display.set_caption(f"Suikapy - FPS: {int(self.clock.get_fps())}")

    def draw(self):
        self.window.fill("white")
        self.container.draw()
        self.spawner.draw()
        for body in self.fruits:
            body.draw()
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
