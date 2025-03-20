from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .Avatar import Avatar

@dataclass
class UserBlocklistMasterCardMerchant:
  merchant_name: Optional[str]
  merchant_id: Optional[str]
  merchant_identifier: Optional[str]
  mastercard_merchant_id: Optional[str]
  external_merchant_id: Optional[str]
  id: Optional[int]
  created: Optional[str]
  updated: Optional[str]
  status: Optional[str]
  merchant_hash: Optional[str]
  merchant_avatar: Optional[Avatar]
