from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class Address:
  street: 'Optional[str]'
  house_number: 'Optional[str]'
  po_box: 'Optional[str]'
  postal_code: 'Optional[str]'
  city: 'Optional[str]'
  country: 'Optional[str]'
  extra: 'Optional[str]'
  mailbox_name: 'Optional[str]'
  province: 'Optional[str]'
  is_user_address_updated: 'Optional[bool]'

