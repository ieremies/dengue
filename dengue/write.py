#!/usr/bin/env python3
#!/usr/bin/env python3
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from pypdf import PdfReader, PdfWriter

from math import floor
from dengue.parse import usuario, parse
from dengue.debug import debug
import os
import requests
from datetime import datetime, timedelta


class writer:
    def __init__(self, user: usuario):
        self.user = user
        self.w, self.h = A4
        self.offset = 0

        name = self.user.nome.split()
        if len(name) > 0:
            pdf_name = f"{name[0].lower()}_{name[-1].lower()}.pdf"
        else:
            pdf_name = f"notificacao.pdf"

        if os.name == "nt":  # windows
            self.save_path = os.path.join(os.path.expanduser("~"), "Desktop/", pdf_name)
        else:  # linux
            self.save_path = "./tmp/" + pdf_name

        # check if tmp folder exists
        if not os.path.exists("./tmp"):
            os.makedirs("./tmp")

        self.c = canvas.Canvas(self.save_path, pagesize=A4)

    def write_dados_gerais(self):
        self.write_spaced(self.user.data, (452, 652))
        self.write_spaced(self.user.uf, (59, 623))
        self.write(self.user.municipio, (92, 624))
        # self.write_spaced(self.user.ibge, (482, 623), 15)
        self.write(self.user.ubs, (62, 595))
        self.write_spaced(self.user.ubs_code, (343, 595))
        # skip data primeiros sintomas

    def write_notificacao_individual(self):
        self.write(self.user.nome, (62, 564))
        self.write_spaced(self.user.nascimento, (449, 564))
        # skip idade
        if len(self.user.sexo) > 0:
            self.write_spaced(self.user.sexo[0], (232, 548))
        # skip gestante
        self.write_spaced(self._code_raca(self.user.raca), (552, 548))
        self.write_spaced(self._code_esco(self.user.escolaridade), (552, 519))
        self.write_spaced(self.user.n_sus, (54, 474), 11.7)
        self.write(self.user.nome_mae, (236, 474))

    def write_dados_residencia(self):
        self.write_spaced(self.user.uf_residencia, (54, 443))
        self.write(self.user.municipio_residencia, (84, 444))
        self.write_spaced(self.user.ibge_residencia, (326, 444))
        self.write(self.user.distrito_residencia, (414, 444))
        self.write(self.user.bairro_residencia, (64, 419))
        self.write(self.user.logradouro_residencia, (198, 418))
        self.write_spaced(self.user.cod_logradouro_residencia, (479, 418))
        self.write(self.user.numero_residencia, (63, 395))
        self.write(self.user.complemento_residencia, (120, 395))
        self.write_spaced(self.user.complemento_residencia, (225, 369))
        # skip geo gampo 1
        # skip geo campo 2
        # skip ponto de referência
        self.write_spaced(self.user.cep_residencia, (458, 367), 14)
        self.write_spaced(self.user.telefone_residencia, (56, 343), 15)

        match self.user.zona_residencia:
            case "Urbana":
                zona = 1
            case "Rural":
                zona = 2
            case "Periurbana":
                zona = 3
            case _:
                zona = 9
        self.write_spaced(str(zona), (334, 354))

    def _code_esco(self, esco: str) -> str:
        esco = esco.lower()
        # remove acentos
        esco.replace("ã", "a").replace("é", "e").replace("ç", "c")

        if "analfabeto" in esco:
            return "0"
        if all(w in esco for w in ["1", "4", "serie", "incompleto"]):
            return "1"
        if all(w in esco for w in ["4", "serie", "completo"]):
            return "2"
        if all(w in esco for w in ["5", "8", "serie", "incompleto"]):
            return "3"
        if all(w in esco for w in ["fundamental", "completo"]):
            return "4"
        if all(w in esco for w in ["medio", "incompleto"]):
            return "5"
        if all(w in esco for w in ["medio", "completo"]):
            return "6"
        if all(w in esco for w in ["superior", "incompleto"]):
            return "7"
        if all(w in esco for w in ["superior", "completo"]):
            return "8"
        return ""

    def _code_raca(self, raca: str) -> str:
        raca = raca.lower()
        if "branca" in raca:
            return "1"
        if "preta" in raca:
            return "2"
        if "amarela" in raca:
            return "3"
        if "parda" in raca:
            return "4"
        if "indigena" in raca:
            return "5"
        return ""

    def write_spaced(
        self, to_write: str, coord: tuple[int, int], spacing: float = 14.5
    ):
        print("spaced", to_write)
        self.c.setFont("Times-Roman", 10)
        x, y = coord
        for char in to_write.replace("/", "").strip():
            self.c.drawString(x, y + self.offset, char)
            x += spacing

    def write(self, to_write: str, coord: tuple[int, int]):
        self.c.setFont("Times-Roman", 10)
        print("non", to_write)
        x, y = coord
        self.c.drawString(x, y + self.offset, to_write.strip())

    def draw_grid(self):
        self.c.setStrokeColorRGB(0.1, 0.1, 0.1)
        self.c.setFont("Times-Roman", 3)
        for x in range(10, floor(self.w), 10):
            self.c.line(x, 0, x, self.h)

        for y in range(10, floor(self.h), 10):
            self.c.line(0, y, self.w, y)

        for x in range(10, floor(self.w), 10):
            for y in range(10, floor(self.h), 10):
                self.c.drawString(x + 1, y + 1, f"{x//10}|{y//10}")

    def file_exists_and_not_old(self, file_path: str):
        if not os.path.exists(file_path):
            return False

        file_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        current_time = datetime.now()
        max_age = timedelta(hours=12)

        return current_time - file_modified_time < max_age

    def check_exists_file(self, file):
        # if file exists

        if self.file_exists_and_not_old("tmp/" + file):
            return

        url = f"https://dengue.ieremies.dev/data/{file}"
        response = requests.get(url)
        if response.status_code == 200:
            with open("tmp/" + file, "wb") as f:
                f.write(response.content)

    def merge_sinan(self):
        self.check_exists_file("sinan1.pdf")

        base_pdf = PdfReader(open("tmp/sinan1.pdf", "rb"))
        base = base_pdf.pages[0]
        overlay = PdfReader(open(self.save_path, "rb")).pages[0]
        base.merge_page(overlay)

        output_pdf = PdfWriter()
        output_pdf.add_page(base)
        output_pdf.add_page(base_pdf.pages[1])

        # Write the merged PDF to a new file
        with open(self.save_path, "wb") as output_file:
            output_pdf.write(output_file)

    def save(self):
        self.write_dados_gerais()
        self.write_notificacao_individual()
        self.write_dados_residencia()
        self.c.showPage()
        # self.offset = 89
        # self.write_dados_gerais()
        # self.write_notificacao_individual()
        # self.write_dados_residencia()
        self.c.save()

        self.merge_sinan()

        return self.save_path


if __name__ == "__main__":
    u = parse(debug)
    w = writer(u)
    w.save()
