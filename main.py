# main.py
import raylibpy as rl
from math import sqrt, atan2, degrees
from Enemy import Enemy
from Projectile import Projectile
from Tower import Tower
from functions import distance, predict_enemy_position
from Round import Round
from PlanetBar import PlanetBar

# Definir el estado del juego
MENU = 0
GAME = 1
current_screen = MENU
planetBar = PlanetBar(
    [Tower(position=(400, 500)),
     Tower(position=(400, 500), planet_type='long_range'),
     Tower(position=(400, 500), planet_type='tank'),
     Tower(position=(400, 500), planet_type='healer'),
     Tower(position=(400, 500), planet_type='fast'),
     ]
    )

# Funciones del menú
def update_menu():
    if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
        mouse_x, mouse_y = rl.get_mouse_x(), rl.get_mouse_y()
        if 300 < mouse_x < 500 and 200 < mouse_y < 250:
            global current_screen
            current_screen = GAME  # Cambiar a la pantalla de juego
        elif 300 < mouse_x < 500 and 300 < mouse_y < 350:
            rl.close()  # Cerrar el juego

def draw_menu():
    rl.draw_text("Menú Principal", 300, 100, 30, rl.LIGHTGRAY)
    rl.draw_rectangle(300, 200, 200, 50, rl.DARKBLUE)
    rl.draw_text("Jugar", 370, 215, 20, rl.LIGHTGRAY)
    rl.draw_rectangle(300, 300, 200, 50, rl.DARKBLUE)
    rl.draw_text("Salir", 370, 315, 20, rl.LIGHTGRAY)

# Funciones del juego
def update_game(towers, enemies, projectiles, round_instance):
    if round_instance.phase == "attack":
        update_towers(towers)
        move_enemies(enemies, towers, projectiles)
        shoot_projectiles(towers, enemies, projectiles)
        move_projectiles(projectiles, enemies)

def update_towers(towers):
    for tower in towers:
        if tower.attack_cooldown > 0:
            tower.attack_cooldown -= 1

def move_enemies(enemies, towers, projectiles):
    for enemy in enemies:
        closest_tower = min(towers, key=lambda t: distance(t.position, enemy.position))
        enemy.move_towards(target_position=closest_tower.position)
        enemy.apply_special_effect(enemies, projectiles=projectiles)
        if enemy.is_dead():
            enemies.remove(enemy)

def shoot_projectiles(towers, enemies, projectiles):
    for tower in towers:
        if tower.attack_cooldown <= 0:
            for enemy in enemies:
                if distance(tower.position, enemy.position) <= tower.range and enemy.health > 0:
                    predicted_position = predict_enemy_position(tower.position, enemy.position, enemy.speed)
                    dx, dy = predicted_position[0] - tower.position[0], predicted_position[1] - tower.position[1]
                    dist = sqrt(dx ** 2 + dy ** 2)
                    direction = (dx / dist, dy / dist)
                    projectiles.append(Projectile(position=tower.position, direction=direction, speed= tower.attack_speed))
                    tower.attack_cooldown = 30
                    break

def move_projectiles(projectiles, enemies):
    for projectile in projectiles:
        if projectile.active:
            projectile.move()
            for enemy in enemies:
                enemy_rect = (enemy.position[0] - 5, enemy.position[1] - 5, 10, 10)
                proj_rect = projectile.get_rect()
                if rl.check_collision_recs(proj_rect, enemy_rect):
                    enemy.health -= 100
                    projectile.active = False
                    break

def draw_game(towers, enemies, projectiles, round_instance):
    rl.clear_background(rl.RAYWHITE)
    round_instance.draw_phase_info()  # Muestra el estado de la ronda

    # Dibuja el botón de preparación si estamos en esa fase
    if round_instance.phase == "preparation":
        planetBar.draw_selected_planet()
        planetBar.place_selected_planet()
        for planet in planetBar.get_placed_planets():
            print("SE DIBUJA PLANETA ", planet.type)
            planet.draw()
        x_preparation_btn, y_preparation_btn, w_preparation_btn, y_preparation_btn = planetBar.planet_buttons[-1]["rect"]
        if planetBar.check_preparation_button(x_preparation_btn, y_preparation_btn, w_preparation_btn, y_preparation_btn):
            round_instance.start_attack_phase()

    # Dibuja torres, enemigos y proyectiles solo si estamos en fase de ataque
    if round_instance.phase == "attack":
        for tower in towers:
            tower.draw()
        for enemy in enemies:
            if enemy.health > 0:
                enemy.draw()
        for projectile in projectiles:
            if projectile.active:
                projectile.draw()

def main():
    rl.init_window(800, 600, "Defensa de la Torre")
    rl.set_target_fps(60)

    # Inicialización de torres, enemigos, proyectiles y ronda
    towers = planetBar.get_placed_planets()
 
    projectiles = []
    round_instance = Round(attack_duration=60, planet_bar= planetBar)  # La duración de ataque se maneja en la ronda
    while not rl.window_should_close():
        rl.begin_drawing()
        rl.clear_background(rl.DARKGRAY)
        
        if current_screen == MENU:
            update_menu()
            draw_menu()
        elif current_screen == GAME:
            round_instance.update()  # Actualizar ronda en cada fotograma
            planetBar.draw()
            planetBar.update()
            update_game(towers, round_instance.enemies, projectiles, round_instance)
            draw_game(towers, round_instance.enemies, projectiles, round_instance)
        
        rl.end_drawing()

    rl.close_window()

if __name__ == "__main__":
    main()
