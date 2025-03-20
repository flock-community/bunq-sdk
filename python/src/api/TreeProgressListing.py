from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .LabelUser import LabelUser

@dataclass
class TreeProgressListing:
  number_of_tree: Optional[int]
  progress_tree_next: Optional[int]
  url_invite_profile: Optional[str]
  label_user: Optional[LabelUser]
