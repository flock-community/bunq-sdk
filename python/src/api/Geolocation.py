from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class Geolocation:
  latitude: Optional[int]
  longitude: Optional[int]
  altitude: Optional[int]
  radius: Optional[int]
