from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class BunqMeFundraiserResultRead:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  bunqme_fundraiser_profile: 'Optional[BunqMeFundraiserProfile]'
  payments: 'Optional[List[Payment]]'

from .BunqMeFundraiserProfile import BunqMeFundraiserProfile
from .Payment import Payment