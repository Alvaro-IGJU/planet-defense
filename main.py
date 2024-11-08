import raylibpy as rl
from math import sqrt, atan2, degrees
from Enemy import Enemy
from Projectile import Projectile
from Tower import Tower
from functions import distance, predict_enemy_position, create_enemy

# Configuración de la ventana
rl.init_window(800, 600, "Defensa de la Torre con IA y Balas Rectangulares")
rl.set_target_fps(60)

# Inicialización de la torre, enemigos y proyectiles
towers = [Tower(position=(400, 500)), Tower(position=(700, 500), planet_type="long_range")]
enemies = [

    create_enemy(position=(0, 0), type="evader"),  # Agregamos un enemigo evader
]
projectiles = []

while not rl.window_should_close():
    for tower in towers:
        if tower.attack_cooldown > 0:
            tower.attack_cooldown -= 1

    # Mueve enemigos hacia la torre y evade proyectiles
    for enemy in enemies:
        # Movimiento hacia la torre o el objetivo
        enemy.move_towards(target_position=(tower.position[0], tower.position[1]))
    
        # Aplicar efectos especiales, como el sanador curando a los cercanos o el líder dando bonificaciones
        enemy.apply_special_effect(enemies, projectiles=projectiles)
        if enemy.is_dead():
            enemies.remove(enemy)  # Eliminar el enemigo de la lista

    # Disparo de la torre con predicción de posición
    for tower in towers:
        if tower.attack_cooldown <= 0:
            for enemy in enemies:
                if distance(tower.position, enemy.position) <= tower.range and enemy.health > 0:
                    predicted_position = predict_enemy_position(tower.position, enemy.position, enemy.speed)
                    dx = predicted_position[0] - tower.position[0]
                    dy = predicted_position[1] - tower.position[1]
                    dist = sqrt(dx ** 2 + dy ** 2)
                    direction = (dx / dist, dy / dist)
                    projectiles.append(Projectile(position=tower.position, direction=direction))
                    tower.attack_cooldown = 30
                    break

    # Mueve proyectiles y verifica colisiones con enemigos
    for projectile in projectiles:
        if projectile.active:
            projectile.move()
            for enemy in enemies:
                # Detecta colisión proyectil-enemigo usando el rectángulo
                enemy_rect = (enemy.position[0] - 5, enemy.position[1] - 5, 10, 10)
                proj_rect = projectile.get_rect()
                if rl.check_collision_recs(proj_rect, enemy_rect):
                    enemy.health -= 100
                    projectile.active = False
                    break

    # Renderiza el juego
    rl.begin_drawing()
    rl.clear_background(rl.RAYWHITE)

    # Dibuja la torre
    for tower in towers:
        rl.draw_circle(int(tower.position[0]), int(tower.position[1]), 20, rl.BLUE)

    # Dibuja los enemigos
    for enemy in enemies:
        if enemy.health > 0:
            rl.draw_circle(int(enemy.position[0]), int(enemy.position[1]), 10, rl.RED)
            health_text = f"{enemy.health}"
            rl.draw_text(health_text, int(enemy.position[0] - len(health_text) * 3), int(enemy.position[1] - 25), 10, rl.RED)

    # Dibuja los proyectiles como rectángulos rotados
    for projectile in projectiles:
        if projectile.active:
            # Calcula el ángulo de la dirección del proyectil
            angle = atan2(projectile.direction[1], projectile.direction[0])
            # Convierte el ángulo a grados
            angle_degrees = degrees(angle)

            # Dibuja el rectángulo con rotación
            rl.draw_rectangle_pro(
                (projectile.position[0], projectile.position[1], projectile.width, projectile.height), 
                (projectile.width / 2, projectile.height / 2),  # Punto de rotación en el centro del rectángulo
                angle_degrees,  # Ángulo de rotación en grados
                rl.BLACK  # Color del proyectil
            )

    # Dibuja el texto de salud de la torre
    for tower in towers:
        tower_health_text = f"{tower.health}"
        rl.draw_text(tower_health_text, int(tower.position[0] - 7), int(tower.position[1] -5 ), 10, rl.BLACK)

    rl.end_drawing()

rl.close_window()
