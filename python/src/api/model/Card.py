from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class Card:
  pin_code: 'Optional[str]'
  activation_code: 'Optional[str]'
  status: 'Optional[str]'
  order_status: 'Optional[str]'
  card_limit: 'Optional[Amount]'
  card_limit_atm: 'Optional[Amount]'
  country_permission: 'Optional[List[CardCountryPermission]]'
  pin_code_assignment: 'Optional[List[CardPinAssignment]]'
  primary_account_numbers: 'Optional[List[CardPrimaryAccountNumber]]'
  monetary_account_id_fallback: 'Optional[int]'
  preferred_name_on_card: 'Optional[str]'
  second_line: 'Optional[str]'
  cancellation_reason: 'Optional[str]'

from ..model.Amount import Amount
from ..model.CardCountryPermission import CardCountryPermission
from ..model.CardPinAssignment import CardPinAssignment
from ..model.CardPrimaryAccountNumber import CardPrimaryAccountNumber