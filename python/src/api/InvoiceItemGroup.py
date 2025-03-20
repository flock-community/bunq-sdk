from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .InvoiceItem import InvoiceItem

@dataclass
class InvoiceItemGroup:
  type: Optional[str]
  type_description: Optional[str]
  type_description_translated: Optional[str]
  instance_description: Optional[str]
  product_vat_exclusive: Optional[Amount]
  product_vat_inclusive: Optional[Amount]
  item: Optional[List[InvoiceItem]]
