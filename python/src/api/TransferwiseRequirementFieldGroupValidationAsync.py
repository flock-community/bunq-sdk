from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .TransferwiseRequirementFieldGroupValidationAsyncParams import TransferwiseRequirementFieldGroupValidationAsyncParams

@dataclass
class TransferwiseRequirementFieldGroupValidationAsync:
  url: Optional[str]
  params: Optional[TransferwiseRequirementFieldGroupValidationAsyncParams]
