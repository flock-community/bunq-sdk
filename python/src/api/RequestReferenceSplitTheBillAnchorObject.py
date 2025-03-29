from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class RequestReferenceSplitTheBillAnchorObject:
  BillingInvoice: 'Optional[Invoice]'
  DraftPayment: 'Optional[DraftPayment]'
  MasterCardAction: 'Optional[MasterCardAction]'
  Payment: 'Optional[Payment]'
  PaymentBatch: 'Optional[PaymentBatch]'
  RequestResponse: 'Optional[RequestResponse]'
  ScheduleInstance: 'Optional[ScheduleInstance]'
  WhitelistResult: 'Optional[WhitelistResult]'
  TransferwisePayment: 'Optional[TransferwiseTransfer]'
  CurrencyConversion: 'Optional[CurrencyConversion]'

from .Invoice import Invoice
from .DraftPayment import DraftPayment
from .MasterCardAction import MasterCardAction
from .Payment import Payment
from .PaymentBatch import PaymentBatch
from .RequestResponse import RequestResponse
from .ScheduleInstance import ScheduleInstance
from .WhitelistResult import WhitelistResult
from .TransferwiseTransfer import TransferwiseTransfer
from .CurrencyConversion import CurrencyConversion