import os
import subprocess
import sys
import unittest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RAIZ)

import checar  # noqa: E402

EXEMPLOS = ["calculadora-roi", "landing-page", "investigacao-lenta", "testes-por-pacote"]

BOA = """# Tarefa
Adicionar testes às funções de data e de moeda.

## Como verificar
- comando: `npm test`

## Peças

### @datas
- dono: `src/utils/date.ts`
- não mexe: `src/utils/currency.ts`
- pronto quando: testes de data passam

### @moeda
- dono: `src/utils/currency.ts`
- não mexe: `src/utils/date.ts`
- pronto quando: testes de moeda passam

## Verificador
- modelo: diferente dos workers
- roda: lê os diffs e roda `npm test`

## Limites
- cota: 2 workers e 1 verificador
- parar: quando `npm test` passar
- limpar workers: remover no fim
- sem laço: nada de rodar /swarm em laço sem supervisão
"""


def ler(caminho):
    with open(os.path.join(RAIZ, caminho), encoding="utf-8") as f:
        return f.read()


def item(res, n):
    return next(i for i in res["itens"] if i["n"] == n)


class TestExemplos(unittest.TestCase):
    def test_calculadora_tem_4_entradas(self):
        t = ler("exemplos/calculadora-roi/ficha.md")
        for campo in ("tráfego mensal", "taxa de conversão", "ticket médio", "aumento estimado"):
            self.assertIn(campo, t)
        self.assertIn("(aumento/100) × (conversão/100)", t)

    def test_exemplos_tiram_8(self):
        for nome in EXEMPLOS:
            with self.subTest(nome=nome):
                res = checar.checar(ler(f"exemplos/{nome}/ficha.md"))
                self.assertEqual(res["nota"], 8, [i for i in res["itens"] if not i["ok"]])

    def test_ruim_tira_nota_baixa(self):
        res = checar.checar(ler("exemplos/ruim.md"))
        self.assertLessEqual(res["nota"], 3)
        for n in (2, 5, 7, 8):
            self.assertFalse(item(res, n)["ok"], n)

    def test_modelo_vazio_nao_passa(self):
        self.assertLess(checar.checar(ler("modelos/FICHA.md"))["nota"], checar.NOTA_MINIMA)

    def test_codigo_de_saida(self):
        for nome, esperado in [("exemplos/calculadora-roi/ficha.md", 0), ("exemplos/ruim.md", 1)]:
            r = subprocess.run([sys.executable, os.path.join(RAIZ, "checar.py"), os.path.join(RAIZ, nome)],
                               capture_output=True, text=True)
            self.assertEqual(r.returncode, esperado, r.stdout)
        r = subprocess.run([sys.executable, os.path.join(RAIZ, "checar.py"), "/nao/existe.md"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2)

    def test_prompt_txt_igual_ao_gerado(self):
        for nome in EXEMPLOS:
            with self.subTest(nome=nome):
                res = checar.checar(ler(f"exemplos/{nome}/ficha.md"))
                self.assertEqual(ler(f"exemplos/{nome}/prompt.txt").strip(), checar.montar_prompt(res))
                self.assertEqual(ler(f"exemplos/{nome}/prompt.en.txt").strip(), checar.montar_prompt(res, en=True))


class TestItens(unittest.TestCase):
    def test_boa_tira_8(self):
        self.assertEqual(checar.checar(BOA)["nota"], 8)

    def test_uma_peca_so(self):
        t = BOA.split("### @moeda")[0] + "## Verificador" + BOA.split("## Verificador")[1]
        res = checar.checar(t)
        self.assertFalse(item(res, 3)["ok"])
        self.assertIn("subagente", item(res, 3)["corrigir"])

    def test_sem_comando(self):
        res = checar.checar(BOA.replace("- comando: `npm test`", "ver se funciona"))
        self.assertFalse(item(res, 2)["ok"])

    def test_sem_dono(self):
        res = checar.checar(BOA.replace("- dono: `src/utils/currency.ts`\n", ""))
        self.assertFalse(item(res, 4)["ok"])

    def test_mesmo_arquivo(self):
        res = checar.checar(BOA.replace("- dono: `src/utils/currency.ts`", "- dono: `src/utils/date.ts`"))
        self.assertFalse(item(res, 5)["ok"])

    def test_pasta_que_contem(self):
        res = checar.checar(BOA.replace("- dono: `src/utils/currency.ts`", "- dono: `src/utils/`"))
        self.assertFalse(item(res, 5)["ok"])
        self.assertIn("src/utils/", item(res, 5)["motivo"])

    def test_sem_nao_mexe_ou_pronto(self):
        res = checar.checar(BOA.replace("- pronto quando: testes de moeda passam\n", ""))
        self.assertFalse(item(res, 6)["ok"])

    def test_sem_verificador(self):
        t = BOA.split("## Verificador")[0] + "## Limites" + BOA.split("## Limites")[1]
        self.assertFalse(item(checar.checar(t), 7)["ok"])

    def test_verificador_sem_modelo_e_aviso(self):
        res = checar.checar(BOA.replace("- modelo: diferente dos workers\n", ""))
        self.assertTrue(item(res, 7)["ok"])
        self.assertTrue(any("modelo" in a for a in item(res, 7)["avisos"]))

    def test_proporcao_avisa(self):
        pecas = "".join(f"\n### @p{i}\n- dono: `p{i}/`\n- não mexe: as outras\n- pronto quando: testes passam\n" for i in range(6))
        t = BOA.split("## Peças")[0] + "## Peças\n" + pecas + "\n## Verificador" + BOA.split("## Verificador")[1]
        res = checar.checar(t)
        self.assertEqual(res["nota"], 8)
        self.assertTrue(any("2" in a for a in item(res, 7)["avisos"]))

    def test_sem_limites(self):
        t = BOA.split("## Limites")[0]
        self.assertFalse(item(checar.checar(t), 8)["ok"])

    def test_laco_sem_supervisao_reprova(self):
        res = checar.checar(BOA + "- rodar o /swarm em laço a noite toda sem supervisão\n")
        self.assertFalse(item(res, 8)["ok"])

    def test_negacao_do_laco_passa(self):
        res = checar.checar(BOA.replace("nada de rodar /swarm em laço sem supervisão",
                                        "nunca deixar rodando à noite em laço"))
        self.assertTrue(item(res, 8)["ok"])

    def test_loop_no_codigo_nao_e_laco(self):
        res = checar.checar(BOA.replace("Adicionar testes", "Corrigir o loop de retry e adicionar testes"))
        self.assertTrue(item(res, 8)["ok"])


class TestSobreposicao(unittest.TestCase):
    def test_casos(self):
        casos = [
            ("a.js", "a.js", True), ("./a.js", "a.js", True), ("src/", "src/x.js", True),
            ("src", "src/x.js", True), ("src/a.js", "src/b.js", False), ("src/a", "src/ab.js", False),
            ("src/*.js", "src/x.js", True), ("src/*.js", "src/x.css", False),
            ("tests/test_a*.py", "tests/test_b*.py", False), ("src/*.js", "src/**/*.js", True),
            ("src/*.js", "src/*.css", False),
        ]
        for a, b, esperado in casos:
            with self.subTest(a=a, b=b):
                self.assertEqual(checar.se_sobrepoe(a, b), esperado)

    def test_pergunta_nao_e_caminho(self):
        self.assertEqual(checar.caminhos("pergunta: por que demora?"), [])


class TestPrompt(unittest.TestCase):
    def test_pt(self):
        p = checar.montar_prompt(checar.checar(BOA))
        self.assertTrue(p.startswith("/swarm Adicionar testes"))
        self.assertIn("@datas é dono de src/utils/date.ts", p)
        self.assertIn("modelo diferente do dos workers", p)
        self.assertIn("rode npm test", p)
        self.assertNotIn("\n", p)

    def test_en(self):
        p = checar.montar_prompt(checar.checar(BOA), en=True)
        self.assertIn("Give each piece its own worker", p)
        self.assertIn("@moeda owns src/utils/currency.ts", p)
        self.assertIn("different model than the workers", p)
        self.assertIn("Verify with npm test", p)

    def test_json(self):
        r = subprocess.run([sys.executable, os.path.join(RAIZ, "checar.py"),
                            os.path.join(RAIZ, "exemplos/ruim.md"), "--json", "--prompt"],
                           capture_output=True, text=True)
        import json
        d = json.loads(r.stdout)
        self.assertEqual(d["maximo"], 8)
        self.assertEqual(len(d["itens"]), 8)
        self.assertIn("prompt", d)
        self.assertIsNone(d["prompt"])  # nota 2/8: sem texto do /swarm

    def test_prompt_so_com_nota_7(self):
        r = subprocess.run([sys.executable, os.path.join(RAIZ, "checar.py"),
                            os.path.join(RAIZ, "exemplos/ruim.md"), "--prompt"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 1)
        self.assertNotIn("/swarm Melhorar", r.stdout)
        self.assertIn("2/8", r.stdout)
        self.assertIn("como corrigir", r.stdout)
        r = subprocess.run([sys.executable, os.path.join(RAIZ, "checar.py"),
                            os.path.join(RAIZ, "exemplos/calculadora-roi/ficha.md"), "--prompt"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertTrue(r.stdout.startswith("/swarm "))


if __name__ == "__main__":
    unittest.main()
