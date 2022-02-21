from dataclasses import dataclass

# Create class sphere with dataclass
@dataclass
class Sphere:
    radius: float = 1
    triangulation_method: str = "icosahedron"


sphere = Sphere()

print(sphere)