from math import sqrt
from Enemy import Enemy

# Función para calcular distancia
def distance(pos1, pos2):
    return sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)

# Función para predecir posición del enemigo
def predict_enemy_position(tower_position, enemy_position, enemy_speed):
    dx = enemy_position[0] - tower_position[0]
    dy = enemy_position[1] - tower_position[1]
    dist = sqrt(dx ** 2 + dy ** 2)
    time_to_hit = dist / enemy_speed
    return (enemy_position[0] + dx / dist * enemy_speed * time_to_hit,
            enemy_position[1] + dy / dist * enemy_speed * time_to_hit)


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
    elif type == "explosive":
        return Enemy(position, health=50, speed=1.5, type="explosive")
    elif type == "evader":
        return Enemy(position, health=40, speed=1.0, type="evader")
    else:
        return Enemy(position)  # Básico por defecto
