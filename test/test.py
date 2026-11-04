import os
import pygame
from pygame.math import Vector2


class Car:
    def __init__(self, x, y, angle=0.0, image_path=None, width=80, height=42):
        self.position = Vector2(x, y)
        self.velocity = 0.0          # Velocidad actual
        self.angle = angle

        # --- PARÁMETROS DE CONDUCCIÓN HÍBRIDA ---
        self.max_speed = 8.0        # Velocidad máxima
        self.acceleration = 25.0     # Ligera aceleración (alcanza el tope rápido)
        self.friction = 15.0         # Freno/rozamiento natural suave al soltar tecla
        self.turn_rate = 200.0       # Velocidad base de giro (grados/seg)

        # Carga y escalado de la imagen
        self.image_path = image_path
        if image_path:
            self.original_image = pygame.image.load(image_path).convert_alpha()
        else:
            self.original_image = None

        self.set_size(width, height)

    def set_size(self, width, height):
        self.width = width
        self.height = height
        if self.original_image:
            self.image = pygame.transform.scale(self.original_image, (int(self.width), int(self.height)))
        else:
            self.image = pygame.Surface((int(self.width), int(self.height)))
            self.image.fill((255, 0, 0))

    def update(self, dt, accelerate, reverse, turn_dir):
        # 1. Aceleración / Marcha atrás con ligera inercia
        if accelerate:
            self.velocity += self.acceleration * dt
        elif reverse:
            self.velocity -= self.acceleration * dt
        else:
            # Rozamiento natural para frenar de forma suave pero rápida
            if self.velocity > 0:
                self.velocity = max(0.0, self.velocity - self.friction * dt)
            elif self.velocity < 0:
                self.velocity = min(0.0, self.velocity + self.friction * dt)

        # Limitar la velocidad máxima
        self.velocity = max(-self.max_speed * 0.4, min(self.velocity, self.max_speed))

        # 2. Giro (SÓLO SI ESTÁ EN MOVIMIENTO)
        if self.velocity != 0 and turn_dir != 0:
            # Factor de giro: depende de cuánto se esté moviendo respecto a su velocidad máxima
            speed_ratio = abs(self.velocity) / self.max_speed
            # Girar en el sentido correcto (marcha atrás invierte la dirección lógica)
            direction_factor = 1 if self.velocity >= 0 else -1
            
            self.angle += turn_dir * self.turn_rate * speed_ratio * direction_factor * dt

        # 3. Mover la posición
        direction = Vector2(1, 0).rotate(-self.angle)
        self.position += direction * self.velocity * dt

    def draw(self, surface, ppu=32):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        pixel_pos = self.position * ppu
        rect = rotated_image.get_rect(center=pixel_pos)
        surface.blit(rotated_image, rect.topleft)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Car - Control Híbrido Equilibrado")
        width = 1280
        height = 720
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False

    def run(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        image_path = os.path.join(current_dir, "car.png")
        ppu = 32

        car = Car(x=10, y=10, image_path=image_path)

        while not self.exit:
            dt = self.clock.get_time() / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            pressed = pygame.key.get_pressed()

            # Capturar las entradas
            accelerate = pressed[pygame.K_UP]
            reverse = pressed[pygame.K_DOWN]
            
            turn_dir = 0
            if pressed[pygame.K_LEFT]:
                turn_dir += 1
            if pressed[pygame.K_RIGHT]:
                turn_dir -= 1

            # Actualizar la física equilibrada del coche
            car.update(dt, accelerate, reverse, turn_dir)

            # Dibujar
            self.screen.fill((0, 0, 0))
            car.draw(self.screen, ppu)
            pygame.display.flip()

            self.clock.tick(self.ticks)

        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()