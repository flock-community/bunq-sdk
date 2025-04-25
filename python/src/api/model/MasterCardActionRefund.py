from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class MasterCardActionRefund:
  type: 'Optional[str]'
  sub_type: 'Optional[str]'
  amount: 'Optional[Amount]'
  category: 'Optional[str]'
  reason: 'Optional[str]'
  comment: 'Optional[str]'
  attachment: 'Optional[List[AttachmentMasterCardActionRefund]]'
  terms_and_conditions: 'Optional[str]'
  id: 'Optional[int]'
  created: 'Optional[str]'
  updated: 'Optional[str]'
  label_user_creator: 'Optional[LabelUser]'
  status: 'Optional[str]'
  reference_mastercard_action_event: 'Optional[List[MasterCardActionReference]]'
  mastercard_action_id: 'Optional[int]'
  alias: 'Optional[LabelMonetaryAccount]'
  counterparty_alias: 'Optional[LabelMonetaryAccount]'
  description: 'Optional[str]'
  label_card: 'Optional[LabelCard]'
  time_refund: 'Optional[str]'
  additional_information: 'Optional[AdditionalInformation]'
  status_description: 'Optional[str]'
  status_description_translated: 'Optional[str]'
  status_together_url: 'Optional[str]'

from ..model.Amount import Amount
from ..model.AttachmentMasterCardActionRefund import AttachmentMasterCardActionRefund
from ..model.LabelUser import LabelUser
from ..model.MasterCardActionReference import MasterCardActionReference
from ..model.LabelMonetaryAccount import LabelMonetaryAccount
from ..model.LabelCard import LabelCard
from ..model.AdditionalInformation import AdditionalInformation