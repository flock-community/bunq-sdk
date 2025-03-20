from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class NoteTextBunqMeFundraiserResult:
  content: Optional[str]
