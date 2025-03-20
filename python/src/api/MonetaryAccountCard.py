from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Amount import Amount
from .Pointer import Pointer

@dataclass
class MonetaryAccountCard:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  currency: Optional[str]
  description: Optional[str]
  daily_limit: Optional[Amount]
  overdraft_limit: Optional[Amount]
  balance: Optional[Amount]
  balance_real: Optional[Amount]
  alias: Optional[List[Pointer]]
  public_uuid: Optional[str]
  status: Optional[str]
  sub_status: Optional[str]
  user_id: Optional[int]
