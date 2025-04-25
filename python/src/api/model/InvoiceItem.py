from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class InvoiceItem:
  id: 'Optional[int]'
  billing_date: 'Optional[str]'
  type_description: 'Optional[str]'
  type_description_translated: 'Optional[str]'
  unit_vat_exclusive: 'Optional[Amount]'
  unit_vat_inclusive: 'Optional[Amount]'
  vat: 'Optional[int]'
  quantity: 'Optional[int]'
  total_vat_exclusive: 'Optional[Amount]'
  total_vat_inclusive: 'Optional[Amount]'

from ..model.Amount import Amount