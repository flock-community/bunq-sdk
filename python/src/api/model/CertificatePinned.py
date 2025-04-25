from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class CertificatePinned:
  certificate_chain: 'List[Certificate]'

from ..model.Certificate import Certificate