from abc import abstractmethod
from dataclasses import dataclass
from .shared.Wirespec import T, Wirespec
from typing import List, Optional

from .BunqId import BunqId
from .SessionServerToken import SessionServerToken
from .UserCompany import UserCompany
from .UserPerson import UserPerson
from .UserApiKey import UserApiKey
from .UserPaymentServiceProvider import UserPaymentServiceProvider

@dataclass
class SessionServerCreate:
  Id: Optional[BunqId]
  Token: Optional[SessionServerToken]
  UserCompany: Optional[UserCompany]
  UserPerson: Optional[UserPerson]
  UserApiKey: Optional[UserApiKey]
  UserPaymentServiceProvider: Optional[UserPaymentServiceProvider]
