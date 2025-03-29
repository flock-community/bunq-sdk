from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class InstallationCreate:
  Id: 'Optional[BunqId]'
  Token: 'Optional[InstallationToken]'
  ServerPublicKey: 'Optional[InstallationServerPublicKey]'

from .BunqId import BunqId
from .InstallationToken import InstallationToken
from .InstallationServerPublicKey import InstallationServerPublicKey