from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

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

from ..model.BunqMeTab import BunqMeTab
from ..model.BunqMeTabResultResponse import BunqMeTabResultResponse
from ..model.BunqMeFundraiserResult import BunqMeFundraiserResult
from ..model.Card import Card
from ..model.CardDebit import CardDebit
from ..model.DraftPayment import DraftPayment
from ..model.FeatureAnnouncement import FeatureAnnouncement
from ..model.IdealMerchantTransaction import IdealMerchantTransaction
from ..model.Invoice import Invoice
from ..model.SchedulePayment import SchedulePayment
from ..model.SchedulePaymentBatch import SchedulePaymentBatch
from ..model.ScheduleInstance import ScheduleInstance
from ..model.MasterCardAction import MasterCardAction
from ..model.BankSwitchServiceNetherlandsIncomingPayment import BankSwitchServiceNetherlandsIncomingPayment
from ..model.Payment import Payment
from ..model.PaymentBatch import PaymentBatch
from ..model.RequestInquiryBatch import RequestInquiryBatch
from ..model.RequestInquiry import RequestInquiry
from ..model.RequestResponse import RequestResponse
from ..model.ShareInviteMonetaryAccountInquiry import ShareInviteMonetaryAccountInquiry
from ..model.ShareInviteMonetaryAccountResponse import ShareInviteMonetaryAccountResponse
from ..model.SofortMerchantTransaction import SofortMerchantTransaction
from ..model.TransferwiseTransfer import TransferwiseTransfer