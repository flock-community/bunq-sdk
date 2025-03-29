from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class UserPersonRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  public_uuid: 'Optional[str]'
  first_name: 'Optional[str]'
  middle_name: 'Optional[str]'
  last_name: 'Optional[str]'
  legal_name: 'Optional[str]'
  display_name: 'Optional[str]'
  public_nick_name: 'Optional[str]'
  alias: 'Optional[List[Pointer]]'
  tax_resident: 'Optional[List[TaxResident]]'
  address_main: 'Optional[Address]'
  address_postal: 'Optional[Address]'
  date_of_birth: 'Optional[str]'
  place_of_birth: 'Optional[str]'
  country_of_birth: 'Optional[str]'
  nationality: 'Optional[str]'
  all_nationality: 'Optional[List[str]]'
  language: 'Optional[str]'
  region: 'Optional[str]'
  gender: 'Optional[str]'
  avatar: 'Optional[Avatar]'
  version_terms_of_service: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  session_timeout: 'Optional[int]'
  daily_limit_without_confirmation_login: 'Optional[Amount]'
  notification_filters: 'Optional[List[NotificationFilter]]'
  relations: 'Optional[List[RelationUser]]'

from .Pointer import Pointer
from .TaxResident import TaxResident
from .Address import Address
from .Avatar import Avatar
from .Amount import Amount
from .NotificationFilter import NotificationFilter
from .RelationUser import RelationUser