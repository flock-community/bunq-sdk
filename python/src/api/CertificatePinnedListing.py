from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CertificatePinnedListing:
  certificate_chain: 'Optional[str]'
  id: 'Optional[int]'

