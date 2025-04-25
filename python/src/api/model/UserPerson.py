from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class UserPerson:
  subscription_type: 'Optional[str]'
  first_name: 'Optional[str]'
  middle_name: 'Optional[str]'
  last_name: 'Optional[str]'
  public_nick_name: 'Optional[str]'
  address_main: 'Optional[Address]'
  address_postal: 'Optional[Address]'
  avatar_uuid: 'Optional[str]'
  tax_resident: 'Optional[List[TaxResident]]'
  document_type: 'Optional[str]'
  document_number: 'Optional[str]'
  document_country_of_issuance: 'Optional[str]'
  document_front_attachment_id: 'Optional[int]'
  document_back_attachment_id: 'Optional[int]'
  date_of_birth: 'Optional[str]'
  nationality: 'Optional[str]'
  all_nationality: 'Optional[List[str]]'
  language: 'Optional[str]'
  region: 'Optional[str]'
  gender: 'Optional[str]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  legal_guardian_alias: 'Optional[Pointer]'
  session_timeout: 'Optional[int]'
  daily_limit_without_confirmation_login: 'Optional[Amount]'
  display_name: 'Optional[str]'
  signup_track_type: 'Optional[str]'
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  public_uuid: 'Optional[str]'
  legal_name: 'Optional[str]'
  alias: 'Optional[List[Pointer]]'
  place_of_birth: 'Optional[str]'
  country_of_birth: 'Optional[str]'
  avatar: 'Optional[Avatar]'
  version_terms_of_service: 'Optional[str]'
  notification_filters: 'Optional[List[NotificationFilter]]'
  relations: 'Optional[List[RelationUser]]'

from ..model.Address import Address
from ..model.TaxResident import TaxResident
from ..model.Pointer import Pointer
from ..model.Amount import Amount
from ..model.Pointer import Pointer
from ..model.Avatar import Avatar
from ..model.NotificationFilter import NotificationFilter
from ..model.RelationUser import RelationUser