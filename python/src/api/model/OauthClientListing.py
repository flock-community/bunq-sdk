from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class OauthClientListing:
  id: 'Optional[int]'
  status: 'Optional[str]'
  display_name: 'Optional[str]'
  client_id: 'Optional[str]'
  secret: 'Optional[str]'
  callback_url: 'Optional[List[OauthCallbackUrl]]'

from ..model.OauthCallbackUrl import OauthCallbackUrl