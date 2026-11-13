import json
import os
import subprocess
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

import escolher  # noqa: E402


def roda(*args, entrada=None):
    return subprocess.run([sys.executable, os.path.join(RAIZ, "escolher.py"), *args],
                          capture_output=True, text=True, input=entrada)


class TestDecidir(unittest.TestCase):
    def test_tabela(self):
        self.assertEqual(escolher.decidir(divide_limpo=True), "swarm")
        self.assertEqual(escolher.decidir(dificil=True), "boost")
        self.assertEqual(escolher.decidir(dias=True), "teamwork")
        self.assertEqual(escolher.decidir(lateral=True), "subagente")
        self.assertEqual(escolher.decidir(), "agente")

    def test_precedencia(self):
        self.assertEqual(escolher.decidir(divide_limpo=True, dias=True), "teamwork")
        self.assertEqual(escolher.decidir(divide_limpo=True, dificil=True), "swarm")
        self.assertEqual(escolher.decidir(lateral=True, dificil=True), "subagente")

    def test_planos_da_tabela_oficial(self):
        self.assertIn("Pro", escolher.OPCOES["swarm"]["plano"])
        self.assertIn("Ultra", escolher.OPCOES["swarm"]["plano"])
        self.assertEqual(escolher.OPCOES["boost"]["plano"], "planos pagos")
        self.assertEqual(escolher.OPCOES["teamwork"]["plano"], "planos pagos")
        self.assertEqual(escolher.OPCOES["subagente"]["plano"], "todos os planos")


class TestCLI(unittest.TestCase):
    def test_flags(self):
        r = roda("--divide-limpo", "sim")
        self.assertEqual(r.returncode, 0)
        self.assertIn("Use: /swarm", r.stdout)
        self.assertIn("Google AI Pro", r.stdout)
        self.assertIn("checar.py", r.stdout)
        self.assertIn("Use: /boost", roda("--dificil").stdout)
        self.assertIn("Use: /teamwork", roda("--dias").stdout)
        self.assertIn("subagente", roda("--lateral").stdout)
        self.assertIn("agente padrão", roda("--divide-limpo", "nao").stdout)

    def test_aviso_swarm_e_dificil(self):
        self.assertIn("/boost", roda("--divide-limpo", "sim", "--dificil").stdout)

    def test_json(self):
        d = json.loads(roda("--dias", "--json").stdout)
        self.assertEqual(d["escolha"], "teamwork")

    def test_sem_flag_sem_terminal(self):
        self.assertEqual(roda(entrada="").returncode, 2)

    def test_perguntas(self):
        r = roda("--perguntar", entrada="n\nn\ns\nn\n")
        self.assertIn("Use: /swarm", r.stdout)
        r = roda("--perguntar", entrada="s\n")
        self.assertIn("Use: /teamwork", r.stdout)

    def test_resposta_invalida_pergunta_de_novo(self):
        respostas = iter(["talvez", "n", "n", "n", "s"])
        self.assertEqual(escolher.decidir(**escolher.perguntar(lambda _: next(respostas))), "boost")


if __name__ == "__main__":
    unittest.main()
