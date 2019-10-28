import math
import random
import pygame
import util
from spawner import ShimmerFirework, Firework


ROW_COUNT = 6           
COLUMN_COUNT = 7
SQUARESIZE = 100
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE
myfont = pygame.font.SysFont("monospace", 75)
RED = (255,0,0)
size = (width, height)
screen = pygame.display.set_mode(size)

# The little shooter that flies up and explodes
class Sparker:
    size = 3
    colour = [80, 20, 20]
    startVelocity = 100
    minVelocity = 0
    gravityPower = 5

    allSparkers = []

    def __init__(self, pos, colour, velocity, particleSize, sparsity, hasTrail, lifetime,
                 isShimmer=False, radius=0, proportion=0, focusRad=0, weight=0):
        # store firework attributes
        self.targetPos = pos
        self.colour = colour
        self.fwVelocity = velocity
        self.particleSize = particleSize
        self.sparsity = sparsity
        self.hasTrail = hasTrail
        self.fwLifetime = lifetime
        self.isShimmer = isShimmer
        self.radius = radius
        self.proportion = proportion
        self.focusRad = focusRad
        self.weight = weight

        # setup sparker to fly in direction of cursor
        self.pos = [random.uniform(util.SCREEN_SIZE[0] * 1/3, util.SCREEN_SIZE[0] * 2/3),
                    util.SCREEN_SIZE[1]]
        rad = math.atan2(self.targetPos[1] - self.pos[1], self.targetPos[0] - self.pos[0])
        self.direction = [math.cos(rad), math.sin(rad)]
        self.velocity = Sparker.startVelocity

        self.surface = pygame.Surface((Sparker.size, Sparker.size))
        self.surface.fill(Sparker.colour)

        Sparker.allSparkers.append(self)

    def update(self, dt):
        # move
        for axis in (0, 1):
            self.pos[axis] += self.direction[axis] * self.velocity * dt

        # gravity acts
        self.velocity -= Sparker.gravityPower * dt

        # if above target y or going slowly, time to detonate
        if self.pos[1] <= self.targetPos[1] or self.velocity < Sparker.minVelocity:
            self.detonate()

    def draw(self, screen):
        screen.blit(self.surface, self.pos)

    def detonate(self):
        # create the firework object
        if self.isShimmer:
            ShimmerFirework(self.pos, self.colour, self.velocity, self.particleSize, self.sparsity,
                            self.radius, self.proportion, self.focusRad, self.fwLifetime, self.weight)

        else:
            Firework(self.pos, self.colour, self.fwVelocity, self.particleSize,
                 self.sparsity, self.hasTrail, self.fwLifetime)
        label = myfont.render("Player 1 wins!!", 1, RED)
        screen.blit(label, (40, 210))            #updates that specific part of the screen with the label
        game_over = True
        # destroy the sparker
        Sparker.allSparkers.remove(self)