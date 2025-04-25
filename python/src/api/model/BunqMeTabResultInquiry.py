from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class BunqMeTabResultInquiry:
  payment: 'Optional[Payment]'
  bunq_me_tab_id: 'Optional[int]'

from ..model.Payment import Payment