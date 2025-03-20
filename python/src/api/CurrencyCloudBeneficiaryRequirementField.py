from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class CurrencyCloudBeneficiaryRequirementField:
  label: Optional[str]
  name: Optional[str]
  validation_expression: Optional[str]
  input_type: Optional[str]
