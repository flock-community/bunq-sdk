from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class RelationUser:
  user_id: 'Optional[str]'
  counter_user_id: 'Optional[str]'
  label_user: 'Optional[LabelUser]'
  counter_label_user: 'Optional[LabelUser]'
  relationship: 'Optional[str]'
  status: 'Optional[str]'
  user_status: 'Optional[str]'
  counter_user_status: 'Optional[str]'
  company_employee_setting_adyen_card_transaction: 'Optional[CompanyEmployeeSettingAdyenCardTransaction]'
  all_company_employee_card: 'Optional[List[CompanyEmployeeCard]]'

from ..model.LabelUser import LabelUser
from ..model.CompanyEmployeeSettingAdyenCardTransaction import CompanyEmployeeSettingAdyenCardTransaction
from ..model.CompanyEmployeeCard import CompanyEmployeeCard