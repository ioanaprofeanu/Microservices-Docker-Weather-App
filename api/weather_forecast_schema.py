from dataclasses import dataclass

@dataclass
class Country:
    id: int
    nume: str
    lat: float
    lon: float

@dataclass
class City:
    id: int
    idTara: int
    nume: str
    lat: float
    lon: float