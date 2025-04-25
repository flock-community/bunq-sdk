from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class TransferwiseRequirementField:
  key: 'str'
  value: 'str'
  name: 'Optional[str]'
  group: 'Optional[TransferwiseRequirementFieldGroup]'

from ..model.TransferwiseRequirementFieldGroup import TransferwiseRequirementFieldGroup