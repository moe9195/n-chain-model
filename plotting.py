from pydantic import BaseModel
import matplotlib.pyplot as plt
import numpy as np

class Plotter(BaseModel):
  plot_directory: str = './'

  def plot_sphere(self, sphere, show_quadrant = True):
    vertices = sphere.vertices
    v1, v2, v3 = vertices[:,0,:], vertices[:,1,:], vertices[:,2,:]

    ax = plt.axes(projection = '3d')
    ax.set_title(f'Sphere with {sphere.number_of_triangles} triangles')

    if show_quadrant:
      v1[v1 < 0], v2[v2 < 0], v3[v3 < 0] = np.nan, np.nan, np.nan
      ax.set_zlim(0, sphere.radius)
      ax.view_init(elev = 25., azim = 30)

    for i in range(1, v1.shape[1]):
      triangle = np.vstack((v1[:,i], v2[:,i], v3[:,i], v1[:,i]))
      ax.plot(triangle[:,0], triangle[:,1], triangle[:,2], 'b-', linewidth = 0.5)

    plt.show()