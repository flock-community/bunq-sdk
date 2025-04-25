from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CurrencyCloudBeneficiaryRequirementListing:
  payment_type: 'Optional[str]'
  legal_entity_type: 'Optional[str]'
  all_field: 'Optional[List[CurrencyCloudBeneficiaryRequirementField]]'

from ..model.CurrencyCloudBeneficiaryRequirementField import CurrencyCloudBeneficiaryRequirementField