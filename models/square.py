import numpy
import moderngl


class Square:
    def __init__(self, app):
        self.app = app
        self.ctx = app.ctx
        self.ibo = self.get_indices_buffer_object()
        self.vbo = self.get_vertex_buffer_object()
        self.shader_program = self.get_shader_program("default")
        self.vao = self.get_vertex_array_object()

    def render(self):
        self.vao.render(moderngl.TRIANGLES)

    def destroy(self):
        self.vbo.release()
        self.shader_program.release()
        self.vao.release()

    def get_vertex_array_object(self):
        vao = self.ctx.vertex_array(
            self.shader_program,
            [(self.vbo, "3f", "in_position")],
            index_buffer=self.ibo,
        )
        return vao

    def get_vertex_data(self):
        # Get the window dimensions
        width, height = self.app.WIN_SIZE

        # Calculate aspect ratio
        aspect_ratio = width / height

        # Adjust vertex coordinates to maintain square shape
        # Scale based on the narrower dimension
        if aspect_ratio > 1:
            # Wider screen: scale x coordinates
            scale_x = 1 / aspect_ratio
            scale_y = 1.0
        else:
            # Taller screen: scale y coordinates
            scale_x = 1.0
            scale_y = aspect_ratio

        vertex_data = [
            (-0.5 * scale_x, -0.5 * scale_y, 0.0),  # bottom-left
            (0.5 * scale_x, -0.5 * scale_y, 0.0),  # bottom-right
            (0.5 * scale_x, 0.5 * scale_y, 0.0),  # top-right
            (-0.5 * scale_x, 0.5 * scale_y, 0.0),  # top-left
        ]
        vertex_data = numpy.array(vertex_data, dtype=numpy.float32)
        return vertex_data

    def get_indices_buffer_object(self):
        indices = [0, 1, 2, 2, 3, 0]  # first triangle  # second triangle
        indices = numpy.array(indices, dtype=numpy.uint32)
        ibo = self.ctx.buffer(indices)
        return ibo

    def get_vertex_buffer_object(self):
        vertex_data = self.get_vertex_data()
        vbo = self.ctx.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name):
        with open(f"shaders/{shader_name}.vert") as file:
            vertex_shader = file.read()
        with open(f"shaders/{shader_name}.frag") as file:
            fragment_shader = file.read()

        program = self.ctx.program(
            vertex_shader=vertex_shader, fragment_shader=fragment_shader
        )
        return program
