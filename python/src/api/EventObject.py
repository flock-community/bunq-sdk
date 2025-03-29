from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class EventObject:
  BunqMeTab: 'Optional[BunqMeTab]'
  BunqMeTabResultResponse: 'Optional[BunqMeTabResultResponse]'
  BunqMeFundraiserResult: 'Optional[BunqMeFundraiserResult]'
  Card: 'Optional[Card]'
  CardDebit: 'Optional[CardDebit]'
  DraftPayment: 'Optional[DraftPayment]'
  FeatureAnnouncement: 'Optional[FeatureAnnouncement]'
  IdealMerchantTransaction: 'Optional[IdealMerchantTransaction]'
  Invoice: 'Optional[Invoice]'
  ScheduledPayment: 'Optional[SchedulePayment]'
  ScheduledPaymentBatch: 'Optional[SchedulePaymentBatch]'
  ScheduledInstance: 'Optional[ScheduleInstance]'
  MasterCardAction: 'Optional[MasterCardAction]'
  BankSwitchServiceNetherlandsIncomingPayment: 'Optional[BankSwitchServiceNetherlandsIncomingPayment]'
  Payment: 'Optional[Payment]'
  PaymentBatch: 'Optional[PaymentBatch]'
  RequestInquiryBatch: 'Optional[RequestInquiryBatch]'
  RequestInquiry: 'Optional[RequestInquiry]'
  RequestResponse: 'Optional[RequestResponse]'
  ShareInviteBankInquiry: 'Optional[ShareInviteMonetaryAccountInquiry]'
  ShareInviteBankResponse: 'Optional[ShareInviteMonetaryAccountResponse]'
  SofortMerchantTransaction: 'Optional[SofortMerchantTransaction]'
  TransferwisePayment: 'Optional[TransferwiseTransfer]'

from .BunqMeTab import BunqMeTab
from .BunqMeTabResultResponse import BunqMeTabResultResponse
from .BunqMeFundraiserResult import BunqMeFundraiserResult
from .Card import Card
from .CardDebit import CardDebit
from .DraftPayment import DraftPayment
from .FeatureAnnouncement import FeatureAnnouncement
from .IdealMerchantTransaction import IdealMerchantTransaction
from .Invoice import Invoice
from .SchedulePayment import SchedulePayment
from .SchedulePaymentBatch import SchedulePaymentBatch
from .ScheduleInstance import ScheduleInstance
from .MasterCardAction import MasterCardAction
from .BankSwitchServiceNetherlandsIncomingPayment import BankSwitchServiceNetherlandsIncomingPayment
from .Payment import Payment
from .PaymentBatch import PaymentBatch
from .RequestInquiryBatch import RequestInquiryBatch
from .RequestInquiry import RequestInquiry
from .RequestResponse import RequestResponse
from .ShareInviteMonetaryAccountInquiry import ShareInviteMonetaryAccountInquiry
from .ShareInviteMonetaryAccountResponse import ShareInviteMonetaryAccountResponse
from .SofortMerchantTransaction import SofortMerchantTransaction
from .TransferwiseTransfer import TransferwiseTransfer