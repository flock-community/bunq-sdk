from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class Fulfillment:
  type: 'Optional[str]'
  reason: 'Optional[str]'
  reason_translated: 'Optional[str]'
  status: 'Optional[str]'
  time_mandatory: 'Optional[str]'
  user_id: 'Optional[int]'
  all_status_allowed: 'Optional[List[str]]'

