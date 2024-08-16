import re
from typing import Annotated, Optional, Any
from pydantic import BaseModel, Field
from pydantic.functional_validators import BeforeValidator


def validate_phone(phone: str) -> str:
    phone_regex = re.compile(r'^\d{11}$')
    if not phone_regex.match(phone):
        raise ValueError(f'Неверный формат номера телефона: {phone}')
    return phone


def validate_address(address: str) -> str:
    if not address.strip():
        raise ValueError('Строка адреса не может быть пустой')
    return address

Phone = Annotated[str, BeforeValidator(validate_phone)]
Address = Annotated[str, BeforeValidator(validate_address)]


class DataIn(BaseModel):
    phone: Phone = Field(..., example="89090000000")
    address: Address = Field(..., example="Текстовый адрес")

class AddressOut(BaseModel):
    address: Address = Field(..., example="Текстовый адрес")

class ApiResponse(BaseModel):
    status: str = Field(..., example="success")
    code: int = Field(..., example=200)
    entity: Optional[Any] = None




