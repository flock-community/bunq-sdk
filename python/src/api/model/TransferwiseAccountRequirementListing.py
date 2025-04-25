from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class TransferwiseAccountRequirementListing:
  type: 'Optional[str]'
  label: 'Optional[str]'
  fields: 'Optional[List[TransferwiseRequirementField]]'

from ..model.TransferwiseRequirementField import TransferwiseRequirementField