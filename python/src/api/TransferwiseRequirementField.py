from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .TransferwiseRequirementFieldGroup import TransferwiseRequirementFieldGroup

@dataclass
class TransferwiseRequirementField:
  key: str
  value: str
  name: Optional[str]
  group: Optional[TransferwiseRequirementFieldGroup]
