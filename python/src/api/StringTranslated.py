from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class StringTranslated:
  de_DE: 'Optional[str]'
  en_US: 'Optional[str]'
  es_ES: 'Optional[str]'
  fr_FR: 'Optional[str]'
  hi_IN: 'Optional[str]'
  it_IT: 'Optional[str]'
  nl_NL: 'Optional[str]'
  pl_PL: 'Optional[str]'
  pt_PT: 'Optional[str]'
  ru_RU: 'Optional[str]'
  uk_UA: 'Optional[str]'

