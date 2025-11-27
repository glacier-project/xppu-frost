from dataclasses import dataclass
from enum import Enum
from shape import Shape, CircleShape
from shapely import Point

@dataclass(frozen=True)
class Position:
    x: float = 0
    y: float = 0
    z: float = 0

class MaterialType(str, Enum):
    UNDEFINED = "undefined"
    STEEL = "steel"
    PLASTIC = "plastic"

class Material:

    def __init__(
            self, 
            id: int = -1,
            m_type: MaterialType = MaterialType.UNDEFINED,
            weight: float = 0,
            shape: Shape = None,
            cap: str = '',
            stamped: bool = False
            ):
        self.id = id
        self.m_type = m_type
        self.weight = weight
        if shape is None:
            shape = CircleShape(Point(0,0,0), radius=0.025)
        self.shape = shape
        self.cap = cap
        self.stamped = stamped

    def __eq__(self, other) -> bool:
        if not isinstance(other, Material):
            return False
        return (self.id == other.id and
                self.m_type == other.m_type and
                self.weight == other.weight and
                self.cap == other.cap and
                self.stamped == other.stamped and
                self.shape == other.shape)
    
    def __hash__(self) -> int:
        return hash((self.id, self.m_type, self.weight, self.cap, self.stamped, self.shape))

    def __str__(self) -> str:
        return f'Material(id={self.id}, m_type={self.m_type}, weight={self.weight}, cap={self.cap}, stamped={self.stamped}, shape={self.shape})'

    def __repr__(self) -> str:
        return f'Material(id={self.id}, m_type={self.m_type}, weight={self.weight}, cap={self.cap}, stamped={self.stamped}, shape={self.shape})'


class SteelMaterial(Material):

    def __init__(
            self,
            id: int = -1,
            weight: float = 0,
            shape: Shape = None
            ):
        super().__init__(id=id,m_type=MaterialType.STEEL,weight=weight,shape=shape)
        
class PlasticMaterial(Material):

    def __init__(
            self,
            id: int = -1,
            weight: float = 0,
            shape: Shape = None
            ):
        super().__init__(id=id,m_type=MaterialType.PLASTIC,weight=weight,shape=shape)