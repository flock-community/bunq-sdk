from abc import abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from .shared.Wirespec import T, Wirespec

@dataclass
class TransferwiseRequirementFieldGroup:
  key: 'Optional[str]'
  type: 'Optional[str]'
  name: 'Optional[str]'
  refresh_requirements_on_change: 'Optional[bool]'
  required: 'Optional[bool]'
  display_format: 'Optional[str]'
  example: 'Optional[str]'
  min_length: 'Optional[str]'
  max_length: 'Optional[str]'
  validation_regexp: 'Optional[str]'
  validation_async: 'Optional[TransferwiseRequirementFieldGroupValidationAsync]'
  values_allowed: 'Optional[TransferwiseRequirementFieldGroupValuesAllowed]'

from .TransferwiseRequirementFieldGroupValidationAsync import TransferwiseRequirementFieldGroupValidationAsync
from .TransferwiseRequirementFieldGroupValuesAllowed import TransferwiseRequirementFieldGroupValuesAllowed