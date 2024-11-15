import raylibpy as rl

class PlanetBar:
    def __init__(self, planets):
        """
        Inicializa la barra de selección de planetas.
        
        :param planets: Lista de tipos de planetas disponibles (por ejemplo, "basic", "long_range", etc.).
        """
        self.planets = planets  # Lista de planetas disponibles para seleccionar
        self.placed_planets = []
        self.selected_planet = None  # Planeta seleccionado por el usuario
        self.planet_buttons = self.create_buttons()
        self.preparation_is_able = True
        self.planet_buttons_is_able = True
    
    def create_buttons(self):
        """Crea las posiciones y dimensiones de los botones para cada planeta en la barra."""
        screen_width = 800  # Ajusta según el ancho de tu pantalla
        button_width = 60
        button_height = 60
        padding = 20
        y_position = 550  # Posición vertical cerca de la parte inferior de la pantalla

        buttons = []
        for i, planet in enumerate(self.planets):
            x_position = padding + i * (button_width + padding)
            buttons.append({
                "type": planet.type,
                "rect": (x_position, y_position, button_width, button_height)
            })
        
        return buttons

    def update(self):
        self.check_planet_button_click()


    def draw(self):
        if self.planet_buttons_is_able:
            """Dibuja la barra de selección de planetas y resalta el planeta seleccionado."""
            # Dibuja cada botón en la barra
            for button in self.planet_buttons:
                x, y, width, height = button["rect"]
                color = rl.DARKBLUE if button["type"] != self.selected_planet else rl.SKYBLUE
                rl.draw_rectangle(x, y, width, height, color)
                rl.draw_text(button["type"], x + 5, y + 20, 10, rl.WHITE)

            # Texto de instrucción
            # rl.draw_text("Selecciona un planeta para colocar:", 10, 520, 20, rl.BLACK)
            x_preparation_btn, y_preparation_btn, w_preparation_btn, y_preparation_btn = self.planet_buttons[-1]["rect"]
            self.draw_preparation_button(x_preparation_btn, y_preparation_btn, w_preparation_btn, y_preparation_btn)
        # Dibuja el botón de "Comenzar Ronda" y verifica si se ha presionado
    def draw_preparation_button(self, x , y, width, height):
        if self.preparation_is_able:

            # Dimensiones del botón
            button_x, button_y, button_width, button_height = x, y, width, height
            button_color = rl.DARKBLUE

            # Dibujar el botón
            rl.draw_rectangle(button_x, button_y, button_width, button_height, button_color)
            rl.draw_text("Comenzar Ronda", button_x + 20, button_y + 15, 20, rl.LIGHTGRAY)

        
    def check_preparation_button(self, x , y, width, height):
        if self.preparation_is_able:
            button_x, button_y, button_width, button_height = x, y, width, height
            if rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
                mouse_x, mouse_y = rl.get_mouse_x(), rl.get_mouse_y()
                if button_x < mouse_x < button_x + button_width and button_y < mouse_y < button_y + button_height:
                    self.preparation_is_able = False
                    self.planet_buttons_is_able = False
                    return True
            return False
        
    def check_planet_button_click(self):
        if self.planet_buttons_is_able:
            """Verifica si el usuario ha hecho clic en un botón de planeta y actualiza el planeta seleccionado."""
            if rl.is_mouse_button_down(rl.MOUSE_LEFT_BUTTON):
                mouse_x, mouse_y = rl.get_mouse_x(), rl.get_mouse_y()
                for button in self.planet_buttons:
                    x, y, width, height = button["rect"]
                    if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
                        self.selected_planet = button["type"]
                        print(f"Planeta seleccionado: {self.selected_planet}")

    def draw_selected_planet(self):
        """Dibuja el planeta seleccionado en la posición actual del ratón."""
        if self.selected_planet:
            # Busca el planeta en self.planets con el tipo correspondiente a self.selected_planet
            for planet in self.planets:
                if planet.type == self.selected_planet:
                    # Obtiene la posición del ratón
                    mouse_x, mouse_y = rl.get_mouse_x(), rl.get_mouse_y()
                    planet.position[0] = mouse_x
                    planet.position[1] = mouse_y
                    # Llama al método draw() del planeta encontrado, pasando la posición del ratón
                    planet.draw()
                    break  # Sale del bucle una vez que ha encontrado y dibujado el planeta

    def place_selected_planet(self):
        if self.selected_planet and rl.is_mouse_button_pressed(rl.MOUSE_LEFT_BUTTON):
            print(self.placed_planets)

            for planet in self.planets:
                if planet.type == self.selected_planet:
                    # Obtiene la posición del ratón
                    mouse_x, mouse_y = rl.get_mouse_x(), rl.get_mouse_y()
                    planet.position[0] = mouse_x
                    planet.position[1] = mouse_y
                    # Llama al método draw() del planeta encontrado, pasando la posición del ratón
                    self.placed_planets.append(planet)
                    self.selected_planet = None
                    break  # Sale del bucle una vez que ha encontrado y dibujado el planeta


    def get_placed_planets(self):
        return self.placed_planets             