import random
from math import sqrt
import raylibpy as rl

# Planeta base
class Tower:
    def __init__(self, position, planet_type="basic"):
        self.position = position
        self.health = 100
        self.range = 250
        self.attack_cooldown = 0
        self.color = rl.BLUE
        self.type = planet_type  # Tipo de planeta: healer, long_range, tank, mine, fast, etc.
        
        # Personalización según el tipo de planeta
        if self.type == "healer":
            self.health = 80  # Un healer tiene menos salud
            self.color = rl.GREEN
            self.heal_radius = 100  # Rango de curación
        elif self.type == "long_range":
            self.range = 400  # Rango más largo
            self.color = rl.YELLOW  # Rango más largo
        elif self.type == "tank":
            self.health = 200  # Más salud, resistente
            self.range = 200  # Rango más pequeño
            self.color = rl.GREY
        elif self.type == "mine":
            self.health = 50  # Las minas son frágiles
            self.range = 50   # Rango limitado a la mina
            self.color = rl.BLACK  # Rango más largo
        elif self.type == "fast":
            self.health = 80  # Menos salud por ser rápido
            self.range = 300  # Rango medio

    def attack(self, enemies):
        # Este método será sobreescrito por cada tipo de planeta para hacer un ataque específico.
        pass

    def heal_allies(self, planets):
        if self.type == "healer":
            for planet in planets:
                if planet != self and self.distance(self.position, planet.position) < self.heal_radius:
                    planet.health = min(planet.health + 1, 100)  # Cura hasta 100 de salud

    def deploy_mine(self, mines):
        if self.type == "mine":
            if random.random() < 0.01:  # Una pequeña probabilidad de colocar una mina
                mine_position = (self.position[0] + random.randint(-50, 50), self.position[1] + random.randint(-50, 50))
                mines.append(Mine(position=mine_position))

    def distance(self, pos1, pos2):
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        return sqrt(dx**2 + dy**2)


# Mina
class Mine:
    def __init__(self, position):
        self.position = position
        self.active = True

    def explode(self, enemies):
        if self.active:
            for enemy in enemies:
                if self.distance(self.position, enemy.position) < 20:  # Radio de explosión
                    enemy.health -= 50  # Daño por mina
                    self.active = False
                    print(f"Mina explotó en {self.position}, dañando al enemigo.")
                    break

    def distance(self, pos1, pos2):
        dx = pos1[0] - pos2[0]
        dy = pos1[1] - pos2[1]
        return sqrt(dx**2 + dy**2)
