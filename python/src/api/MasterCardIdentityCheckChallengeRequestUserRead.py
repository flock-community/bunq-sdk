from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelMonetaryAccount import LabelMonetaryAccount

@dataclass
class MasterCardIdentityCheckChallengeRequestUserRead:
  amount: Optional[str]
  expiry_time: Optional[str]
  description: Optional[str]
  status: Optional[str]
  decision_description: Optional[str]
  decision_description_translated: Optional[str]
  url_merchant_app: Optional[str]
  counterparty_alias: Optional[LabelMonetaryAccount]
  event_id: Optional[int]
  card_id: Optional[int]
