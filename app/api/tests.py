from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch
import requests


class ConsultaMantisTests(TestCase):

    def test_consulta_mantis_view_get(self):
        print("Iniciando teste: GET /consulta_mantis")
        try:
            response = self.client.get(reverse('consulta_mantis'))
            self.assertEqual(response.status_code, 200, "Falha: Status code GET não foi 200.")
            self.assertTemplateUsed(response, 'consulta_mantis.html', "Falha: Template consulta_mantis.html não foi usado.")
            print("✔️ Teste GET /consulta_mantis passou!")
        except AssertionError as e:
            print(f"❌ Teste GET /consulta_mantis falhou: {e}")
            raise

    @patch('requests.get')
    def test_consulta_mantis_view_post_valid(self, mock_get):
        print("Iniciando teste: POST /consulta_mantis com dados válidos")
        try:
            mock_response = {
                "issues": [{"id": 1, "summary": "Issue Teste"}]
            }
            mock_get.return_value.status_code = 200
            mock_get.return_value.json.return_value = mock_response

            response = self.client.post(reverse('consulta_mantis'), {'issue_id': 24806})
            self.assertEqual(response.status_code, 200, "Falha: Status code POST válido não foi 200.")
            self.assertTemplateUsed(response, 'mantis_issue.html', "Falha: Template mantis_issue.html não foi usado.")
            print("✔️ Teste POST /consulta_mantis com dados válidos passou!")
        except AssertionError as e:
            print(f"❌ Teste POST /consulta_mantis com dados válidos falhou: {e}")
            raise

    @patch('requests.get')
    def test_consulta_mantis_view_post_invalid(self, mock_get):
        print("Iniciando teste: POST /consulta_mantis com erro de API")
        try:
            mock_get.side_effect = requests.RequestException("Erro na API")

            response = self.client.post(reverse('consulta_mantis'), {'issue_id': 24806})
            self.assertEqual(response.status_code, 500, "Falha: Status code POST com erro de API não foi 500.")
            self.assertJSONEqual(response.content, {"error": "Erro ao buscar ou analisar os dados da issue do Mantis."}, "Falha: JSON de erro não corresponde.")
            print("✔️ Teste POST /consulta_mantis com erro de API passou!")
        except AssertionError as e:
            print(f"❌ Teste POST /consulta_mantis com erro de API falhou: {e}")
            raise

    def test_form_validation(self):
        print("Iniciando teste: Validação de formulário")
        try:
            response = self.client.post(reverse('consulta_mantis'), {'issue_id': 'abc'})
            self.assertContains(response, "O Issue ID deve ser numérico.", status_code=400, msg_prefix="Falha na validação: ")
            print("✔️ Teste de validação de formulário passou!")
        except AssertionError as e:
            print(f"❌ Teste de validação de formulário falhou: {e}")
            raise

