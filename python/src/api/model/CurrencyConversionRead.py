from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CurrencyConversionRead:
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

from ..model.Amount import Amount
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.Payment import Payment