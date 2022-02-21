from pydantic import BaseModel, Field, validator
import numpy as np
import triangulation

class Sphere(BaseModel):
    radius: float = 1
    triangulation_method: str = "octahedron"
    number_of_triangles: int
    vertices: np.ndarray = None

    def __init__(self, **data):
        super().__init__(**data)
        self.vertices = self.__calculate_vertices()
        self.number_of_triangles = self.vertices.shape[-1]

    def __calculate_vertices(self):
        return getattr(triangulation, self.triangulation_method).calculate(self.number_of_triangles, self.radius)

    @validator('triangulation_method')
    def triangulation_method_must_be(cls, v):
        if v not in ['grid', 'octahedron']:
            raise ValueError(f'Triangulation method must be either "grid" or "octahedron"')
        return v
    
    class Config:
        arbitrary_types_allowed = True
