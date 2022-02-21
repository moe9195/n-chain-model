from sphere import Sphere
from plotting import Plotter

experiment = [
  ['uniaxial', 2],
  ['uniaxial', 2.5],
  ['uniaxial', 3]
]

def main():
  sphere = Sphere(radius = 1,
                  number_of_chains = 5000,
                  triangulation_method = 'grid')

  for deformation_type, stretch_ratio in experiment:
    sphere.deform(deformation_type, stretch_ratio)

  plotter = Plotter(sphere = sphere)
  plotter.plot_stress_strain_curve()

if __name__ == '__main__':
  main()