from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from ..wirespec import T, Wirespec

@dataclass
class SessionServerCreate:
  Id: 'Optional[BunqId]'
  Token: 'Optional[SessionServerToken]'
  UserCompany: 'Optional[UserCompany]'
  UserPerson: 'Optional[UserPerson]'
  UserApiKey: 'Optional[UserApiKey]'
  UserPaymentServiceProvider: 'Optional[UserPaymentServiceProvider]'

from ..model.BunqId import BunqId
from ..model.SessionServerToken import SessionServerToken
from ..model.UserCompany import UserCompany
from ..model.UserPerson import UserPerson
from ..model.UserApiKey import UserApiKey
from ..model.UserPaymentServiceProvider import UserPaymentServiceProvider