import numpy as np
import triangulation
from pydantic import BaseModel, validator
from typing import Any, List
from physics import stress_strain
from math import log, sqrt

class Sphere(BaseModel):
    radius: float = 1
    triangulation_method: str = "octahedron"
    vertices: np.ndarray = None
    number_of_chains: int = 1024
    stress_strain_curve: np.ndarray = None
    num_of_links: int = 10
    shear_modulus: float = 0.135
    step_size: float = 0.01
    chain_length_std: float = 5
    tolerance: float = 0.9
    strech_vector: np.ndarray = None
    stress_strain_curve: List = []
    chain_length_distribution: np.ndarray = None
    seed: int = 1

    def __init__(self, **data) -> None:
        super().__init__(**data)
        self.vertices = self.__calculate_vertices()
        self.number_of_chains = self.vertices.shape[-1]
        self.chain_length_distribution = self.__calculate_chain_length_distribution()

    def __calculate_vertices(self) -> np.ndarray:
        return getattr(triangulation, self.triangulation_method).calculate(self.number_of_chains, self.radius)
    
    def __calculate_chain_length_distribution(self) -> np.ndarray:
        mu  = log(self.num_of_links / sqrt(1 + ((self.chain_length_std ** 2) / (self.num_of_links ** 2))))
        sig = sqrt(log(1 + ((self.chain_length_std ** 2) / (self.num_of_links ** 2))))
        return np.random.lognormal(mean = mu, sigma = sig, size = self.vertices.shape[2])

    def deform(self, type: str, stretch_ratio: float) -> None:
        stretch_vector, total_force, total_unloading_force = stress_strain.stress_strain_relation(self.chain_length_distribution, self.shear_modulus, self.step_size, self.tolerance, stretch_ratio, type, self.vertices)
        self.stress_strain_curve.append([stretch_vector, total_force, total_unloading_force])

    @validator('triangulation_method')
    def triangulation_method_must_be(cls, v) -> Any:
        if v not in ['grid', 'octahedron']:
            raise ValueError(f'Triangulation method must be either "grid" or "octahedron"')
        return v
    
    @validator('tolerance')
    def tolerance_must_be(cls, v) -> Any:
        if v <= 0 or v >= 1:
            raise ValueError(f'Tolerance must be between 0 and 1')
        return v
    
    class Config:
        arbitrary_types_allowed = True
