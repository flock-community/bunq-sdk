from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class PaymentListing:
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  monetary_account_id: 'Optional[int]'
  amount: 'Optional[Amount]'
  alias: 'Optional[LabelMonetaryAccount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  description: 'Optional[str]'
  type: 'Optional[str]'
  sub_type: 'Optional[str]'
  payment_arrival_expected: 'Optional[PaymentArrivalExpected]'
  bunqto_status: 'Optional[str]'
  bunqto_sub_status: 'Optional[str]'
  bunqto_share_url: 'Optional[str]'
  bunqto_expiry: 'Optional[str]'
  bunqto_time_responded: 'Optional[str]'
  attachment: 'Optional[List[AttachmentMonetaryAccountPayment]]'
  merchant_reference: 'Optional[str]'
  batch_id: 'Optional[int]'
  scheduled_id: 'Optional[int]'
  address_shipping: 'Optional[Address]'
  address_billing: 'Optional[Address]'
  geolocation: 'Optional[Geolocation]'
  request_reference_split_the_bill: 'Optional[List[RequestInquiryReference]]'
  balance_after_mutation: 'Optional[Amount]'
  payment_auto_allocate_instance: 'Optional[PaymentAutoAllocateInstance]'
  payment_suspended_outgoing: 'Optional[PaymentSuspendedOutgoing]'

from .Amount import Amount
from .LabelMonetaryAccount import LabelMonetaryAccount
from .PaymentArrivalExpected import PaymentArrivalExpected
from .AttachmentMonetaryAccountPayment import AttachmentMonetaryAccountPayment
from .Address import Address
from .Geolocation import Geolocation
from .RequestInquiryReference import RequestInquiryReference
from .PaymentAutoAllocateInstance import PaymentAutoAllocateInstance
from .PaymentSuspendedOutgoing import PaymentSuspendedOutgoing