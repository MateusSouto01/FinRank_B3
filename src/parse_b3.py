import pandas as pd
from pathlib import Path


RAW_DIR = Path("data/raw/b3")
PROCESSED_DIR = Path("data/processed")
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


COLUMNS_SPECS = [
    (0, 2),      # tipo_registro
    (2, 10),     # data_pregao
    (10, 12),    # cod_bdi
    (12, 24),    # ticker
    (24, 27),    # tipo_mercado
    (27, 39),    # nome_empresa
    (39, 49),    # especificacao
    (49, 52),    # prazo_termo
    (52, 56),    # moeda
    (56, 69),    # preco_abertura
    (69, 82),    # preco_maximo
    (82, 95),    # preco_minimo
    (95, 108),   # preco_medio
    (108, 121),  # preco_fechamento
    (121, 134),  # melhor_oferta_compra
    (134, 147),  # melhor_oferta_venda
    (147, 152),  # numero_negocios
    (152, 170),  # quantidade_negociada
    (170, 188),  # volume_negociado
    (188, 201),  # preco_exercicio
    (201, 202),  # indicador_correcao
    (202, 210),  # data_vencimento
    (210, 217),  # fator_cotacao
    (217, 230),  # preco_exercicio_pontos
    (230, 242),  # codigo_isi
    (242, 245),  # numero_distribuicao
]

COLUMN_NAMES = [
    "tipo_registro",
    "data_pregao",
    "cod_bdi",
    "ticker",
    "tipo_mercado",
    "nome_empresa",
    "especificacao",
    "prazo_termo",
    "moeda",
    "preco_abertura",
    "preco_maximo",
    "preco_minimo",
    "preco_medio",
    "preco_fechamento",
    "melhor_oferta_compra",
    "melhor_oferta_venda",
    "numero_negocios",
    "quantidade_negociada",
    "volume_negociado",
    "preco_exercicio",
    "indicador_correcao",
    "data_vencimento",
    "fator_cotacao",
    "preco_exercicio_pontos",
    "codigo_isi",
    "numero_distribuicao",
]


PRICE_COLUMNS = [
    "preco_abertura",
    "preco_maximo",
    "preco_minimo",
    "preco_medio",
    "preco_fechamento",
    "melhor_oferta_compra",
    "melhor_oferta_venda",
    "preco_exercicio",
    "preco_exercicio_pontos",
]

INTEGER_COLUMNS = [
    "numero_negocios",
    "quantidade_negociada",
    "volume_negociado",
]


def parse_cotahist_file(file_path: Path) -> pd.DataFrame:
    """
    Lê um arquivo COTAHIST da B3 em largura fixa.
    """

    df = pd.read_fwf(
        file_path,
        colspecs=COLUMNS_SPECS,
        names=COLUMN_NAMES,
        dtype=str,
        encoding="latin1",
    )

    # Mantém apenas registros de negociação.
    df = df[df["tipo_registro"] == "01"].copy()

    # Limpeza textual.
    text_columns = [
        "ticker",
        "nome_empresa",
        "especificacao",
        "moeda",
        "cod_bdi",
        "tipo_mercado",
    ]

    for col in text_columns:
        df[col] = df[col].str.strip()

    # Converte data.
    df["data_pregao"] = pd.to_datetime(df["data_pregao"], format="%Y%m%d")

    # Converte preços. A B3 armazena preços multiplicados por 100.
    for col in PRICE_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce") / 100

    # Converte inteiros.
    for col in INTEGER_COLUMNS:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def main():
    files = sorted(RAW_DIR.glob("COTAHIST_A*.TXT"))

    if not files:
        raise FileNotFoundError(
            "Nenhum arquivo COTAHIST_A*.TXT encontrado em data/raw/b3. "
            "Rode primeiro src/download_b3.py."
        )

    dataframes = []

    for file_path in files:
        print(f"[PROCESSANDO] {file_path}")
        df_year = parse_cotahist_file(file_path)
        dataframes.append(df_year)

    df = pd.concat(dataframes, ignore_index=True)

    # Mercado à vista.
    df = df[df["tipo_mercado"] == "010"].copy()

    # Salva base processada inicial.
    output_path = PROCESSED_DIR / "b3_cotacoes_mercado_vista.parquet"
    df.to_parquet(output_path, index=False)

    print(f"[OK] Base salva em: {output_path}")
    print(df.shape)
    print(df.head())


if __name__ == "__main__":
    main()