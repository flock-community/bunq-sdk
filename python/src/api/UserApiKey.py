from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .UserApiKeyAnchoredUser import UserApiKeyAnchoredUser

@dataclass
class UserApiKey:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  requested_by_user: Optional[UserApiKeyAnchoredUser]
  granted_by_user: Optional[UserApiKeyAnchoredUser]
