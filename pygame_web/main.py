# main.py
import asyncio          
import pygame
from constants import FPS, SCREEN_WIDTH, SCREEN_HEIGHT
from scenes import MenuScene

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("自我之路")
        self.clock = pygame.time.Clock()
        self.scene = MenuScene(self)

    async def run(self):          
        while True:
            events = pygame.event.get()
            self.scene.handle_events(events)
            self.scene.update()
            self.scene.draw(self.screen)
            pygame.display.flip()
            
            await asyncio.sleep(0)   

async def main():
    game = Game()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())