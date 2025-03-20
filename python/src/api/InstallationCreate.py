from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .BunqId import BunqId
from .InstallationToken import InstallationToken
from .InstallationServerPublicKey import InstallationServerPublicKey

@dataclass
class InstallationCreate:
  Id: Optional[BunqId]
  Token: Optional[InstallationToken]
  ServerPublicKey: Optional[InstallationServerPublicKey]
