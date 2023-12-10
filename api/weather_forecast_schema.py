# Profeanu Ioana, 343C1 - schemas for the server responses
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


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


@dataclass
class Temperature:
    id: int
    valoare: float
    timestamp: datetime


@dataclass
class TemperatureFilters:
    lat: Optional[float] = None
    lon: Optional[float] = None
    from_date: Optional[datetime] = None
    until_date: Optional[datetime] = None
