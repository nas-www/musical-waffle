import pygame
import random

SCREEN_WIDTH = 300 
SCREEN_HEIGHT = 600 
GRID_SIZE = 30 
COLUMNS = SCREEN_WIDTH // GRID_SIZE 
ROWS = SCREEN_HEIGHT // GRID_SIZE 
FPS = 3
 
COLORS = [ 
    (0, 0, 0), 
    (255, 0, 0), 
    (0, 255, 0), 
    (0, 0, 255), 
    (255, 255, 0), 
    (255, 165, 0), 
    (0, 255, 255), 
    (255, 0, 255) 
] 
 
SHAPES = [ 
    [[1, 1, 1, 1]], 
    [[1, 1], [1, 1]], 
    [[0, 1, 0], [1, 1, 1]], 
    [[1, 0, 0], [1, 1, 1]], 
    [[0, 0, 1], [1, 1, 1]], 
    [[0, 1, 1], [1, 1, 0]], 
    [[1, 1, 0], [0, 1, 1]] 
] 

class Tetris:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Tetris')
        self.clock = pygame.time.Clock()
        self.grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)]
        self.current_piece = self.new_piece()
        self.current_piece = self.new_piece() 
        self.next_piece = self.new_piece() 
        self.score = 0 

    def new_piece(self): 
        shape = random.choice(SHAPES) 
        color = random.randint(1, len(COLORS) - 1) 
        return {'shape': shape, 'color': color, 'x': COLUMNS // 2 - len(shape[0]) // 2, 'y': 0} 
    
    def rotate(self, piece): 
        piece['shape'] = [list(row) for row in zip(*piece['shape'][::-1])] 

    def collision(self, piece, dx, dy): 
        for y, row in enumerate(piece['shape']): 
            for x, cell in enumerate(row): 
                if cell and (x + piece['x'] + dx < 0 or x + piece['x'] + dx >= COLUMNS or y + piece['y'] + dy >= ROWS or self.grid[y + piece['y'] + dy][x + piece['x'] + dx]): 
                    return True 
        return False 
    
    def freeze(self): 
        for y, row in enumerate(self.current_piece['shape']): 
            for x, cell in enumerate(row): 
                if cell: 
                    self.grid[y + self.current_piece['y']][x + self.current_piece['x']] = self.current_piece['color'] 
        self.clear_lines() 
        self.current_piece = self.next_piece 
        self.next_piece = self.new_piece() 
        if self.collision(self.current_piece, 0, 0): 
            self.game_over() 

    def clear_lines(self): 
        new_grid = [[0 for _ in range(COLUMNS)] for _ in range(ROWS)] 
        yi = ROWS - 1 
        for y in range(ROWS - 1, -1, -1): 
            if 0 in self.grid[y]: 
                new_grid[yi] = self.grid[y] 
                yi -= 1 
            else: 
                self.score += 1 
        self.grid = new_grid 

    def game_over(self): 
        self.init() 
 
    def draw_grid(self): 
        for y in range(ROWS): 
            for x in range(COLUMNS): 
                color = COLORS[self.grid[y][x]] 
                pygame.draw.rect(self.screen, color, (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE)) 
                pygame.draw.rect(self.screen, (255, 255, 255), (x * GRID_SIZE, y * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1) 

    def draw_piece(self, piece): 
        for y, row in enumerate(piece['shape']): 
            for x, cell in enumerate(row): 
                if cell: 
                    color = COLORS[piece['color']] 
                    pygame.draw.rect(self.screen, color, ((x + piece['x']) * GRID_SIZE, (y + piece['y']) * GRID_SIZE, GRID_SIZE, GRID_SIZE)) 
                    pygame.draw.rect(self.screen, (255, 255, 255), ((x + piece['x']) * GRID_SIZE, (y + piece['y']) * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1) 
    
    
    def run(self): 
        running = True 
        while running: 
            self.screen.fill((0, 0, 0)) 
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    running = False 
                if event.type == pygame.KEYDOWN: 
                    if event.key == pygame.K_LEFT and not self.collision(self.current_piece, -1, 0): 
                        self.current_piece['x'] -= 1
                    if event.key == pygame.K_RIGHT and not self.collision(self.current_piece, 1, 0): 
                        self.current_piece['x'] += 1 
                    if event.key == pygame.K_DOWN and not self.collision(self.current_piece, 0, 1): 
                        self.current_piece['y'] += 1 
                    if event.key == pygame.K_UP: 
                        original_shape = self.current_piece['shape'] 
                        self.rotate(self.current_piece) 
                        if self.collision(self.current_piece, 0, 0): 
                            self.current_piece['shape'] = original_shape
            if not self.collision(self.current_piece, 0, 1): 
                self.current_piece['y'] += 1 
            else: 
                self.freeze() 
            self.draw_grid() 
            self.draw_piece(self.current_piece) 
            pygame.display.flip() 
            self.clock.tick(FPS) 
        pygame.quit() 

if __name__ == "__main__": 
    pygame.init() 
    Tetris().run()


