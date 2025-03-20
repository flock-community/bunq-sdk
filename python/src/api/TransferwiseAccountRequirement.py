from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .TransferwiseRequirementField import TransferwiseRequirementField

@dataclass
class TransferwiseAccountRequirement:
  country: Optional[str]
  name_account_holder: str
  type: str
  detail: Optional[List[TransferwiseRequirementField]]
