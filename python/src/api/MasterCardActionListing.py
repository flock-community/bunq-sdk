from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class MasterCardActionListing:
  id: 'Optional[int]'
  monetary_account_id: 'Optional[int]'
  card_id: 'Optional[int]'
  amount_local: 'Optional[Amount]'
  amount_converted: 'Optional[Amount]'
  amount_billing: 'Optional[Amount]'
  amount_original_local: 'Optional[Amount]'
  amount_original_billing: 'Optional[Amount]'
  amount_fee: 'Optional[Amount]'
  card_authorisation_id_response: 'Optional[str]'
  decision: 'Optional[str]'
  payment_status: 'Optional[str]'
  decision_description: 'Optional[str]'
  decision_description_translated: 'Optional[str]'
  decision_together_url: 'Optional[str]'
  description: 'Optional[str]'
  authorisation_status: 'Optional[str]'
  authorisation_type: 'Optional[str]'
  pan_entry_mode_user: 'Optional[str]'
  settlement_status: 'Optional[str]'
  clearing_status: 'Optional[str]'
  maturity_date: 'Optional[str]'
  city: 'Optional[str]'
  alias: 'Optional[LabelMonetaryAccount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  label_card: 'Optional[LabelCard]'
  merchant_id: 'Optional[str]'
  token_status: 'Optional[str]'
  reservation_expiry_time: 'Optional[str]'
  clearing_expiry_time: 'Optional[str]'
  applied_limit: 'Optional[str]'
  secure_code_id: 'Optional[int]'
  wallet_provider_id: 'Optional[str]'
  request_reference_split_the_bill: 'Optional[List[RequestInquiryReference]]'
  card_tokenization_event: 'Optional[Event]'
  all_mastercard_action_refund: 'Optional[List[MasterCardActionRefund]]'
  pos_card_presence: 'Optional[str]'
  pos_card_holder_presence: 'Optional[str]'
  eligible_whitelist_id: 'Optional[int]'
  cashback_payout_item: 'Optional[CashbackPayoutItem]'
  point_mutation: 'Optional[PointMutation]'
  blacklist: 'Optional[UserBlocklistMasterCardMerchant]'
  blocklist: 'Optional[UserBlocklistMasterCardMerchant]'
  additional_authentication_status: 'Optional[str]'
  pin_status: 'Optional[str]'
  mastercard_action_report: 'Optional[MasterCardActionReport]'
  merchant_category_code: 'Optional[str]'
  company_employee_card_receipt: 'Optional[CompanyEmployeeCardReceipt]'

from .Amount import Amount
from .LabelMonetaryAccount import LabelMonetaryAccount
from .LabelCard import LabelCard
from .RequestInquiryReference import RequestInquiryReference
from .Event import Event
from .MasterCardActionRefund import MasterCardActionRefund
from .CashbackPayoutItem import CashbackPayoutItem
from .PointMutation import PointMutation
from .UserBlocklistMasterCardMerchant import UserBlocklistMasterCardMerchant
from .MasterCardActionReport import MasterCardActionReport
from .CompanyEmployeeCardReceipt import CompanyEmployeeCardReceipt