from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Certificate import Certificate

@dataclass
class CertificatePinned:
  certificate_chain: List[Certificate]
