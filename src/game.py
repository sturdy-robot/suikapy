import pygame
import pymunk
import random

from enum import Enum, auto

def convert_pygame_pos_to_pymunk(pos: tuple[float, float]) -> tuple[float, float]:
    return pos[0], -pos[1] + 600


class FruitType(Enum):
    CHERRY = auto()
    STRAWBERRY = auto()
    ORANGE = auto()
    LEMON = auto()
    PEACH = auto()
    APPLE = auto()
    COCONUT = auto()
    PEAR = auto()
    PINEAPPLE = auto()
    MELON = auto()
    WATERMELON = auto()


FRUITS = {
    FruitType.CHERRY: ("blue4", 20),
    FruitType.STRAWBERRY: ("brown1", 30),
    FruitType.ORANGE: ("darkorange", 40),
    FruitType.LEMON: ("darkolivegreen3", 50),
    FruitType.PEACH: ("darkorchid", 70),
    FruitType.APPLE: ("red", 90),
    FruitType.COCONUT: ("saddlebrown", 120),
    FruitType.PEAR: ("salmon", 150),
    FruitType.PINEAPPLE: ("gold", 170),
    FruitType.MELON: ("springgreen", 190),
    FruitType.WATERMELON: ("green4", 200),
}


FRUIT_SCORES = {
    FruitType.CHERRY: 1,
    FruitType.STRAWBERRY: 2,
    FruitType.ORANGE: 4,
    FruitType.LEMON: 8,
    FruitType.PEACH: 16,
    FruitType.APPLE: 32,
    FruitType.COCONUT: 64,
    FruitType.PEAR: 128,
    FruitType.PINEAPPLE: 256,
    FruitType.MELON: 512,
    FruitType.WATERMELON: 1024,
}


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
    def __init__(self, fruit_type: FruitType, pos: tuple[float, float], *args):
        super().__init__(*args)
        self.fruit_type = fruit_type
        self.color, self.radius = FRUITS[self.fruit_type]
        self.size = (self.radius, self.radius)
        self.image = pygame.Surface(self.size)
        self.rect = self.image.get_frect()
        self.rect.center = pos
        self.body = pymunk.Body(10, 200, body_type=pymunk.Body.DYNAMIC)
        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.friction = 0.75
        self.shape.collision_type = 2
        self.body.position = convert_pygame_pos_to_pymunk(pos)

    def update(self):
        self.rect.center = convert_pygame_pos_to_pymunk((self.body.position.x, self.body.position.y))

    def draw(self):
        display = pygame.display.get_surface()
        pygame.draw.circle(display, self.color, self.rect.center, self.radius)
        pygame.draw.circle(display, "black", self.rect.center, self.radius, 3)


class Spawner(pygame.sprite.Sprite):
    def __init__(self, pos, *args):
        super().__init__(*args)
        self.image = pygame.Surface((20, 20))
        self.rect = self.image.get_frect()
        self.rect.center = pos
        self.current_fruit: FruitType = FruitType.CHERRY
        self.color, self.radius = FRUITS[self.current_fruit]
        self.set_fruit_spawner()

    def update(self, xpos: int, dt: float):
        if 125 + self.radius < xpos < 1050 - self.radius:
            self.rect.x = xpos

    def set_fruit_spawner(self, fruit: FruitType = FruitType.CHERRY):
        self.current_fruit = fruit
        self.color, self.radius = FRUITS[fruit]

    def draw(self):
        display = pygame.display.get_surface()
        pygame.draw.line(display, "blue4", (self.rect.center[0], 1200), (self.rect.centerx, self.rect.centery), 3)
        pygame.draw.circle(display, self.color, self.rect.center, self.radius)
        pygame.draw.circle(display, "black", self.rect.center, self.radius, 3)


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
        self.fruits_enabled = [FruitType.CHERRY]
        self.rounds = 0
        self.score = 0
        self.score_font = pygame.freetype.Font(None, 20)
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
        self.rounds = 0
        self.fruits_enabled = [FruitType.CHERRY]
        self.next_fruit = FruitType.CHERRY
        self.spawner.set_fruit_spawner()
        self.score = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                self.rounds += 1
                fruit = Fruit(self.spawner.current_fruit, self.spawner.rect.center)
                self.add_fruit(fruit)
                self.spawner.set_fruit_spawner(self.next_fruit)
                self.get_next_fruit()
            if event.type == pygame.KEYUP and event.key == pygame.K_r:
                self.reset_space()

    def check_collisions(self):
        for fruit in self.fruits:
            for fruit2 in self.fruits:
                if fruit == fruit2:
                    continue
                
                if fruit.fruit_type == fruit2.fruit_type:
                    fruit1_vec = pygame.Vector2(fruit.rect.center)
                    fruit2_vec = pygame.Vector2(fruit2.rect.center)
                    if fruit1_vec.distance_to(fruit2_vec) <= fruit.radius + fruit2.radius:
                        self.merge_fruits(fruit, fruit2)

    def add_fruit(self, fruit: Fruit):
        self.fruits.append(fruit)
        self.space.add(fruit.body, fruit.shape)
        self.score += FRUIT_SCORES[fruit.fruit_type]

    def remove_fruit(self, fruit: Fruit):
        if fruit in self.fruits:
            self.fruits.remove(fruit)

        if fruit.body in self.space.bodies or fruit.shape in self.space.shapes:
            self.space.remove(fruit.body, fruit.shape)

    def get_next_fruit(self):
        self.next_fruit = FruitType.CHERRY

        if self.rounds >= 3 and FruitType.STRAWBERRY not in self.fruits_enabled:
            self.fruits_enabled.append(FruitType.STRAWBERRY)
        elif self.rounds >= 7 and FruitType.ORANGE not in self.fruits_enabled:
            self.fruits_enabled.append(FruitType.ORANGE)
        elif self.rounds >= 10 and FruitType.LEMON not in self.fruits_enabled:
            self.fruits_enabled.append(FruitType.LEMON)
        elif self.rounds >= 15 and FruitType.PEACH not in self.fruits_enabled:
            self.fruits_enabled.append(FruitType.PEACH)

        self.next_fruit = random.choice(self.fruits_enabled)

    def merge_fruits(self, fruit1: Fruit, fruit2: Fruit):
        new_fruit = FruitType.CHERRY
        if fruit1.fruit_type == FruitType.CHERRY:
            new_fruit = FruitType.STRAWBERRY
        if fruit1.fruit_type == FruitType.STRAWBERRY:
            new_fruit = FruitType.ORANGE
        elif fruit1.fruit_type == FruitType.ORANGE:
            new_fruit = FruitType.LEMON
        elif fruit1.fruit_type == FruitType.LEMON:
            new_fruit = FruitType.PEACH
        elif fruit1.fruit_type == FruitType.PEACH:
            new_fruit = FruitType.APPLE
        elif fruit1.fruit_type == FruitType.APPLE:
            new_fruit = FruitType.COCONUT
        elif fruit1.fruit_type == FruitType.COCONUT:
            new_fruit = FruitType.PEAR
        elif fruit1.fruit_type == FruitType.PEAR:
            new_fruit = FruitType.PINEAPPLE
        elif fruit1.fruit_type == FruitType.PINEAPPLE:
            new_fruit = FruitType.MELON
        elif fruit1.fruit_type == FruitType.MELON:
            new_fruit = FruitType.WATERMELON

        new_fruit_obj = Fruit(new_fruit, fruit1.rect.center)
        self.remove_fruit(fruit1)
        self.remove_fruit(fruit2)
        if fruit1.fruit_type != FruitType.WATERMELON:
            self.add_fruit(new_fruit_obj)
        else:
            self.score += 1024

    def update(self, dt: float):
        self.container.update(dt)
        xpos, _ = pygame.mouse.get_pos()
        self.spawner.update(xpos, dt)
        self.check_collisions()
        for body in self.fruits:
            body.update()
        dt = 1.0 / self.fps
        self.space.step(dt)
        pygame.display.set_caption(f"Suikapy - FPS: {int(self.clock.get_fps())}")

    def draw_score(self):
        score_text, score_rect = self.score_font.render(f"Score: {self.score}", "black", size=22)
        score_rect.topleft = self.window.get_rect().topleft
        score_rect.y += 5
        score_rect.x += 10
        self.window.blit(score_text, score_rect)

    def draw_next_fruit(self):
        next_fruit_text, next_fruit_rect = self.score_font.render("Next:", "black", size=22)
        next_fruit_rect.topright = self.window.get_rect().topright
        radius = 20
        fruit_rect = pygame.Rect(0, 0, radius, radius)
        fruit_rect.topright = next_fruit_rect.topright
        fruit_rect.centerx -= int(next_fruit_rect.width / 2) + radius
        fruit_rect.centery += radius
        next_fruit_rect.centerx = fruit_rect.x
        next_fruit_rect.centerx -= fruit_rect.width + 2 * radius 
        self.window.blit(next_fruit_text, next_fruit_rect)
        
        pygame.draw.circle(self.window, FRUITS[self.next_fruit][0], fruit_rect.center, radius)
        pygame.draw.circle(self.window, "black", fruit_rect.center, radius, width=3)

    def draw(self):
        self.window.fill("white")
        self.container.draw()
        self.draw_score()
        self.draw_next_fruit()
        self.spawner.draw()
        for body in self.fruits:
            body.draw()
        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
