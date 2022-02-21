import numpy as np

def deform(stretch_ratios: np.ndarray, type: str) -> np.ndarray:
  if type == 'equibiaxial':
    return equibiaxial(stretch_ratios)
  elif type == 'uniaxial':
    return uniaxial(stretch_ratios)
  elif type == 'shear':
    return shear(stretch_ratios)
  else:
    raise ValueError(f'Deformation type must be either "equibiaxial", "uniaxial" or "shear"')


def uniaxial(stretch_ratios: np.ndarray) -> np.ndarray:
  """
  Takes array of stretch ratios and outputs the three principle stretch ratio in the xyz directions
  for uniaxial deformation, assuming constant volume criterion
  """
  x_stretch = stretch_ratios
  y_stretch = np.reciprocal(np.sqrt(x_stretch))
  z_stretch = y_stretch

  return np.vstack((z_stretch, y_stretch, x_stretch))

def equibiaxial(stretch_ratios: np.ndarray) -> np.ndarray:
  """
  Takes array of stretch ratios and outputs the three principle stretch ratio in the xyz directions
  for equibiaxial deformation, assuming constant volume criterion
  """
  x_stretch = stretch_ratios
  y_stretch = stretch_ratios
  z_stretch = np.reciprocal(stretch_ratios ** 2)

  return np.vstack((z_stretch, y_stretch, x_stretch))

def shear(stretch_ratios: np.ndarray) -> np.ndarray:
  """
  Takes array of stretch ratios and outputs the three principle stretch ratio in the xyz directions
  for pure shear, assuming constant volume criterion
  """
  x_stretch = stretch_ratios
  y_stretch = np.ones((1, stretch_ratios.size))
  z_stretch = np.reciprocal(stretch_ratios)

  return np.vstack((z_stretch, y_stretch, x_stretch))
