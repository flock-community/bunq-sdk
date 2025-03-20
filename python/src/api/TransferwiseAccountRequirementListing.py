from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .TransferwiseRequirementField import TransferwiseRequirementField

@dataclass
class TransferwiseAccountRequirementListing:
  type: Optional[str]
  label: Optional[str]
  fields: Optional[List[TransferwiseRequirementField]]
