from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class CertificatePinned:
  certificate_chain: 'List[Certificate]'

from .Certificate import Certificate