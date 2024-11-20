#version 330 core

uniform sampler2D tex;

in vec2 v_texcoord;
out vec4 f_color;

void main() {
    f_color = texture(tex, v_texcoord);
}