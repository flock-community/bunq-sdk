from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class Geolocation:
  latitude: 'Optional[int]'
  longitude: 'Optional[int]'
  altitude: 'Optional[int]'
  radius: 'Optional[int]'

