from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class LabelUser:
  uuid: 'Optional[str]'
  display_name: 'Optional[str]'
  country: 'Optional[str]'
  avatar: 'Optional[Avatar]'
  public_nick_name: 'Optional[str]'

from .Avatar import Avatar