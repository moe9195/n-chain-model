import numpy as np
from math import atan

def arsnorm(A: np.ndarray) -> np.ndarray:
	'''
	Takes a numpy array of vertices and returns the norm
	'''
    
	return np.sum(np.abs(A) ** 2, axis = 0) ** (0.5)

def arsunit(A: np.ndarray, radius: float) -> np.ndarray:
	'''
	Takes a numpy array of vertices and projects them onto a sphere
	'''

	normOfA = arsnorm(A.transpose())
	return radius * np.divide(A, np.transpose(np.vstack((normOfA, normOfA, normOfA))))

def det3(matrix: np.ndarray) -> float:
    """
    Calculate the determinant of a 3x3 matrix. This is faster than using numpy.linalg.det for 3x3 matrices.
    """

    return (matrix[0, 0] * (matrix[1, 1] * matrix[2, 2] - matrix[2, 1] * matrix[1, 2]) -
            matrix[0, 1] * (matrix[1, 0] * matrix[2, 2] - matrix[2, 0] * matrix[1, 2]) +
            matrix[0, 2] * (matrix[1, 0] * matrix[2, 1] - matrix[2, 0] * matrix[1, 1]))


def solid_angles(vertices: np.ndarray) -> float:
    """
    Calculate the solid angles each triangle in the verticles array using Van Oosterom formula
    """

    dims = np.shape(vertices)
    solid_angles = np.zeros([1, dims[2]])

    # For each triangle we calculate the individual solid angles and add them to the solid angle array
    for i in range(dims[2]):
        X = vertices[:,:,i]
        R1, R2, R3 = X[:,0], X[:,1], X[:,2]
        N = arsnorm(X)
        n1, n2, n3 = N[0], N[1], N[2]
        D = abs(det3(X))
        A = D/((n1 * n2 * n3) + ((np.dot(R1, R2) * n3) + (np.dot(R1, R3) * n2) + (np.dot(R2, R3) * n1)))
        solid_angles[0, i] = atan(A)*2      

    return solid_angles

def spherical_triangle_centroid(vertices: np.ndarray) -> np.ndarray:
    """
    Calculate the coordinates of the centroid of a each spherical triangle in the vertices array
    """

    dims = vertices.shape
    centroids = np.zeros([3, dims[2]])

    for i in range(dims[2]):

        # Getting the vertex vectors of the triangles
        X = vertices[:,:,i]
        R1 = X[:,0]
        R2 = X[:,1]
        R3 = X[:,2]

        # Calculating xyz position of centres and projecting onto the sphere
        temp = (R1 + R2 + R3)/3
        temp = temp/np.linalg.norm(temp)
        centroids[:,i] = temp

    return centroids