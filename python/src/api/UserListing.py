from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class UserListing:
  UserPerson: 'Optional[UserPerson]'
  UserCompany: 'Optional[UserCompany]'
  UserApiKey: 'Optional[UserApiKey]'
  UserPaymentServiceProvider: 'Optional[UserPaymentServiceProvider]'

from .UserPerson import UserPerson
from .UserCompany import UserCompany
from .UserApiKey import UserApiKey
from .UserPaymentServiceProvider import UserPaymentServiceProvider