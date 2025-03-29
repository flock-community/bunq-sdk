from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CurrencyConversion:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  status: 'Optional[str]'
  date_delivery_expected: 'Optional[str]'
  rate: 'Optional[str]'
  amount: 'Optional[Amount]'
  counter_amount: 'Optional[Amount]'
  group_uuid: 'Optional[str]'
  type: 'Optional[str]'
  order_type: 'Optional[str]'
  label_monetary_account: 'Optional[LabelMonetaryAccount]'
  counter_label_monetary_account: 'Optional[LabelMonetaryAccount]'
  payment: 'Optional[Payment]'

from .Amount import Amount
from .LabelMonetaryAccount import LabelMonetaryAccount
from .Payment import Payment