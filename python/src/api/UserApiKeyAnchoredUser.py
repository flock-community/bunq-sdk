from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class UserApiKeyAnchoredUser:
  UserPerson: 'Optional[UserPerson]'
  UserCompany: 'Optional[UserCompany]'
  UserPaymentServiceProvider: 'Optional[UserPaymentServiceProvider]'

from .UserPerson import UserPerson
from .UserCompany import UserCompany
from .UserPaymentServiceProvider import UserPaymentServiceProvider