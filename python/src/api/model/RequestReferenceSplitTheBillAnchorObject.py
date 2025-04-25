from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

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

from ..model.Invoice import Invoice
from ..model.DraftPayment import DraftPayment
from ..model.MasterCardAction import MasterCardAction
from ..model.Payment import Payment
from ..model.PaymentBatch import PaymentBatch
from ..model.RequestResponse import RequestResponse
from ..model.ScheduleInstance import ScheduleInstance
from ..model.WhitelistResult import WhitelistResult
from ..model.TransferwiseTransfer import TransferwiseTransfer
from ..model.CurrencyConversion import CurrencyConversion