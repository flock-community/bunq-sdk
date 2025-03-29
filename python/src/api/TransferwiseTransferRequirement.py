from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class TransferwiseTransferRequirement:
  recipient_id: 'str'
  detail: 'Optional[List[TransferwiseRequirementField]]'

from .TransferwiseRequirementField import TransferwiseRequirementField