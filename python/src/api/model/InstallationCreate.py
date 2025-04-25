from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class InstallationCreate:
  Id: 'Optional[BunqId]'
  Token: 'Optional[InstallationToken]'
  ServerPublicKey: 'Optional[InstallationServerPublicKey]'

from ..model.BunqId import BunqId
from ..model.InstallationToken import InstallationToken
from ..model.InstallationServerPublicKey import InstallationServerPublicKey