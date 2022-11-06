import mechanize
from bs4 import BeautifulSoup

from schemas.sar_model import InfoRTNResponse


class SarService:

    def __init__(self, url):
        self.url = url

    def get_url(self):
        return self.url

    def get_sar_info(self, documento, numero):
        _documentos_dict = {
            'RTN': 'ruc',
            'DNI': 'identificacion'
        }

        print('Documento', str([_documentos_dict[documento]]))

        _browser = mechanize.Browser()
        _browser.open(self.url)
        _browser.select_form(nr=0)
        _browser.form['RadioList'] = [_documentos_dict[documento] or 'ruc']
        _browser.form['txtCriterio'] = numero
        _browser.submit()

        _bs = BeautifulSoup(_browser.response().read(), 'html.parser')

        _browser.close()

        _resp = InfoRTNResponse(
            nombre=_bs.find(id='LblNombre').text,
            rtn=_bs.find(id='LblRuc').text,
            identificacion=_bs.find(id='LblIdentificacion').text
        )

        return _resp
