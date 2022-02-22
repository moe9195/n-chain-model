from pydantic import BaseModel
from sphere import Sphere
import matplotlib.pyplot as plt
import numpy as np
import time

class Plotter(BaseModel):
  plot_directory: str = './saved_plots/'
  sphere: Sphere = None

  def save_current_figure(self, xlabel, ylabel, name):
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.tight_layout()
    plt.savefig(self.plot_directory + name)
    plt.show()

  def plot_sphere(self, show_quadrant: bool = True) -> None:
    vertices = self.sphere.vertices
    v1, v2, v3 = vertices[:,0,:], vertices[:,1,:], vertices[:,2,:]

    ax = plt.axes(projection = '3d')
    ax.set_title(f'Sphere with {self.sphere.number_of_chains} triangles')

    if show_quadrant:
      v1[v1 < 0], v2[v2 < 0], v3[v3 < 0] = np.nan, np.nan, np.nan
      ax.set_zlim(0, self.sphere.radius)
      ax.view_init(elev = 25., azim = 30)

    for i in range(1, v1.shape[1]):
      triangle = np.vstack((v1[:,i], v2[:,i], v3[:,i], v1[:,i]))
      ax.plot(triangle[:,0], triangle[:,1], triangle[:,2], 'b-', linewidth = 0.5)

    self.save_current_figure('X', 'Y', f'sphere_{self.sphere.triangulation_method}_{self.sphere.number_of_chains}.png')

  def plot_stress_strain_curve(self) -> None:
    stress_strain_curve = self.sphere.stress_strain_curve

    for load in stress_strain_curve:
      stretch_ratio, total_force, total_unloading_force = load
      plt.ylim([0,np.max(total_force)+0.01])
      plt.margins(0,0)
      plt.plot(stretch_ratio, total_force, 'k', stretch_ratio, total_unloading_force, 'k')

    plt.title(f'Stress Strain Relation (N = {self.sphere.number_of_chains})')
    plt.grid()
    self.save_current_figure('Stretch ratio (%)', 'Tensile force (N)', f'stress_strain_{self.sphere.number_of_chains}_{time.time()}.png')

  def plot_chain_length_distribution(self) -> None:
    chain_length_distribution = self.sphere.chain_length_distribution

    plt.hist(chain_length_distribution, bins = 100)
    plt.title(f'Chain Length Distribution (N = {self.sphere.number_of_chains}, seed = {self.sphere.seed})')
    self.save_current_figure('Chain length', 'Chain count', f'chain_length_distribution_{self.sphere.number_of_chains}_{self.sphere.seed}.png')


