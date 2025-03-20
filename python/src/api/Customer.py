from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class Customer:
  billing_account_id: Optional[str]
  invoice_notification_preference: Optional[str]
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
