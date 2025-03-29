from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class TreeProgressListing:
  number_of_tree: 'Optional[int]'
  progress_tree_next: 'Optional[int]'
  url_invite_profile: 'Optional[str]'
  label_user: 'Optional[LabelUser]'

from .LabelUser import LabelUser