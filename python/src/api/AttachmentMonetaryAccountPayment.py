from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class AttachmentMonetaryAccountPayment:
  id: Optional[int]
  monetary_account_id: Optional[int]
