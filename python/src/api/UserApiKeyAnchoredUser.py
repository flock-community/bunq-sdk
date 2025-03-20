from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .UserPerson import UserPerson
from .UserCompany import UserCompany
from .UserPaymentServiceProvider import UserPaymentServiceProvider

@dataclass
class UserApiKeyAnchoredUser:
  UserPerson: Optional[UserPerson]
  UserCompany: Optional[UserCompany]
  UserPaymentServiceProvider: Optional[UserPaymentServiceProvider]
