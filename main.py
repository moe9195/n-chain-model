from sphere import Sphere
from plotting import Plotter

def main():

  experiment = [
    ['uniaxial', 1.50],
    ['uniaxial', 2.00],
    ['uniaxial', 2.50],
    ['uniaxial', 3.00],
  ]

  sphere = Sphere(radius = 1, number_of_chains = 10000, triangulation_method = 'octahedron')

  for deformation_type, stretch_ratio in experiment:
    sphere.deform(deformation_type, stretch_ratio)

  plotter = Plotter(sphere = sphere)

  plotter.plot_sphere(show_quadrant = True)
  plotter.plot_stress_strain_curve()
  plotter.plot_chain_length_distribution()

if __name__ == '__main__':
  main()