from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .ErrorArray import ErrorArray

@dataclass
class List_all_CallbackUrl_for_User_OauthClient400ResponseBody:
  Error: Optional[List[ErrorArray]]
