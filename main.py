from sphere import Sphere
from plotting import Plotter

sphere = Sphere(number_of_triangles = 1000, radius = 1, triangulation_method = 'octahedron')

plotter = Plotter()
plotter.plot_sphere(sphere, show_quadrant = True)

