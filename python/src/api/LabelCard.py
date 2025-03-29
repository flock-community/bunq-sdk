from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class LabelCard:
  uuid: 'Optional[str]'
  type: 'Optional[str]'
  second_line: 'Optional[str]'
  expiry_date: 'Optional[str]'
  status: 'Optional[str]'
  label_user: 'Optional[LabelUser]'

from .LabelUser import LabelUser