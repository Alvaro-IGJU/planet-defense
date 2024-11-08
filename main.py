import raylibpy as rl
from math import sqrt, atan2, degrees
from Enemy import Enemy
from Projectile import Projectile
from Tower import Tower
from functions import distance, predict_enemy_position, create_enemy


# Definir el estado del juego
MENU = 0
GAME = 1

# Estado actual del juego
current_screen = MENU

def main():
    rl.init_window(800, 600, "Menú Principal Raylib")
    rl.set_target_fps(60)
    
    while not rl.window_should_close():
        # Procesar la lógica del menú
        if current_screen == MENU:
            rl.set_window_size(800, 600)
            update_menu()
        elif current_screen == GAME:
            update_game()

        rl.begin_drawing()
        rl.clear_background(rl.DARKGRAY)
        
        if current_screen == MENU:
            draw_menu()
        elif current_screen == GAME:
            draw_game()

        rl.end_drawing()

    rl.close()

def update_menu():
    # Verificar las entradas del ratón o teclado
    if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
        mouse_x, mouse_y = rl.get_mouse_x(), rl.get_mouse_y()

        # Verificar si se hace clic en el botón "Jugar"
        if 300 < mouse_x < 500 and 200 < mouse_y < 250:
            global current_screen
            rl.toggle_fullscreen()  # Alternar entre ventana y pantalla completa

            current_screen = GAME  # Cambiar a la pantalla de juego

        # Verificar si se hace clic en el botón "Salir"
        elif 300 < mouse_x < 500 and 300 < mouse_y < 350:
            rl.close()  # Cerrar el juego

def draw_menu():
    # Dibuja el texto del menú
    rl.draw_text("Menú Principal", 300, 100, 30, rl.LIGHTGRAY)
    
    # Botón de "Jugar"
    rl.draw_rectangle(300, 200, 200, 50, rl.DARKBLUE)
    rl.draw_text("Jugar", 370, 215, 20, rl.LIGHTGRAY)
    
    # Botón de "Salir"
    rl.draw_rectangle(300, 300, 200, 50, rl.DARKBLUE)
    rl.draw_text("Salir", 370, 315, 20, rl.LIGHTGRAY)

def update_game():
    # Lógica del juego (por ejemplo, podrías agregar el código de tu juego aquí)
    if rl.is_key_pressed(rl.KEY_ESCAPE):  # Permitir salir del juego con Escape
        global current_screen
        current_screen = MENU  # Volver al menú principal

def draw_game():
    # Configuración de la ventana

    # Inicialización de la torre, enemigos y proyectiles
    towers = [Tower(position=(400, 500)), Tower(position=(700, 500), planet_type="long_range")]
    enemies = [
        create_enemy(position=(0, 0), type="evader"),  # Agregamos un enemigo evader
        create_enemy(position=(0, 20), type="evader"),  # Agregamos un enemigo evader
        create_enemy(position=(20, 0), type="evader"),  # Agregamos un enemigo evader
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
            
            rl.draw_circle_lines(int(tower.position[0]), int(tower.position[1]), tower.range, rl.BLUE)
            rl.draw_circle(int(tower.position[0]), int(tower.position[1]), 20, tower.color)

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


if __name__ == "__main__":
    main()


