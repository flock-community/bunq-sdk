from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class UserPaymentServiceProviderRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  certificate_distinguished_name: 'Optional[str]'
  alias: 'Optional[List[Pointer]]'
  avatar: 'Optional[Avatar]'
  status: 'Optional[str]'
  sub_status: 'Optional[str]'
  public_uuid: 'Optional[str]'
  display_name: 'Optional[str]'
  public_nick_name: 'Optional[str]'
  language: 'Optional[str]'
  region: 'Optional[str]'
  session_timeout: 'Optional[int]'

from ..model.Pointer import Pointer
from ..model.Avatar import Avatar