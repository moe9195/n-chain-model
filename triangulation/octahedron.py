import numpy as np
from math import ceil
from helper_functions import arsunit

def num_to_iterations(num: int) -> int:
  '''
  Takes the number of trianges we want
  and calculates the closest n and m values
  '''
  return ceil((np.log(num) - 3 * np.log(2)) / (2 * np.log(2)))

def calculate(num_triangles: int, radius: float) -> np.ndarray:
	'''
	Using octahedron (geodesic sphere) triangulation method:
	For every iteration divide every triangle into three new triangles
								^ C
								/ \
					AC/2 /_4_\CB/2
							/\ 3 /\
						 / 1\ /2 \
					A /____V____\B           
								AB/2	
	Takes a number of iterations and radius and returns an 3x3xN array
	where each 3x3 subarray represents a triangle on the sphere and each
	row represents the xyz coordinates of each vertex
	'''

	iterations = num_to_iterations(num_triangles)

	# Initialize octahedron vertices
	A = np.array([1,0,0])
	B = np.array([0,1,0])
	C = np.array([0,0,1])

	# Create initial triangles which define the octahedron
	triangles = np.vstack((A, B, C, A, B, -C, -A, B, C, -A, B, -C, -A, -B, C, -A, -B, -C, A, -B, C, A, -B, -C)) 

	# Split the triangles into ABC points
	selector  = np.arange(1, triangles.shape[0]-1, 3)
	Ap = triangles[selector-1]
	Bp = triangles[selector]
	Cp = triangles[selector+1]
	

	for _ in range(1, iterations + 1):
			AB_2 = arsunit((Ap + Bp) / 2, radius)
			AC_2 = arsunit((Ap + Cp) / 2, radius)
			CB_2 = arsunit((Cp + Bp) / 2, radius)
			Ap = np.vstack((Ap, AB_2, AC_2, AC_2))
			Bp = np.vstack((AB_2, Bp, AB_2, CB_2))
			Cp = np.vstack((AC_2, CB_2, CB_2, Cp))
	
	return np.transpose(np.array([Ap, Bp, Cp]), (2, 0, 1))
