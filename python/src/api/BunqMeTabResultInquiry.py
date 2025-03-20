from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Payment import Payment

@dataclass
class BunqMeTabResultInquiry:
  payment: Optional[Payment]
  bunq_me_tab_id: Optional[int]
