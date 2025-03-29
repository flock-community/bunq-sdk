from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class TransferwiseRequirementFieldGroupValidationAsync:
  url: 'Optional[str]'
  params: 'Optional[TransferwiseRequirementFieldGroupValidationAsyncParams]'

from .TransferwiseRequirementFieldGroupValidationAsyncParams import TransferwiseRequirementFieldGroupValidationAsyncParams