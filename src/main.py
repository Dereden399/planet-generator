import sys
import pygame
import moderngl
from array import array
import random;

from pygame.locals import QUIT, KEYDOWN
from general.Planet import Planet
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

FNT = pygame.font.SysFont('Arial', 36)

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
shader['noiseSeed'] = random.uniform(-2**15, 2**15);

def surfToTexture(surf: pygame.Surface):
  tex = ctx.texture(surf.get_size(), 4)
  tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
  tex.swizzle = "BGRA"
  tex.write(surf.get_view('1'))
  return tex

planet = Planet(0.25, 1.1, -0.2, 1.5,
                [0.55, 0.54, 0.48],
                [0.486, 0.988, 0.0,
                 0.761, 0.698, 0.502,
                 0.118, 0.565, 1.0,
                 0.004, 0.227, 0.420],
                 [0.7, 0.6],
                 [1, 1, 1,
                  1, 1, 1])
planet.setUniforms(shader)

time = 0
print("GAME LOOP STARTS")
while True:
  display.fill('Black')
  delta = CLOCK.tick(SETTINGS.fpsCap) / 1000
  time += delta

  textSurface = FNT.render(f"fps: {int(CLOCK.get_fps())}", True, 'White')
  display.blit(textSurface, (5, 5))

  for event in pygame.event.get():
    if event.type == QUIT or event.type == KEYDOWN and event.key == pygame.K_ESCAPE:
      print("GAME LOOP ENDS")
      pygame.quit()
      sys.exit()
    if event.type == KEYDOWN and event.key == pygame.K_SPACE:
      shader['noiseSeed'] = random.uniform(-2**15, 2**15);
  
  tex = surfToTexture(display)
  tex.use(0)


  shader['backgroundTexture'] = 0
  shader['time'] = time

  VAO.render(mode=moderngl.TRIANGLE_STRIP)

  pygame.display.flip()

  tex.release()