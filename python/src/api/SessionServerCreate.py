from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class SessionServerCreate:
  Id: 'Optional[BunqId]'
  Token: 'Optional[SessionServerToken]'
  UserCompany: 'Optional[UserCompany]'
  UserPerson: 'Optional[UserPerson]'
  UserApiKey: 'Optional[UserApiKey]'
  UserPaymentServiceProvider: 'Optional[UserPaymentServiceProvider]'

from .BunqId import BunqId
from .SessionServerToken import SessionServerToken
from .UserCompany import UserCompany
from .UserPerson import UserPerson
from .UserApiKey import UserApiKey
from .UserPaymentServiceProvider import UserPaymentServiceProvider