from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class TransferwiseRequirementFieldGroupValidationAsyncParams:
  key: Optional[str]
  parameter_name: Optional[str]
  required: Optional[bool]
