import pandas as pd
from pathlib import Path


PROCESSED_DIR = Path("data/processed")


# Universo inicial: ações líquidas + ETFs úteis como benchmark/mercado.
TICKERS_UNIVERSE = [
    # Benchmark / ETFs
    "BOVA11", "SMAL11",

    # Bancos / financeiro
    "ITUB4", "BBDC4", "BBAS3", "SANB11", "BPAC11", "B3SA3",

    # Commodities / energia
    "PETR3", "PETR4", "VALE3", "PRIO3", "GGBR4", "CSNA3", "SUZB3", "KLBN11",

    # Elétricas / saneamento
    "ELET3", "ELET6", "EQTL3", "TAEE11", "CPFE3", "SBSP3",

    # Consumo / varejo / saúde
    "ABEV3", "RENT3", "RADL3", "LREN3", "MGLU3", "VIVA3", "HAPV3",

    # Telecom / infraestrutura / transportes
    "VIVT3", "TIMS3", "RAIL3", "CCRO3", "WEGE3",

    # Alimentos / indústria
    "JBSS3", "BRFS3", "UGPA3",
]


def main():
    input_path = PROCESSED_DIR / "b3_cotacoes_mercado_vista.parquet"
    output_path = PROCESSED_DIR / "b3_universo_modelagem.parquet"

    print("[INFO] Lendo base processada da B3...")
    df = pd.read_parquet(input_path)

    print("[INFO] Shape original:", df.shape)

    # Garantia de formato.
    df["ticker"] = df["ticker"].astype(str).str.strip()

    # Filtra universo de ativos.
    df = df[df["ticker"].isin(TICKERS_UNIVERSE)].copy()

    print("[INFO] Shape após filtro de tickers:", df.shape)

    # Mantém colunas principais.
    cols = [
        "data_pregao",
        "ticker",
        "cod_bdi",
        "tipo_mercado",
        "nome_empresa",
        "especificacao",
        "preco_abertura",
        "preco_maximo",
        "preco_minimo",
        "preco_medio",
        "preco_fechamento",
        "numero_negocios",
        "quantidade_negociada",
        "volume_negociado",
    ]

    df = df[cols].copy()

    # Remove possíveis duplicidades por segurança.
    df = df.drop_duplicates(subset=["data_pregao", "ticker"])

    # Ordena base.
    df = df.sort_values(["ticker", "data_pregao"]).reset_index(drop=True)

    # Salva.
    df.to_parquet(output_path, index=False)

    print(f"[OK] Base filtrada salva em: {output_path}")
    print("[INFO] Shape final:", df.shape)

    print("\n[INFO] Quantidade de registros por ticker:")
    print(df["ticker"].value_counts().sort_index())

    print("\n[INFO] Período da base:")
    print(df["data_pregao"].min(), "até", df["data_pregao"].max())


if __name__ == "__main__":
    main()