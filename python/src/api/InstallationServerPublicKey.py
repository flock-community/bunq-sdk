from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class InstallationServerPublicKey:
  server_public_key: 'Optional[str]'

