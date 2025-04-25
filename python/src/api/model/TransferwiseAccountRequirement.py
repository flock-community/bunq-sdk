from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class TransferwiseAccountRequirement:
  country: 'Optional[str]'
  name_account_holder: 'str'
  type: 'str'
  detail: 'Optional[List[TransferwiseRequirementField]]'

from ..model.TransferwiseRequirementField import TransferwiseRequirementField