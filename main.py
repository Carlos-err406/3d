import pygame
import sys
import moderngl

# from models.triangle import Triangle
from models.square import Square
from models.text import Text


class GraphicsEngine:
    def __init__(self):
        pygame.init()
        infoObject = pygame.display.Info()
        self.WIN_SIZE = (infoObject.current_w, infoObject.current_h)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(
            pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE
        )
        pygame.display.set_mode(
            self.WIN_SIZE,
            pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE,
        )
        self.ctx = moderngl.create_context()

        # enable alpha channel for colors
        self.ctx.enable(moderngl.BLEND)
        self.ctx.blend_func = (moderngl.SRC_ALPHA, moderngl.ONE_MINUS_SRC_ALPHA)

        self.clock = pygame.time.Clock()

        square = Square(self, rotation=45, color=(1, 1, 1, 0.8))
        text = Text(
            self,
            "OMEN",
            position=(0, -0.4),
            font_size=120,
            font_path="fonts/hewlett-packard.otf",
        )
        self.text = text
        self.scene = square

    def check_events(self):
        def _is_quitting(event):
            return event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            )

        for event in pygame.event.get():
            if _is_quitting(event):
                self.scene.destroy()
                pygame.quit()
                sys.exit()

    def render(self):
        self.ctx.clear(color=(0, 0, 0.1))
        self.scene.render()
        self.text.render()
        pygame.display.flip()

    def run(self):
        while True:
            self.check_events()

            # self.scene.rotation = self.scene.rotation - 0.1
            # self.scene.rotate(self.scene.rotation - 0.1)

            self.render()
            self.clock.tick(60)


if __name__ == "__main__":
    app = GraphicsEngine()
    app.run()
