from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class TransferwiseRequirementFieldGroupValidationAsync:
  url: 'Optional[str]'
  params: 'Optional[TransferwiseRequirementFieldGroupValidationAsyncParams]'

from ..model.TransferwiseRequirementFieldGroupValidationAsyncParams import TransferwiseRequirementFieldGroupValidationAsyncParams