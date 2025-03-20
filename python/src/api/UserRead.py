from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .UserPerson import UserPerson
from .UserCompany import UserCompany
from .UserApiKey import UserApiKey
from .UserPaymentServiceProvider import UserPaymentServiceProvider

@dataclass
class UserRead:
  UserPerson: Optional[UserPerson]
  UserCompany: Optional[UserCompany]
  UserApiKey: Optional[UserApiKey]
  UserPaymentServiceProvider: Optional[UserPaymentServiceProvider]
