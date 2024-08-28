#version 330 core

in vec2 aPos;
in vec2 aTex;

out vec2 TexCoord;

void main() {
  TexCoord = aTex;
  gl_Position = vec4(aPos, 0.0, 1.0);
}