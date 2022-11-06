from enum import Enum
from typing import Literal

from pydantic import BaseModel, validator


class DocEnum(str, Enum):
    RTN = 'ruc'
    DNI = 'identificacion'

class InfoRTN(BaseModel):
    """
    Informacion de persona juridica
    """
    identificacion: str
    nombre: str
    rtn: str


class InfoRTNRequest(BaseModel):
    """
    DTO para la consulta de informacion de persona juridica
    """
    documento: Literal["RTN", "DNI"]
    numero: str

    @validator('numero')
    def numero_debe_tener_longitud_correcta(cls, v, values):
        if values['documento'] == 'RTN' and len(v) != 14:
            raise ValueError('Longitud de RTN debe ser 14')
        if values['documento'] == 'DNI' and len(v) != 13:
            raise ValueError('Longitud de DNI debe ser 13')
        return v


class InfoRTNResponse(InfoRTN):
    """
    DTO para la respuesta
    """
    pass
