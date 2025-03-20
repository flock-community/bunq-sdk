from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Avatar import Avatar

@dataclass
class OpenBankingProviderBank:
  account_information_service_status: Optional[str]
  payment_information_service_status: Optional[str]
  name: Optional[str]
  aiia_provider_id: Optional[str]
  country: Optional[str]
  all_payment_method_allowed_sepa: Optional[List[str]]
  all_payment_method_allowed_domestic: Optional[List[str]]
  audience_business_status: Optional[bool]
  audience_private_status: Optional[bool]
  avatar: Optional[Avatar]
