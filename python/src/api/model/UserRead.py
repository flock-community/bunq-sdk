from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class UserRead:
  UserPerson: 'Optional[UserPerson]'
  UserCompany: 'Optional[UserCompany]'
  UserApiKey: 'Optional[UserApiKey]'
  UserPaymentServiceProvider: 'Optional[UserPaymentServiceProvider]'

from ..model.UserPerson import UserPerson
from ..model.UserCompany import UserCompany
from ..model.UserApiKey import UserApiKey
from ..model.UserPaymentServiceProvider import UserPaymentServiceProvider