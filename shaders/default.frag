#version 330 core

layout(location = 0) out vec4 fragColor;

void main() {
    vec3 color = vec3(0.24, 0.37, 0.52);
    fragColor = vec4(color, 1.0);
}