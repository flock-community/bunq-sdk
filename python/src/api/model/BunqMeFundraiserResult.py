from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class BunqMeFundraiserResult:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  bunqme_fundraiser_profile: 'Optional[BunqMeFundraiserProfile]'
  payments: 'Optional[List[Payment]]'

from ..model.BunqMeFundraiserProfile import BunqMeFundraiserProfile
from ..model.Payment import Payment