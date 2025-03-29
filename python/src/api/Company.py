from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class Company:
  name: 'str'
  address_main: 'Address'
  address_postal: 'Address'
  country: 'str'
  ubo: 'Optional[List[Ubo]]'
  chamber_of_commerce_number: 'Optional[str]'
  legal_form: 'str'
  subscription_type: 'str'
  avatar_uuid: 'Optional[str]'
  vat_number: 'Optional[CompanyVatNumber]'
  vat_numbers: 'Optional[List[CompanyVatNumber]]'
  signup_track_type: 'Optional[str]'

from .Address import Address
from .Ubo import Ubo
from .CompanyVatNumber import CompanyVatNumber
from .CompanyVatNumber import CompanyVatNumber