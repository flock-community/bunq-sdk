from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class UserCompany:
  name: 'Optional[str]'
  public_nick_name: 'Optional[str]'
  avatar_uuid: 'Optional[str]'
  address_main: 'Optional[Address]'
  address_postal: 'Optional[Address]'
  language: 'Optional[str]'
  region: 'Optional[str]'
  country: 'Optional[str]'
  ubo: 'Optional[List[Ubo]]'
  chamber_of_commerce_number: 'Optional[str]'
  legal_form: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  session_timeout: 'Optional[int]'
  daily_limit_without_confirmation_login: 'Optional[Amount]'
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  public_uuid: 'Optional[str]'
  display_name: 'Optional[str]'
  alias: 'Optional[List[Pointer]]'
  type_of_business_entity: 'Optional[str]'
  sector_of_industry: 'Optional[str]'
  counter_bank_iban: 'Optional[str]'
  avatar: 'Optional[Avatar]'
  version_terms_of_service: 'Optional[str]'
  directors: 'Optional[List[LabelUser]]'
  notification_filters: 'Optional[List[NotificationFilter]]'
  customer: 'Optional[Customer]'
  customer_limit: 'Optional[CustomerLimit]'
  billing_contract: 'Optional[List[BillingContractSubscription]]'
  deny_reason: 'Optional[str]'
  relations: 'Optional[List[RelationUser]]'
  tax_resident: 'Optional[List[TaxResident]]'

from .Address import Address
from .Ubo import Ubo
from .Amount import Amount
from .Pointer import Pointer
from .Avatar import Avatar
from .LabelUser import LabelUser
from .NotificationFilter import NotificationFilter
from .Customer import Customer
from .CustomerLimit import CustomerLimit
from .BillingContractSubscription import BillingContractSubscription
from .RelationUser import RelationUser
from .TaxResident import TaxResident