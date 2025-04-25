from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MonetaryAccountSetting:
  color: 'Optional[str]'
  icon: 'Optional[str]'
  default_avatar_status: 'Optional[str]'
  restriction_chat: 'Optional[str]'
  sdd_expiration_action: 'Optional[str]'

