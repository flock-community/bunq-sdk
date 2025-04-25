from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

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

from ..model.Address import Address
from ..model.Ubo import Ubo
from ..model.CompanyVatNumber import CompanyVatNumber
from ..model.CompanyVatNumber import CompanyVatNumber