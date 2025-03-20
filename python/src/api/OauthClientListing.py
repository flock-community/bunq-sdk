from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .OauthCallbackUrl import OauthCallbackUrl

@dataclass
class OauthClientListing:
  id: Optional[int]
  status: Optional[str]
  display_name: Optional[str]
  client_id: Optional[str]
  secret: Optional[str]
  callback_url: Optional[List[OauthCallbackUrl]]
