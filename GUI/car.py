#==================================================
# GUI.CAR | Creacion del objeto del Coche
#==================================================
import pygame
from pygame.math import Vector2

from config.config import load_config

class Car:
    '''
    Objeto → Coche | Carga imagen de su objeto y movimiento 
    '''
    def __init__(self, x, y,angle=0, image_path=None, width=None, height=None):
        config = load_config()

        # == Parametros Bases ==
        self.position = Vector2(x, y)
        self.velocity = 0.0
        self.angle = angle

        # == Parametros Editables ==
        self.max_speed = config["CAR_MAX_SPEED"]
        self.acceleration = config["CAR_ACELERATION"]
        self.friction = config["CAR_FRICTION"]
        self.turn_rate = config["CAR_TURN_RATE"]

        # == Imagen ==
        self.image_path = image_path
        if image_path:
            self.original_image = pygame.image.load(image_path).convert_alpha()
        else:
            self.original_image = None

        # == Reescalado ==
        self.width, self.height = width, height
        if width and height:
            self.set_size(width, height)
        else:
            self.set_size(config["CAR_WIDTH"], config["CAR_HEIGHT"])


    def set_size(self, width, height):
        '''
        Reescalado del tamaño de la imagen
        '''
        self.width = width
        self.height = height
        if self.original_image:
            self.image = pygame.transform.scale(self.original_image, (int(self.width), int(self.height)))
        else:
            self.image = pygame.Surface((int(self.width), int(self.height)))
            self.image.fill((255, 0, 0))


    def update(self, dt, accelerate, reverse, turn_dir):
        '''
        Actualiza el movimiento del Coche
        '''
        # == Movimientos Avance | Retroceso ==
        if accelerate:
            self.velocity += self.acceleration * dt
        elif reverse:
            self.velocity -= self.acceleration * dt
        # == Frenada ==
        else:
            if self.velocity > 0:
                self.velocity = max(0.0, self.velocity - self.friction * dt)
            elif self.velocity < 0:
                self.velocity = min(0.0, self.velocity + self.friction * dt)

        # == Limite velocidad ==
        self.velocity = max(-self.max_speed * 0.4, min(self.velocity, self.max_speed))

        # == Giro ==
        # Solo se ejecuta en movimiento
        if self.velocity != 0 and turn_dir != 0:
            # Depende de cuanto se este moviendo respecto a su velocidad maxima
            speed_ratio = abs(self.velocity) / self.max_speed
            # Invertido marcha atras
            direction_factor = 1 if self.velocity >= 0 else -1
            
            self.angle += turn_dir * self.turn_rate * speed_ratio * direction_factor * dt

        # == Ejecutar movimiento == 
        direction = Vector2(1, 0).rotate(-self.angle)
        self.position += direction * self.velocity * dt


    def draw(self, surface, ppu=32):
        '''
        Dibujado del coche en la pantalla
        '''
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        pixel_pos = self.position * ppu
        rect = rotated_image.get_rect(center=pixel_pos)
        
        surface.blit(rotated_image, rect.topleft)