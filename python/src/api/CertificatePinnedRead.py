from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class CertificatePinnedRead:
  certificate_chain: Optional[str]
  id: Optional[int]
