import unittest
from unittest.mock import MagicMock, patch

from api.schemas.sar_model import InfoRTNResponse
from api.services.sar_service import SarService


class TestSarService(unittest.TestCase):
    def setUp(self):
        self.service = SarService()

    def test_get_url(self):
        expected_url = 'https://enlacertn.sar.gob.hn/index.aspx'
        self.assertEqual(self.service.get_url(), expected_url)

    @patch('api.services.sar_service.mechanize.Browser')
    def test_get_sar_info(self, mock_browser):
        mock_form = MagicMock()
        mock_form.__getitem__.return_value = None
        mock_browser.return_value.select_form.return_value = mock_form
        mock_response = MagicMock()
        mock_response.read.return_value = "<html><body><label id='LblNombre'>Juan Perez</label><label id='LblRuc'>08011995003836</label><label id='LblIdentificacion'>08011995003836</label></body></html>"
        mock_browser.return_value.response.return_value = mock_response

        rtn = '08011995003836'
        documento = 'RTN'
        expected_resp = InfoRTNResponse(nombre='Juan Perez', rtn=rtn, identificacion=rtn)
        resp = self.service.get_sar_info(documento, rtn)

        self.assertEqual(resp, expected_resp)

    @patch('api.services.sar_service.mechanize.Browser')
    def test_get_sar_info_attribute_error(self, mock_browser):
        mock_form = MagicMock()
        mock_form.__getitem__.return_value = None
        mock_browser.return_value.select_form.return_value = mock_form
        mock_response = MagicMock()
        mock_response.read.return_value = "<html><body><label>Some Error</label></body></html>"
        mock_browser.return_value.response.return_value = mock_response

        with self.assertRaises(ValueError):
            rtn = '08011995003836'
            documento = 'RTN'
            self.service.get_sar_info(documento, rtn)
