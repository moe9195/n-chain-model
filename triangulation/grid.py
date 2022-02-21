import numpy as np
from math import sin, cos, ceil, pi

def num_to_dims(num: int) -> int:
  '''
  Takes the number of trianges we want
  and calculates the closest n and m values
  '''
  return ceil((num / 2) ** 0.5)

def calculate(num_triangles: int, radius: float) -> np.ndarray:
  '''
  Uniform grid in spherical coordinates triangulatioin method:
  A sphere is tesselatted in a lattitude and longitude grid, with n divisions around the equator and from pole to pole
  At each pole, N quadrilateral are formed. Each quadrilateral is split into two triangles from the diagonal.
  Takes the number of triangles and radius and returns an 3x3xN array
  where each 3x3 subarray represents a triangle on the sphere and each
  row represents the xyz coordinates of each vertex
  '''

  index = 0
  n = num_to_dims(num_triangles)
  theta = np.linspace(0, 2 * pi, n)
  phi = np.linspace(0, pi, n)
  vertices = np.zeros((3, 3, (n-1) * (n-1) * 2))

  for i in range(n - 1):
    for j in range(n - 1, 0, -1):
      x1u = cos(theta[i]) * sin(phi[j])
      y1u = sin(theta[i]) * sin(phi[j])
      z1u = cos(phi[j])
      
      x2u = cos(theta[i+1]) * sin(phi[j])
      y2u = sin(theta[i+1]) * sin(phi[j])
      z2u = cos(phi[j])
      
      x3u = cos(theta[i]) * sin(phi[j - 1])
      y3u = sin(theta[i]) * sin(phi[j - 1])
      z3u = cos(phi[j - 1])
      
      x1l = x2u
      y1l = y2u
      z1l = z2u
      
      x2l = x3u
      y2l = y3u
      z2l = z3u
      
      x3l = cos(theta[i + 1]) * sin(phi[j - 1])
      y3l = sin(theta[i + 1]) * sin(phi[j - 1])
      z3l = cos(phi[j - 1])
      
      vertices[:,:,2 * index] = np.array([[x1u, x2u, x3u], [y1u, y2u, y3u], [z1u, z2u, z3u]])
      vertices[:,:,2 * index + 1] = np.array([[x1l, x2l, x3l], [y1l, y2l, y3l], [z1l, z2l, z3l]])
      index += 1

  return vertices