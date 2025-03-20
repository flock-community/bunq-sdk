from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .TransferwiseRequirementField import TransferwiseRequirementField

@dataclass
class TransferwiseTransferRequirement:
  recipient_id: str
  detail: Optional[List[TransferwiseRequirementField]]
