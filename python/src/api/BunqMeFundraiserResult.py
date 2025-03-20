from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .BunqMeFundraiserProfile import BunqMeFundraiserProfile
from .Payment import Payment

@dataclass
class BunqMeFundraiserResult:
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  bunqme_fundraiser_profile: Optional[BunqMeFundraiserProfile]
  payments: Optional[List[Payment]]
