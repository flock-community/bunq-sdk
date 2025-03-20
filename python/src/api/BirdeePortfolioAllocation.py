from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional



@dataclass
class BirdeePortfolioAllocation:
  instrument_currency: Optional[str]
  instrument_asset_class: Optional[str]
  instrument_asset_class_name: Optional[str]
  instrument_isin: Optional[str]
  instrument_name: Optional[str]
  instrument_region_name: Optional[str]
  instrument_key_information_document_uri: Optional[str]
  weight: Optional[str]
  quantity: Optional[str]
  price: Optional[str]
  amount: Optional[str]
