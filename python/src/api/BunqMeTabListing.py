from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class BunqMeTabListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  time_expiry: 'Optional[str]'
  monetary_account_id: 'Optional[int]'
  status: 'Optional[str]'
  type: 'Optional[str]'
  alias_monetary_account: 'Optional[LabelMonetaryAccount]'
  bunqme_tab_share_url: 'Optional[str]'
  bunqme_tab_entry: 'Optional[BunqMeTabEntry]'
  bunqme_tab_entries: 'Optional[List[BunqMeTabEntry]]'
  result_inquiries: 'Optional[List[BunqMeTabResultInquiry]]'

from .LabelMonetaryAccount import LabelMonetaryAccount
from .BunqMeTabEntry import BunqMeTabEntry
from .BunqMeTabEntry import BunqMeTabEntry
from .BunqMeTabResultInquiry import BunqMeTabResultInquiry