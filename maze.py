import pygame
import random

WIDTH = 600
HEIGHT = 600
CELL_WIDTH = 40
COL = WIDTH // CELL_WIDTH
ROW = HEIGHT // CELL_WIDTH
WHITE = (255,255,255)
BLACK = (0,0,0)


surface =  pygame.display.set_mode((WIDTH, HEIGHT))
surface.fill(WHITE)
clock = pygame.time.Clock()
pygame.display.set_caption('Maze Generator')


def make_grid(rows, cols):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            cell = Cell(i, j, 1)
            grid[i].append(cell)
    return grid


def draw_grid(rows, cols, grid):
    for j in range(cols):
        for i in range(rows):
            cell = grid[i][j]
            cell.draw()

def color_grid(rows, cols, grid):
    for j in range(cols):
        for i in range(rows):
            cell = grid[i][j]
            cell.color((128,128,128))


def remove_walls(current, next):
    if current.i < next.i and current.j == next.j:
        current.walls[1] = False
        next.walls[3] = False
    elif current.i == next.i and current.j < next.j:
        current.walls[2] = False
        next.walls[0] = False
    elif current.i > next.i and current.j == next.j:
        current.walls[3] = False
        next.walls[1] = False
    elif current.i == current.i and current.j > next.j:
        current.walls[0] = False
        next.walls[2] = False
        

class Cell:
    def __init__(self, i, j, width):
        self.walls = [True, True, True, True]
        self.i = i
        self.j = j
        self.x = i * CELL_WIDTH
        self.y = j * CELL_WIDTH
        self.neighbours = []
        self.width = width
        self.is_visited = False


    def draw(self):
        if self.walls[0]:
            pygame.draw.line(surface, BLACK, (self.x, self.y), (self.x + CELL_WIDTH, self.y), self.width)
        if self.walls[1]:
            pygame.draw.line(surface, BLACK, (self.x + CELL_WIDTH, self.y), (self.x + CELL_WIDTH, self.y + CELL_WIDTH), self.width)
        if self.walls[2]:
            pygame.draw.line(surface, BLACK, (self.x + CELL_WIDTH, self.y + CELL_WIDTH), (self.x, self.y + CELL_WIDTH), self.width)
        if self.walls[3]:
            pygame.draw.line(surface, BLACK, (self.x, self.y + CELL_WIDTH), (self.x, self.y), self.width)


    def color(self, color):
        if self.is_visited:
            pygame.draw.rect(surface, color, (self.x, self.y, CELL_WIDTH, CELL_WIDTH))


    def find_neighbour(self):
        neighbour = []
        if self.j != 0:
            top = grid[self.i][self.j - 1]
            if not top.is_visited:
                neighbour.append(top)
        if self.i != ROW - 1:
            right = grid[self.i + 1][self.j]
            if not right.is_visited:
                neighbour.append(right)
        if self.j != COL - 1:
            bottom = grid[self.i][self.j + 1]
            if not bottom.is_visited:
                neighbour.append(bottom)
        if self.i != 0:
            left = grid[self.i - 1][self.j]
            if not left.is_visited:
                neighbour.append(left)
        if len(neighbour) > 0:
            return random.choice(neighbour)
        return None

    



done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True     

    grid = make_grid(ROW, COL)
    draw_grid(ROW, COL, grid)
    stack = []
    current = grid[0][0]
    current.is_visited = True
    stack.append(current)
    while len(stack) > 0:
        current = stack.pop()
        if current.find_neighbour() is not None:
            stack.append(current)
            next = current.find_neighbour()
            remove_walls(current, next)
            next.is_visited = True
            stack.append(next)
            surface.fill(WHITE)
            color_grid(ROW, COL, grid)
            current.color((0,0,0))
            draw_grid(ROW, COL, grid)
            

        pygame.display.update()
        clock.tick(30)
    done = True
pygame.quit()
quit()