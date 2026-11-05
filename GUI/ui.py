#==================================================
# GUI.UI | Codigo principal donde funciona el juego
#==================================================
from pathlib import Path
import pygame

from config.config import load_config
from GUI.car import Car

class Game:
    '''
    Pantalla principal del juego
    '''
    def __init__(self):
        config = load_config()

        # == Parametros base ==
        pygame.init()
        pygame.display.set_caption(config["NAME"])
        width = config["SCREEN_WIDTH"]
        height = config["SCREEN_HEIGHT"]
        self.screen = pygame.display.set_mode((width, height))
        self.clock = pygame.time.Clock()
        self.ticks = 60
        self.exit = False


    def run(self):
        ''''
        Corre la imagen principal del juego
        '''
        image_path = Path(__file__).resolve().parent.parent / "assets" / "car.png"
        config = load_config()
        ppu = 32

        # == Creacion del Objeto Coche ==
        car = Car(x=config["SCREEN_CAR_INIT_X"], 
                  y=config["SCREEN_CAR_INIT_X"], 
                  image_path=image_path)

        # == Bucle Principal | (Imagen) ==
        while not self.exit:
            dt = self.clock.get_time() / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            pressed = pygame.key.get_pressed()

            # == Teclas ==
            accelerate = pressed[pygame.K_UP]
            reverse = pressed[pygame.K_DOWN]
            
            turn_dir = 0
            if pressed[pygame.K_LEFT]:
                turn_dir += 1
            if pressed[pygame.K_RIGHT]:
                turn_dir -= 1

            # == Actualizacion del Coche ==
            car.update(dt, accelerate, reverse, turn_dir)

            # == Dibujado en pantalla ==
            self.screen.fill((0, 0, 0))
            car.draw(self.screen, ppu)
            pygame.display.flip()

            self.clock.tick(self.ticks)

        pygame.quit()