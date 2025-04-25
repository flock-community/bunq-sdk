from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CardListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  public_uuid: 'Optional[str]'
  user_id: 'Optional[int]'
  user_owner_id: 'Optional[int]'
  user_holder_id: 'Optional[int]'
  type: 'Optional[str]'
  sub_type: 'Optional[str]'
  product_type: 'Optional[str]'
  product_sub_type: 'Optional[str]'
  first_line: 'Optional[str]'
  second_line: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  order_status: 'Optional[str]'
  expiry_date: 'Optional[str]'
  name_on_card: 'Optional[str]'
  preferred_name_on_card: 'Optional[str]'
  primary_account_numbers: 'Optional[List[CardPrimaryAccountNumber]]'
  payment_account_reference: 'Optional[str]'
  card_limit: 'Optional[Amount]'
  card_limit_atm: 'Optional[Amount]'
  country_permission: 'Optional[List[CardCountryPermission]]'
  label_monetary_account_ordered: 'Optional[LabelMonetaryAccount]'
  label_monetary_account_current: 'Optional[LabelMonetaryAccount]'
  monetary_account: 'Optional[MonetaryAccount]'
  pin_code_assignment: 'Optional[List[CardPinAssignment]]'
  monetary_account_id_fallback: 'Optional[int]'
  country: 'Optional[str]'
  card_shipment_tracking_url: 'Optional[str]'
  is_card_eligible_for_free_replacement: 'Optional[bool]'
  card_replacement: 'Optional[CardReplacement]'
  card_generated_cvc2: 'Optional[CardGeneratedCvc2]'
  is_limited_edition: 'Optional[bool]'
  card_metal_member_since_date: 'Optional[str]'
  company_employee_card: 'Optional[CompanyEmployeeCard]'

from ..model.CardPrimaryAccountNumber import CardPrimaryAccountNumber
from ..model.Amount import Amount
from ..model.CardCountryPermission import CardCountryPermission
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.MonetaryAccount import MonetaryAccount
from ..model.CardPinAssignment import CardPinAssignment
from ..model.CardReplacement import CardReplacement
from ..model.CardGeneratedCvc2 import CardGeneratedCvc2
from ..model.CompanyEmployeeCard import CompanyEmployeeCard