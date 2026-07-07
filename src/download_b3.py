import os
import zipfile
import requests
from pathlib import Path


RAW_DIR = Path("data/raw/b3")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def download_b3_cotahist(year: int) -> Path:
    """
    Baixa o arquivo anual COTAHIST da B3.

    Fonte:
    https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{year}.ZIP
    """
    url = f"https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{year}.ZIP"
    zip_path = RAW_DIR / f"COTAHIST_A{year}.ZIP"

    if zip_path.exists():
        print(f"[OK] Arquivo já existe: {zip_path}")
        return zip_path

    print(f"[DOWNLOAD] Baixando {url}")

    response = requests.get(url, timeout=60)

    if response.status_code != 200:
        raise Exception(
            f"Erro ao baixar {year}. "
            f"Status code: {response.status_code}. URL: {url}"
        )

    with open(zip_path, "wb") as file:
        file.write(response.content)

    print(f"[OK] Salvo em: {zip_path}")
    return zip_path


def extract_zip(zip_path: Path) -> None:
    """
    Extrai o ZIP da B3 para a pasta raw.
    """
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(RAW_DIR)

    print(f"[OK] Extraído: {zip_path.name}")


def main():
    years = list(range(2018, 2026))

    for year in years:
        try:
            zip_path = download_b3_cotahist(year)
            extract_zip(zip_path)
        except Exception as error:
            print(f"[ERRO] Ano {year}: {error}")


if __name__ == "__main__":
    main()