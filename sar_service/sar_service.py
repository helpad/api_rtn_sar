import mechanize
from bs4 import BeautifulSoup
from pydantic import BaseModel
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

# from api.schemas.sar_model import InfoRTNResponse

class InfoRTN(BaseModel):
    """
    Informacion de persona juridica
    """
    identificacion: str
    nombre: str
    rtn: str


class SarService:
    """
    Servicio para obtener informacion de persona juridica a partir de su RTN o DNI
    """

    def __init__(self, url: str = 'https://enlacertn.sar.gob.hn/index.aspx'):
        self.url = url

    def get_url(self) -> str:
        """
        Obtiene la url definida donde se obtiene la informacion
        """
        return self.url

    def get_sar_info(self, documento: str, numero: str) -> InfoRTN:
        """
        Obtiene información de persona juridica a partir de su RTN o DNI
        """
        documentos_dict = {
            'RTN': 'ruc',
            'DNI': 'identificacion'
        }

        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        browser.open(self.url)
        browser.select_form(nr=0)
        browser.form['RadioList'] = [documentos_dict[documento] or 'ruc']
        browser.form['txtCriterio'] = numero
        browser.submit()

        bs = BeautifulSoup(browser.response().read(), 'html.parser')
        browser.close()

        try:
            resp = InfoRTN(
                nombre=bs.find(id='LblNombre').text,
                rtn=bs.find(id='LblRuc').text,
                identificacion=bs.find(id='LblIdentificacion').text
            )
        except AttributeError:
            raise ValueError("Could not find information for the provided document and number")

        return resp
