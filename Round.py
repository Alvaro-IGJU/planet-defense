import raylibpy as rl
import time
from Enemy import Enemy
import random

class Round:
    def __init__(self, attack_duration, planet_bar):
        self.phase = "preparation"  # Inicia en fase de preparación
        self.attack_duration = attack_duration
        self.phase_number = 1
        self.completed_time = None  # Momento en que se completó la ronda
        self.enemies = []
        self.planets = []
        self.planet_bar = planet_bar

    def start_attack_phase(self):
        self.load_enemies()
        self.phase = "attack"
        self.attack_start_time = time.time()

    def update(self):
        # Fase de ataque
        if self.phase == "attack":
            elapsed_time = time.time() - self.attack_start_time
            if len(self.enemies) == 0:
                self.end_round()

        # Fase de "completed": Espera unos segundos o un clic del jugador
        elif self.phase == "completed":
            if self.completed_time is None:
                self.completed_time = time.time()  # Marca el inicio de "completed"

            # Comprueba si han pasado 3 segundos o si el jugador hace clic en "Continuar"
            if  self.check_continue_button():
                self.start_preparation_phase()

    def end_round(self):
        print("¡Ronda terminada!")
        self.phase = "completed"
        self.completed_time = time.time()  # Marca el tiempo en que comienza la fase "completed"
    
    def load_enemies(self):
        """Crea una lista de enemigos, mezclando tipos anteriores y nuevos para aumentar la dificultad en cada ronda."""
        
        # Lista de tipos de enemigos que se van introduciendo progresivamente
        enemy_types = ["fast", "tank", "healer", "leader", "explosive", "evader"]
        
        # Determina el índice máximo de tipos de enemigos disponibles en la ronda actual
        max_type_index = min(len(enemy_types) - 1, self.phase_number // 5)  # Cada 5 rondas añade un nuevo tipo de enemigo
        
        # Total de enemigos para la ronda actual
        num_enemies = self.phase_number * 2
        
        # Ancho de la pantalla para definir el rango de posiciones x
        screen_width = 800  # Ajusta esto al ancho de tu pantalla si es diferente
        
        # Genera una lista de enemigos aleatoria con tipos previos y nuevos hasta max_type_index
        self.enemies = [
            self.create_enemy(
                position=(random.randint(0, screen_width), random.randint(-100, -50)),
                type=enemy_types[random.randint(0, max_type_index)]
            )
            for _ in range(num_enemies)
        ]

    def create_enemy(self, position, type="basic"):
        """Crea un enemigo basado en el tipo y posición dados."""
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
    
    def start_preparation_phase(self):
        self.phase = "preparation"
        self.phase_number += 1
        self.planet_bar.preparation_is_able = True
        self.planet_bar.planet_buttons_is_able = True
        self.completed_time = None  # Reinicia el temporizador de "completed"
        print(f"¡Ronda {self.phase_number} comenzará!")

    def check_continue_button(self):
        # Dibuja el botón "Continuar" en la pantalla y verifica el clic
        button_x, button_y, button_width, button_height = 350, 300, 100, 50
        rl.draw_rectangle(button_x, button_y, button_width, button_height, rl.DARKGREEN)
        rl.draw_text("Continuar", button_x + 10, button_y + 15, 20, rl.WHITE)

        if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            mouse_x, mouse_y = rl.get_mouse_x(), rl.get_mouse_y()
            if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:

                return True  # Retorna True si se hizo clic en el botón
        return False

    def draw_phase_info(self):
        # Dibuja información de la fase actual en la pantalla
        rl.draw_text(f"Fase: {self.phase}", 10, 10, 20, rl.BLACK)
        rl.draw_text(f"Ronda: {self.phase_number}", 10, 40, 20, rl.BLACK)



