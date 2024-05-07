#!/usr/bin/env python3
#!/usr/bin/env python3
from datetime import date


class usuario:
    # === Dados Gerais ============================
    data: str = "09/06/2022"
    uf: str = "SP"
    municipio: str = "São Paulo"
    ibge: str = "3550308"
    ubs: str = "UBS Alto de Umuarama"
    ubs_code: str = "2786745"
    # === Notificação Individual ==================
    nome: str = ""  # "João da Silva"
    cpf: str = ""  # "12345678901"
    nascimento: str = ""  # "01/01/1980"
    sexo: str = ""  # "Masculino"
    gestante: str = ""  # "Não"
    raca: str = ""  # "Parda"
    escolaridade: str = ""  # "Ensino Médio"
    n_sus: str = ""  # "123456789012345"
    nome_mae: str = ""  # "Maria da Silva"
    # === Dados residenciais ======================
    uf_residencia: str = ""  # "SP"
    municipio_residencia: str = ""  # "São Paulo"
    ibge_residencia: str = ""  # "3550308"
    distrito_residencia: str = ""  # "São Paulo"
    bairro_residencia: str = ""  # "Alto de Umuarama"
    logradouro_residencia: str = ""  # "Rua da Saúde"
    cod_logradouro_residencia: str = ""  # "123456"
    numero_residencia: str = ""  # "123"
    complemento_residencia: str = ""  # "Apto 123"
    cep_residencia: str = ""  # "12345678"
    telefone_residencia: str = ""  # "111122334455"
    zona_residencia: str = "Urbana"

    def __str__(self):
        s = ""
        # para cada atributo
        for key, value in vars(self).items():
            s += f"{key}: {value}\n"
        return s


def get_sigla(estado: str) -> str:
    estados = {
        "Acre": "AC",
        "Alagoas": "AL",
        "Amapá": "AP",
        "Amazonas": "AM",
        "Bahia": "BA",
        "Ceará": "CE",
        "Distrito Federal": "DF",
        "Espírito Santo": "ES",
        "Goiás": "GO",
        "Maranhão": "MA",
        "Mato Grosso": "MT",
        "Mato Grosso do Sul": "MS",
        "Minas Gerais": "MG",
        "Pará": "PA",
        "Paraíba": "PB",
        "Paraná": "PR",
        "Pernambuco": "PE",
        "Piauí": "PI",
        "Rio de Janeiro": "RJ",
        "Rio Grande do Norte": "RN",
        "Rio Grande do Sul": "RS",
        "Rondônia": "RO",
        "Roraima": "RR",
        "Santa Catarina": "SC",
        "São Paulo": "SP",
        "Sergipe": "SE",
        "Tocantins": "TO",
    }
    return estados.get(estado, "SP")


def get_ibge(municipio: str, uf: str) -> str:
    if municipio == "São Paulo" and uf == "SP":
        return "3550308"
    return ""


def parse(entrada: str = debug) -> usuario:
    u = usuario()
    linhas = entrada.split("\n")

    # Dados Gerais
    u.data = date.today().strftime("%d/%m/%Y")

    # para cada linha na entrada:
    for i in range(len(linhas)):
        if "Visualização do cidadão" in linhas[i - 1]:
            u.nome = linhas[i].split(" | ")[0].strip()
            u.sexo = linhas[i].split(" | ")[1].strip()
        if "Nasceu em" in linhas[i]:
            u.nascimento = linhas[i].split("Nasceu em ")[1]
        if "Telefone(" in linhas[i]:
            u.telefone_residencia = (
                linhas[i]
                .split("Telefone")[1]
                .replace("(", "")
                .replace(")", "")
                .replace("-", "")
                .replace(" ", "")
                .strip()
            )
        if "CPF" in linhas[i - 1]:
            u.cpf = linhas[i].replace(".", "").replace("-", "").strip()
        if "CNS" in linhas[i - 1]:
            u.n_sus = linhas[i].replace(".", "").replace("-", "").strip()
        if "Nome da mãe" in linhas[i - 1]:
            u.nome_mae = linhas[i].strip()
        if "Raça/cor" in linhas[i - 1]:
            print("Achei a raça", linhas[i].strip())
            u.raca = linhas[i].strip()
        if "CEP" in linhas[i - 1]:
            u.cep_residencia = linhas[i].replace("-", "").strip()
        if "Estado" in linhas[i - 1]:
            u.uf_residencia = get_sigla(linhas[i].strip())
        if "Município" in linhas[i - 1]:
            u.municipio_residencia = linhas[i].strip()
            u.ibge_residencia = get_ibge(u.municipio_residencia, u.uf_residencia)
        if "Bairro" in linhas[i - 1]:
            u.bairro_residencia = linhas[i].strip()
        if "Tipo de logradouro" in linhas[i - 1]:
            u.logradouro_residencia = linhas[i].strip()
        if "Logradouro" in linhas[i - 1]:
            u.logradouro_residencia += " " + linhas[i].strip()
        if "Número" in linhas[i - 1]:
            u.numero_residencia = linhas[i].strip()
        if "Complemento" in linhas[i - 1]:
            u.complemento_residencia = (
                linhas[i].strip() if linhas[i].strip() != "na" else ""
            )
        if "Escolaridade" in linhas[i - 1]:
            u.escolaridade = linhas[i].strip()

    return u


if __name__ == "__main__":
    u = parse(debug)
    print(u)
