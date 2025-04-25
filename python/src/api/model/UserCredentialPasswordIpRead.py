from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class UserCredentialPasswordIpRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  status: 'Optional[str]'
  expiry_time: 'Optional[str]'
  token_value: 'Optional[str]'
  permitted_device: 'Optional[PermittedDevice]'

from ..model.PermittedDevice import PermittedDevice