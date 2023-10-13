from typing import Literal

from fastapi import FastAPI, HTTPException

from api.schemas.sar_model import InfoRTNResponse, InfoRTNRequest
from sar_service import SarService

app = FastAPI()


@app.get("/")
async def root():
    return {"documentation": "/docs"}


@app.get("/info_rtn", response_model=InfoRTNResponse)
async def get_info_rtn(documento: Literal["RTN", "DNI"], numero: str):
    try:
        request = InfoRTNRequest(documento=documento, numero=numero)
    except ValueError as e:
        error_msg = "\n".join([f"{error['loc'][0]}: {error['msg']}" for error in e.errors()])
        raise HTTPException(status_code=402, detail=error_msg)

    sar_service = SarService('https://enlacertn.sar.gob.hn/index.aspx')

    try:
        return sar_service.get_sar_info(request.documento, request.numero)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
