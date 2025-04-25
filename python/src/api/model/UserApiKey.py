from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class UserApiKey:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  requested_by_user: 'Optional[UserApiKeyAnchoredUser]'
  granted_by_user: 'Optional[UserApiKeyAnchoredUser]'

from ..model.UserApiKeyAnchoredUser import UserApiKeyAnchoredUser