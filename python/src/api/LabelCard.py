from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelUser import LabelUser

@dataclass
class LabelCard:
  uuid: Optional[str]
  type: Optional[str]
  second_line: Optional[str]
  expiry_date: Optional[str]
  status: Optional[str]
  label_user: Optional[LabelUser]
