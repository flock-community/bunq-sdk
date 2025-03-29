from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class TransferwiseRequirementFieldGroupValidationAsyncParams:
  key: 'Optional[str]'
  parameter_name: 'Optional[str]'
  required: 'Optional[bool]'

