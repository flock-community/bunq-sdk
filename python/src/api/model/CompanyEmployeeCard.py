from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CompanyEmployeeCard:
  pointer_counter_user: 'Pointer'
  pointer_monetary_account: 'Pointer'
  type: 'str'
  product_type: 'str'
  company_name_on_card: 'Optional[str]'
  employee_name_on_card: 'Optional[str]'
  employee_preferred_name_on_card: 'Optional[str]'
  amount_limit_monthly: 'Optional[Amount]'
  status: 'Optional[str]'
  card: 'Optional[Card]'
  amount_spent_monthly: 'Optional[Amount]'
  number_of_company_employee_card_receipt_pending: 'Optional[int]'

from ..model.Pointer import Pointer
from ..model.Amount import Amount
from ..model.Card import Card