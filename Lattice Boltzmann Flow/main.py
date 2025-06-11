from graphics import Canvas
import math
import random

CANVAS_WIDTH = 400
CANVAS_HEIGHT = 400
PARTICLE_COUNT = 200
PARTICLE_RADIUS = 2
FLOW_VELOCITY = 2.0
CYLINDER_RADIUS = 30
CYLINDER_CENTER_X = CANVAS_WIDTH // 4
CYLINDER_CENTER_Y = CANVAS_HEIGHT // 2
WAKE_LENGTH = 60
STREAMLINE_STEP = 4

STREAMLINE_COLORS = [
    "red", "orange", "yellow", "green", "cyan", "blue", "magenta"
]

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.oval = None
        self.path = []
        self.color_index = random.randint(0, len(STREAMLINE_COLORS) - 1)

    def update(self, canvas):
        dx = FLOW_VELOCITY
        dy = 0

        rx = self.x - CYLINDER_CENTER_X
        ry = self.y - CYLINDER_CENTER_Y
        r = math.hypot(rx, ry)

        if r > CYLINDER_RADIUS:
            theta = math.atan2(ry, rx)
            u_r = FLOW_VELOCITY * (1 - (CYLINDER_RADIUS ** 2) / (r ** 2)) * math.cos(theta)
            u_theta = -FLOW_VELOCITY * (1 + (CYLINDER_RADIUS ** 2) / (r ** 2)) * math.sin(theta)

            dx = u_r * math.cos(theta) - u_theta * math.sin(theta)
            dy = u_r * math.sin(theta) + u_theta * math.cos(theta)

            if CYLINDER_CENTER_X < self.x < CYLINDER_CENTER_X + WAKE_LENGTH and abs(self.y - CYLINDER_CENTER_Y) < CYLINDER_RADIUS:
                dx *= 0.5
                dy *= 0.5

        dx += random.uniform(-0.2, 0.2)
        dy += random.uniform(-0.2, 0.2)

        self.x += dx
        self.y += dy

        if self.x > CANVAS_WIDTH or self.y < 0 or self.y > CANVAS_HEIGHT:
            self.x = 0
            self.y = random.uniform(0, CANVAS_HEIGHT)
            self.path.clear()
            self.color_index = random.randint(0, len(STREAMLINE_COLORS) - 1)

        speed = math.hypot(dx, dy)
        gray = min(255, max(0, int(50 + speed * 40)))
        color = f'rgb({gray},{gray},{gray})'

        if self.oval is None:
            self.oval = canvas.create_oval(self.x - PARTICLE_RADIUS, self.y - PARTICLE_RADIUS,
                                           self.x + PARTICLE_RADIUS, self.y + PARTICLE_RADIUS,
                                           color)
        else:
            canvas.moveto(self.oval, self.x - PARTICLE_RADIUS, self.y - PARTICLE_RADIUS)
            canvas.set_color(self.oval, color)

        # Streamlines
        self.path.append((self.x, self.y))
        streamline_color = STREAMLINE_COLORS[self.color_index]
        if len(self.path) > 2:
            for i in range(1, len(self.path)):
                x1, y1 = self.path[i - 1]
                x2, y2 = self.path[i]
                canvas.create_line(x1, y1, x2, y2, streamline_color)


def main():
    canvas = Canvas(CANVAS_WIDTH, CANVAS_HEIGHT)

    canvas.create_oval(CYLINDER_CENTER_X - CYLINDER_RADIUS, CYLINDER_CENTER_Y - CYLINDER_RADIUS,
                       CYLINDER_CENTER_X + CYLINDER_RADIUS, CYLINDER_CENTER_Y + CYLINDER_RADIUS,
                       'blue')

    particles = [Particle(random.uniform(0, CANVAS_WIDTH), random.uniform(0, CANVAS_HEIGHT))
                 for _ in range(PARTICLE_COUNT)]

    while True:
        for particle in particles:
            particle.update(canvas)

if __name__ == '__main__':
    main()
