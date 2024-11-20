# models/text.py
import os
import numpy as np
import pygame
import moderngl


class Text:
    def __init__(
        self,
        app,
        text,
        font_path=None,
        font_size=36,
        color=(1.0, 1.0, 1.0, 1.0),
        position=(0, 0),
    ):  # Position below square
        self.app = app
        self.ctx = app.ctx

        # Pygame font rendering
        if font_path and os.path.exists(font_path):
            font = pygame.font.Font(font_path, font_size)
        else:
            font = pygame.font.Font(None, font_size)
            
        self.text_surface = font.render(
            text, True, (int(color[0] * 255), int(color[1] * 255), int(color[2] * 255))
        )

        # Create texture
        width, height = self.text_surface.get_size()
        self.texture = self.ctx.texture((width, height), 4)
        self.texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
        self.texture.swizzle = "BGRA"
        self.texture.write(pygame.image.tostring(self.text_surface, "BGRA"))

        # Vertex data (adjusted for text positioning)
        self.position = position
        self.vertex_data = self.get_vertex_data()

        # Buffers and shader setup
        self.vbo = self.ctx.buffer(self.vertex_data)
        self.ibo = self.get_indices_buffer_object()
        self.shader_program = self.get_shader_program("text")
        self.vao = self.get_vertex_array_object()

        # Set texture uniform
        self.shader_program["tex"] = 0
        self.texture.use()

    def get_vertex_data(self):
        width, height = self.app.WIN_SIZE

        # Adjust text size and position based on screen
        text_width = self.text_surface.get_width() / width
        text_height = self.text_surface.get_height() / height

        # Flip the vertical texture coordinate (0.0 at top, 1.0 at bottom)
        vertex_data = [
            (
                self.position[0] - text_width / 2,
                self.position[1] - text_height / 2,
                0.0,
                0.0,
                1.0,
            ),  # Bottom-left
            (
                self.position[0] + text_width / 2,
                self.position[1] - text_height / 2,
                0.0,
                1.0,
                1.0,
            ),  # Bottom-right
            (
                self.position[0] + text_width / 2,
                self.position[1] + text_height / 2,
                0.0,
                1.0,
                0.0,
            ),  # Top-right
            (
                self.position[0] - text_width / 2,
                self.position[1] + text_height / 2,
                0.0,
                0.0,
                0.0,
            ),  # Top-left
        ]
        return np.array(vertex_data, dtype=np.float32)

    def get_indices_buffer_object(self):
        indices = [0, 1, 2, 2, 3, 0]
        return self.ctx.buffer(np.array(indices, dtype=np.uint32))

    def get_vertex_array_object(self):
        return self.ctx.vertex_array(
            self.shader_program,
            [(self.vbo, "3f 2f", "in_position", "in_texcoord")],
            index_buffer=self.ibo,
        )

    def get_shader_program(self, shader_name):
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        return self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )

    def render(self):
        self.texture.use()
        self.vao.render(moderngl.TRIANGLES)

    def destroy(self):
        self.vbo.release()
        self.ibo.release()
        self.vao.release()
        self.shader_program.release()
        self.texture.release()
