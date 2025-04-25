from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class UserApiKeyAnchoredUser:
  UserPerson: 'Optional[UserPerson]'
  UserCompany: 'Optional[UserCompany]'
  UserPaymentServiceProvider: 'Optional[UserPaymentServiceProvider]'

from ..model.UserPerson import UserPerson
from ..model.UserCompany import UserCompany
from ..model.UserPaymentServiceProvider import UserPaymentServiceProvider