import sys
import pygame
import moderngl
from array import array
import random;
import colorsys
from typing import List

from pygame.locals import QUIT, KEYDOWN, MOUSEWHEEL, FINGERMOTION
from general.Planet import Planet
from general.Settings import Settings

SETTINGS = Settings()
'''
0 - no water
1 - small amount of water, big lands
2 - normal amount of water, normal lands
3 - big amount of water, small lands
4 - only water
'''
PLANET_CONSTRAINTS = [
  [0.6, 0, 0],
  [0.6, 0.3, 0.1],
  [0.55, 0.54, 0.48],
  [0.8, 0.78, 0.6],
  [1.1, 1.1, 0.5]
]

CLOUD_CONSTRAINTS = [
  [0.8, 0.7],
  [0.8, 0.6],
  [0.7, 0.5],
  [0.7, 0.3]
]


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

def randomInterestingColor():
  while True:
    r, g, b = randomColor()
    # Avoid colors that are too close to black, white, or gray
    if (r, g, b) != (1, 1, 1) and (r, g, b) != (0, 0, 0) and abs(r - g) > 0.1 and abs(r - b) > 0.1 and abs(g - b) > 0.1:
      return [r, g, b]
def randomColor():
  return [random.uniform(0.1, 1), random.uniform(0.1, 1), random.uniform(0.1, 1)]

def getAnalogColor(color: List[int], deg=30/360):
  h, l, s = colorsys.rgb_to_hls(color[0], color[1], color[2])
  newH = (h+deg)%1
  newR, newG, newB = colorsys.hls_to_rgb(newH, l, s)
  return [newR, newG, newB]

def getComplementColor(color: List[int]):
  return [1-color[0], 1-color[1], 1-color[2]]

def generatePlanet() -> Planet:
  planetSize = round(random.uniform(0.1, 0.4), 2)
  cloudRadius = round(random.uniform(0, 3), 2)
  planetRotationSpeed = round(random.uniform(-1, 1), 2)
  if planetRotationSpeed == 0:
    planetRotationSpeed = 0.01
  cloudRotationSpeed = round(random.uniform(0.1, 2), 1)

  planetConstraintsIdx = random.choice(range(len(PLANET_CONSTRAINTS)))
  planetConstraints = PLANET_CONSTRAINTS[planetConstraintsIdx]

  col1 = randomColor()
  col2 = getAnalogColor(col1)
  col3 = getComplementColor(col1) if planetConstraintsIdx != 0 and planetConstraintsIdx != len(PLANET_CONSTRAINTS) else getAnalogColor(col2)
  col4 = getAnalogColor(col3)
  planetColors = col1 + col2 + col3 + col4

  cloudConstraints = random.choice(CLOUD_CONSTRAINTS)

  clCol1 = randomColor()
  clCol2 = getAnalogColor(clCol1, 10/360)

  cloudColors = clCol1 + clCol2

  return Planet(planetSize, cloudRadius, planetRotationSpeed, cloudRotationSpeed,
                planetConstraints,
                planetColors,
                cloudConstraints,
                cloudColors)

planet = generatePlanet()
planet.setUniforms(shader)

uiScale = 1.0

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
      shader['noiseSeed'] = random.uniform(-2**15, 2**15)
      planet = generatePlanet()
      planet.setUniforms(shader)
    if event.type == MOUSEWHEEL:
      val = event.y/100
      uiScale += val
      uiScale = min(uiScale, 3)
      uiScale = max(uiScale, 0.1)
    if event.type == FINGERMOTION:
      print(event.x)
    if event.type == KEYDOWN and event.key == pygame.K_p:
      uiScale = min(uiScale+0.1, 3)
    if event.type == KEYDOWN and event.key == pygame.K_o:
      uiScale = max(uiScale-0.1, 0.1)
    if event.type == KEYDOWN and event.key == pygame.K_0:
      uiScale = 1
  
  tex = surfToTexture(display)
  tex.use(0)


  shader['backgroundTexture'] = 0
  shader['time'] = time
  shader['uiScale'] = uiScale

  VAO.render(mode=moderngl.TRIANGLE_STRIP)

  pygame.display.flip()

  tex.release()