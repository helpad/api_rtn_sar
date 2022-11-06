from typing import Literal

from fastapi import FastAPI

from schemas.sar_model import InfoRTNResponse, InfoRTNRequest
from services.sar_service import SarService

app = FastAPI()


@app.get("/")
async def root():
    return {"documentation": "/docs"}


@app.get("/info_rtn", response_model=InfoRTNResponse)
async def get_info_rtn(documento: Literal["RTN", "DNI"], numero: str):
    _request = InfoRTNRequest(documento=documento, numero=numero)
    _sar_service = SarService('https://enlacertn.sar.gob.hn/index.aspx')

    return _sar_service.get_sar_info(_request.documento, _request.numero)
