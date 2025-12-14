import sys
import pygame
from pygame.locals import *
import math


class FDFViewer:
    def __init__(self, filename):
        """Инициализация программы и загрузка данных из файла"""
        pygame.init()
        self.width = 1200
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"FDF Viewer - {filename}")
        self.bg_color = (10, 10, 20)
        self.line_color = (100, 200, 255)
        self.axis_color = (255, 100, 100)
        self.scale = 20
        self.angle_x = 0
        self.angle_y = 0
        self.offset_x = self.width // 2
        self.offset_y = self.height // 2
        self.points = []
        self.load_fdf(filename)
        self.auto_scale()

    def load_fdf(self, filename):
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
            for y, line in enumerate(lines):
                row = []
                values = line.strip().split()
                for x, value in enumerate(values):
                    if ',' in value:
                        z_val, color = value.split(',')
                        z = int(z_val)
                    else:
                        z = int(value)
                    row.append((x, y, z))
                self.points.append(row)
        except Exception as e:
            print(f"Ошибка загрузки файла: {e}")
            sys.exit(1)

    def auto_scale(self):
        if not self.points:
            return
        max_dim = max(len(self.points), len(self.points[0]))
        if max_dim > 0:
            self.scale = min(self.width, self.height) / (max_dim * 2)

    def project_point(self, x, y, z):
        cos_x, sin_x = math.cos(self.angle_x), math.sin(self.angle_x)
        cos_y, sin_y = math.cos(self.angle_y), math.sin(self.angle_y)
        x1 = x * cos_y + z * sin_y
        z1 = -x * sin_y + z * cos_y
        y1 = y * cos_x - z1 * sin_x
        z2 = y * sin_x + z1 * cos_x
        iso_x = (x1 - y1) * math.cos(0.46365)
        iso_y = -z2 + (x1 + y1) * math.sin(0.46365)
        screen_x = iso_x * self.scale + self.offset_x
        screen_y = iso_y * self.scale + self.offset_y
        return (screen_x, screen_y)

    def draw_grid(self):
        for y in range(len(self.points)):
            for x in range(len(self.points[y]) - 1):
                x1, y1, z1 = self.points[y][x]
                x2, y2, z2 = self.points[y][x + 1]
                start = self.project_point(x1, y1, z1)
                end = self.project_point(x2, y2, z2)
                pygame.draw.line(self.screen, self.line_color, start, end, 2)
        for y in range(len(self.points) - 1):
            for x in range(len(self.points[y])):
                x1, y1, z1 = self.points[y][x]
                x2, y2, z2 = self.points[y + 1][x]
                start = self.project_point(x1, y1, z1)
                end = self.project_point(x2, y2, z2)
                pygame.draw.line(self.screen, self.line_color, start, end, 2)

    def run(self):
        """Основной цикл программы"""
        clock = pygame.time.Clock()
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
            keys = pygame.key.get_pressed()
            if keys[K_w]:
                self.angle_x += 0.05
            if keys[K_s]:
                self.angle_x -= 0.05
            if keys[K_a]:
                self.angle_y += 0.05
            if keys[K_d]:
                self.angle_y -= 0.05
            if keys[K_PLUS] or keys[K_EQUALS]:
                self.scale *= 1.05
            if keys[K_MINUS]:
                self.scale *= 0.95
            if keys[K_UP]:
                self.offset_y -= 10
            if keys[K_DOWN]:
                self.offset_y += 10
            if keys[K_LEFT]:
                self.offset_x -= 10
            if keys[K_RIGHT]:
                self.offset_x += 10
            if keys[K_r]:
                self.angle_x = 0
                self.angle_y = 0
                self.offset_x = self.width // 2
                self.offset_y = self.height // 2
                self.auto_scale()
            self.screen.fill(self.bg_color)
            self.draw_grid()
            pygame.display.flip()
            clock.tick(60)
        pygame.quit()


def main():
    """Основная функция программы"""
    if len(sys.argv) != 2:
        print("Использование: python lab2.py <karkas.fdf>")
        sys.exit(1)

    filename = sys.argv[1]
    viewer = FDFViewer(filename)
    viewer.run()


if __name__ == "__main__":
    main()
