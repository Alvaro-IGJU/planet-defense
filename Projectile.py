
# Clase de los proyectiles como rectángulos
class Projectile:
    def __init__(self, position, direction, speed=4.0, width=10, height=5):
        self.position = position
        self.direction = direction
        self.speed = speed
        self.width = width
        self.height = height
        self.active = True

    def move(self):
        self.position = (self.position[0] + self.direction[0] * self.speed,
                         self.position[1] + self.direction[1] * self.speed)

    def get_rect(self):
        # Calcula las coordenadas del rectángulo basado en su posición y tamaño
        return (self.position[0], self.position[1], self.width, self.height)
