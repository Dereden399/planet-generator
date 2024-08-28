import sys
import pygame
import moderngl
from array import array

from pygame.locals import QUIT, KEYDOWN
from general.Settings import Settings

SETTINGS = Settings()


pygame.init()
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG, True)
SCREEN = pygame.display.set_mode((SETTINGS.screenWidth, SETTINGS.screenHeight), flags=pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface((SETTINGS.screenWidth, SETTINGS.screenHeight))
pygame.display.set_caption("Test Game")
CLOCK = pygame.time.Clock()

ctx = moderngl.create_context()

VBO = ctx.buffer(data=array('f', [
  -1.0, 1.0, 0.0, 0.0,
   1.0, 1.0, 1.0, 0.0,
  -1.0, -1.0, 0.0, 1.0,
   1.0, -1.0, 1.0, 1.0
]))

with open("shaders/vShader.glsl", 'r') as file:
  vShader = file.read()

with open("shaders/fShader.glsl", 'r') as file:
  fShader = file.read()

shader = ctx.program(vertex_shader=vShader, fragment_shader=fShader)
VAO = ctx.vertex_array(shader, [(VBO, '2f 2f', 'aPos', 'aTex')])

shader['screenDimensions'] = [SETTINGS.screenWidth, SETTINGS.screenHeight]

time = 0
print("GAME LOOP STARTS")
while True:
  display.fill('Black')
  delta = CLOCK.tick(SETTINGS.fpsCap) / 1000
  time += delta
  for event in pygame.event.get():
    if event.type == QUIT or event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
      print("GAME LOOP ENDS")
      pygame.quit()
      sys.exit()
  
  shader['time'] = time

  VAO.render(mode=moderngl.TRIANGLE_STRIP)

  pygame.display.flip()
  print(CLOCK.get_fps())