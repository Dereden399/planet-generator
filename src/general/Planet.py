from typing import List
from moderngl import Program

class Planet:
  def __init__(self, 
              planetSizeCoef: float,
              cloudSizeCoef: float,
              rotationSpeed: float,
              cloudRotationSpeed: float,
              planetColorConstraints: List[float],
              planetColors: List[float],
              cloudColorConstraints: List[float],
              cloudColors: List[float]
              ) -> None:
    if len(planetColorConstraints) < 3:
      raise ValueError("PlanetColorConstraints must have 3 components")
    for c in planetColorConstraints:
      if c < 0:
        raise ValueError("PlanetColorConstraints must have positive values")
    if len(planetColors) != 12:
      raise ValueError("PlanetColors has to be a matrix 4x3")
    if len(cloudColorConstraints) < 2:
      raise ValueError("CloudColorConstraints must have 2 components")
    for c in cloudColorConstraints:
      if c < 0:
        raise ValueError("CloudColorConstraints must have positive values")
    if len(cloudColors) != 6:
      raise ValueError("CloudColor has to be a matrix 2x3")
    
    self.planetSizeCoef = planetSizeCoef
    self.cloudSizeCoef = cloudSizeCoef
    self.rotationSpeed = rotationSpeed
    self.cloudRotationSpeed = cloudRotationSpeed
    self.planetColorConstraints = planetColorConstraints
    self.planetColors = planetColors
    self.cloudColorConstraints = cloudColorConstraints
    self.cloudColors = cloudColors
  
  def setUniforms(self, shader: Program):
    shader["planetSizeCoef"] = self.planetSizeCoef
    shader["cloudSizeCoef"] = self.cloudSizeCoef
    shader["rotationSpeed"] = self.rotationSpeed
    shader["cloudRotationSpeed"] = self.cloudRotationSpeed
    shader["planetColorConstraints"] = [self.planetColorConstraints[0], self.planetColorConstraints[1], self.planetColorConstraints[2]]
    shader["planetColors"] = self.planetColors
    shader["cloudColorConstraints"] = [self.cloudColorConstraints[0], self.cloudColorConstraints[1]]
    shader["cloudColors"] = self.cloudColors

