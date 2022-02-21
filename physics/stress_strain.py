from helper_functions import *
from physics.deformation import deform
from math import log, sqrt, pi
np.seterr(divide='ignore', invalid='ignore')

def force(chain_lengths, solid_angles, max_chain_lengths, shear_modulus, h):
  """
  Calculate the force on the chains by calculating the stress on each chain and summing them.
  One point differentiation is used on the entropy to calculate the force.
  """
  beta = inverse_langevin(chain_lengths / np.sqrt(max_chain_lengths))
  entropy = (chain_lengths > 0) * solid_angles * (shear_modulus * np.sqrt(max_chain_lengths) * ((chain_lengths * beta)  + np.log(beta / np.sinh(beta)))) + (chain_lengths <= 0) * 0
  force = np.diff(entropy, axis=0) / h
  force[np.isnan(force)] = 0
  total_force = (1 / (4 * pi)) * np.sum(force, 1)
  return total_force

def stress_strain_relation(num_of_links, shear_modulus,  step_size, std, tolerance, stretch_ratio, deformation_type, vertices):
  np.random.seed(1)
  stretch_ratios = np.arange(1, stretch_ratio + step_size, step_size)  

  solid_angles = calculate_solid_angles(vertices)
  centroid_points = spherical_triangle_centroids(vertices)
  rd = deform(stretch_ratios, deformation_type)

  rx, ry, rz = np.outer(rd[0,:], centroid_points[0,:],), np.outer(rd[1,:], centroid_points[1,:],), np.outer(rd[2,:], centroid_points[2,:],)
  chain_lengths  = np.sqrt((rx**2) + (ry**2) + (rz**2))
  deformation_vector_length, chain_vector_length = chain_lengths.shape[0], chain_lengths.shape[1]

  """
  we a assume chain length distribution that follows a log-normal distribution
  where the average number of links in each chain is given by num_of_links
  """

  mu  = log(num_of_links / sqrt(1 + ((std ** 2)/(num_of_links ** 2))))
  sig = sqrt(log(1 + ((std ** 2) / (num_of_links ** 2))))
  max_chain_lengths  = np.random.lognormal(mean=mu, sigma=sig, size=chain_vector_length)

  """
  we 'break' chains that exceed their maximum allowed length (set by the tolerance) by setting
  their length to 0. Then we calculate the forces on the chains to obtain the loading curve.
  """

  chain_lengths[chain_lengths > np.sqrt(max_chain_lengths) * tolerance] = 0 
  total_force = force(chain_lengths, solid_angles, max_chain_lengths, shear_modulus, step_size)

  """
  For the unloading curve, we remove the contribution of all the broken chains and recalculate
  the forces on the unbroken chains
  """

  a0   = chain_lengths[deformation_vector_length - 1,:]
  unbroken_chain_lengths = chain_lengths[:,~(a0 == 0)]
  #xb, yb, zb = x[(a0==0)], y[(a0==0)], z[(a0==0)]
  unbroken_solid_angles = solid_angles[0,~(a0==0)]
  unbroken_max_chain_lengths = max_chain_lengths[~(a0==0)]
  total_unloading_force = force(unbroken_chain_lengths, unbroken_solid_angles, unbroken_max_chain_lengths, shear_modulus, step_size)
  stretch_vector = 100 * np.delete(stretch_ratios, -1)
  return stretch_vector, total_force, total_unloading_force       