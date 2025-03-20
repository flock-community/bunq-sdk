from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .CurrencyCloudBeneficiaryRequirementField import CurrencyCloudBeneficiaryRequirementField

@dataclass
class CurrencyCloudBeneficiaryRequirementListing:
  payment_type: Optional[str]
  legal_entity_type: Optional[str]
  all_field: Optional[List[CurrencyCloudBeneficiaryRequirementField]]
