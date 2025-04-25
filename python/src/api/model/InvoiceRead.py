from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class InvoiceRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  invoice_date: 'Optional[str]'
  invoice_number: 'Optional[str]'
  status: 'Optional[str]'
  category: 'Optional[str]'
  group: 'Optional[List[InvoiceItemGroup]]'
  total_vat_inclusive: 'Optional[Amount]'
  total_vat_exclusive: 'Optional[Amount]'
  total_vat: 'Optional[Amount]'
  alias: 'Optional[LabelMonetaryAccount]'
  address: 'Optional[Address]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  counterparty_address: 'Optional[Address]'
  chamber_of_commerce_number: 'Optional[str]'
  vat_number: 'Optional[str]'
  request_reference_split_the_bill: 'Optional[List[RequestInquiryReference]]'

from ..model.InvoiceItemGroup import InvoiceItemGroup
from ..model.Amount import Amount
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.Address import Address
from ..model.RequestInquiryReference import RequestInquiryReference