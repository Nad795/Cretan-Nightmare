#pencarian jalur pake BFS

import pygame
from map import Map
import random
import time

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Hint:
    def __init__(self, game_map):
        self.game_map = game_map
        self.hint_path = []
        self.position = self.generate_random_position()
        self.last_collected_time = 0
        self.cooldown = 30  

    def generate_hint_path(self, start, end, steps=20):
        stack = [start]
        visited = set()
        visited.add(start)
        path = []

        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

        while stack and len(path) < steps:
            current = stack.pop()
            path.append(current)

            if current == end:
                break

            random.shuffle(directions)
            for direction in directions:
                nx, ny = current[0] + direction[0], current[1] + direction[1]
                if 0 <= nx < self.game_map.rows and 0 <= ny < self.game_map.cols and (nx, ny) not in visited:
                    if self.game_map.grid[ny][nx] == 0: 
                        stack.append((nx, ny))
                        visited.add((nx, ny))

        self.hint_path = path

    def generate_random_position(self):
        while True:
            x = random.randint(0, self.game_map.cols - 1)
            y = random.randint(0, self.game_map.rows - 1)
            if self.game_map.grid[y][x] == 0: 
                return (x, y)

    def collect(self, player_position):
        if player_position == self.position and time.time() - self.last_collected_time > self.cooldown:
            self.generate_hint_path(player_position, (self.game_map.cols - 1, self.game_map.rows - 1))
            self.last_collected_time = time.time()
            return True
        return False

    def render(self, screen, cell_size):
        pygame.draw.rect(screen, GREEN, (self.position[0] * cell_size, self.position[1] * cell_size, cell_size, cell_size))

    def render_hint_path(self, screen, cell_size):
        for (x, y) in self.hint_path:
            pygame.draw.rect(screen, WHITE, (x * cell_size, y * cell_size, cell_size, cell_size))
