from math import sqrt

def distance(pos1, pos2):
    dx = pos1[0] - pos2[0]
    dy = pos1[1] - pos2[1]
    return sqrt(dx**2 + dy**2)

# Clase del enemigo
class Enemy:
    def __init__(self, position, health=50, speed=1.5, type="basic"):
        self.position = position
        self.health = health
        self.speed = speed
        self.type = type  # Tipo de enemigo (por ejemplo: 'basic', 'fast', 'tank', 'healer', 'leader', 'evader')
    
    def move_towards(self, target_position):
        dx = target_position[0] - self.position[0]
        dy = target_position[1] - self.position[1]
        dist = sqrt(dx**2 + dy**2)
        if dist > 0:
            self.position = (self.position[0] + dx / dist * self.speed,
                             self.position[1] + dy / dist * self.speed)

    def evade_projectiles(self, projectiles):
        for projectile in projectiles:
            if projectile.active and distance(self.position, projectile.position) < 50:
                # Evitar proyectiles cambiando de posición en dirección opuesta a su trayectoria
                self.position = (self.position[0] + (projectile.direction[1] * 5),
                                 self.position[1] - (projectile.direction[0] * 5))

    def apply_special_effect(self, other_enemies, projectiles=None):
        if self.type == "healer":
            for enemy in other_enemies:
                if distance(self.position, enemy.position) < 100:  # Si están cerca
                    enemy.health += 1  # Cura 1 de salud
        elif self.type == "leader":
            for enemy in other_enemies:
                if distance(self.position, enemy.position) < 100:  # Si están cerca
                    enemy.speed += 0.2  # Aumenta su velocidad
        elif self.type == "evader":

            # Si es un evader, esquiva los proyectiles
            if projectiles:
                print("ESQUIVA")
                self.evade_projectiles(projectiles)
        # Puedes seguir agregando otros efectos especiales para otros tipos de enemigos.

    def is_dead(self):
        return self.health <= 0
    
# Función de creación de enemigos para facilitar el manejo
def create_enemy(position, type="basic"):
    if type == "fast":
        return Enemy(position, health=40, speed=3.0, type="fast")
    elif type == "tank":
        return Enemy(position, health=200, speed=0.8, type="tank")
    elif type == "healer":
        return Enemy(position, health=60, speed=1.2, type="healer")
    elif type == "leader":
        return Enemy(position, health=80, speed=1.0, type="leader")
    elif type == "evader":
        return Enemy(position, health=50, speed=2.5, type="evader")  # Evader es rápido y escurridizo
    else:
        return Enemy(position)  # Básico por defecto
