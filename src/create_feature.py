import numpy as np
import pandas as pd
from pathlib import Path


PROCESSED_DIR = Path("data/processed")


def add_features_by_ticker(df_ticker: pd.DataFrame) -> pd.DataFrame:
    """
    Cria features financeiras por ativo.
    """

    df_ticker = df_ticker.sort_values("data_pregao").copy()

    close = df_ticker["preco_fechamento"]
    high = df_ticker["preco_maximo"]
    low = df_ticker["preco_minimo"]

    df_ticker["retorno_1d"] = close.pct_change()

    df_ticker["retorno_7d"] = close.pct_change(7)
    df_ticker["retorno_21d"] = close.pct_change(21)
    df_ticker["retorno_63d"] = close.pct_change(63)
    df_ticker["retorno_126d"] = close.pct_change(126)
    df_ticker["retorno_252d"] = close.pct_change(252)

    df_ticker["volatilidade_21d"] = (
        df_ticker["retorno_1d"].rolling(21).std() * np.sqrt(252)
    )

    df_ticker["volatilidade_63d"] = (
        df_ticker["retorno_1d"].rolling(63).std() * np.sqrt(252)
    )

    df_ticker["volatilidade_126d"] = (
        df_ticker["retorno_1d"].rolling(126).std() * np.sqrt(252)
    )

    df_ticker["volume_medio_21d"] = (
        df_ticker["volume_negociado"].rolling(21).mean()
    )

    df_ticker["volume_medio_63d"] = (
        df_ticker["volume_negociado"].rolling(63).mean()
    )

    df_ticker["negocios_medio_21d"] = (
        df_ticker["numero_negocios"].rolling(21).mean()
    )

    df_ticker["amplitude_intradiaria"] = (high - low) / close

    df_ticker["amplitude_media_21d"] = (
        df_ticker["amplitude_intradiaria"].rolling(21).mean()
    )

    rolling_max_252 = close.rolling(252).max()

    df_ticker["drawdown_252d"] = (close / rolling_max_252) - 1

    df_ticker["distancia_maxima_252d"] = (close / rolling_max_252) - 1

    df_ticker["sharpe_aprox_63d"] = (
        df_ticker["retorno_63d"] / df_ticker["volatilidade_63d"]
    )

    df_ticker["retorno_futuro_60d"] = close.shift(-60) / close - 1

    return df_ticker


def main():
    input_path = PROCESSED_DIR / "b3_universo_modelagem.parquet"
    output_path = PROCESSED_DIR / "b3_features.parquet"

    print("[INFO] Lendo universo de modelagem...")
    df = pd.read_parquet(input_path)

    print("[INFO] Shape inicial:", df.shape)
    print("[INFO] Colunas:", df.columns.tolist())

    if df.empty:
        raise ValueError(
            "A base b3_universo_modelagem.parquet está vazia. "
            "Rode novamente o create_universe.py e confira se os tickers foram encontrados."
        )

    if "ticker" not in df.columns:
        raise ValueError(
            "A coluna 'ticker' não existe na base. "
            "O problema está no create_universe.py ou no parse_b3.py."
        )

    df["ticker"] = df["ticker"].astype(str).str.strip()

    print("\n[INFO] Tickers encontrados:")
    print(sorted(df["ticker"].unique()))

    if "BOVA11" not in df["ticker"].unique():
        raise ValueError(
            "BOVA11 não foi encontrado na base. "
            "Ele é necessário porque será usado como benchmark."
        )

    dataframes = []

    for ticker, df_ticker in df.groupby("ticker"):
        print(f"[FEATURES] Processando {ticker}...")
        df_temp = add_features_by_ticker(df_ticker)
        dataframes.append(df_temp)

    df_features = pd.concat(dataframes, ignore_index=True)

    print("[INFO] Shape após features:", df_features.shape)
    print("[INFO] Colunas após features:", df_features.columns.tolist())

    benchmark = df_features[df_features["ticker"] == "BOVA11"][
        ["data_pregao", "retorno_futuro_60d", "retorno_1d"]
    ].rename(
        columns={
            "retorno_futuro_60d": "retorno_futuro_60d_benchmark",
            "retorno_1d": "retorno_1d_benchmark",
        }
    )

    df_features = df_features.merge(
        benchmark,
        on="data_pregao",
        how="left",
    )

    df_features["target_supera_benchmark_60d"] = (
        df_features["retorno_futuro_60d"]
        > df_features["retorno_futuro_60d_benchmark"]
    ).astype(int)

    df_model = df_features[
        ~df_features["ticker"].isin(["BOVA11", "SMAL11"])
    ].copy()

    feature_cols = [
        "retorno_7d",
        "retorno_21d",
        "retorno_63d",
        "retorno_126d",
        "retorno_252d",
        "volatilidade_21d",
        "volatilidade_63d",
        "volatilidade_126d",
        "volume_medio_21d",
        "volume_medio_63d",
        "negocios_medio_21d",
        "amplitude_media_21d",
        "drawdown_252d",
        "distancia_maxima_252d",
        "sharpe_aprox_63d",
        "retorno_futuro_60d_benchmark",
        "retorno_1d_benchmark",
    ]

    df_model = df_model.dropna(
        subset=feature_cols + ["target_supera_benchmark_60d"]
    ).copy()

    if df_model.empty:
        raise ValueError(
            "Depois de criar features e remover nulos, a base final ficou vazia. "
            "Pode faltar histórico suficiente ou os tickers têm poucos dados."
        )

   # Salva em Parquet
    df_model.to_parquet(output_path, index=False)

    # Salva também em CSV para facilitar leitura no notebook
    csv_output_path = PROCESSED_DIR / "b3_features.csv"
    df_model.to_csv(csv_output_path, index=False)

    print(f"\n[OK] Features salvas em: {output_path}")
    print(f"[OK] Features salvas também em: {csv_output_path}")
    print("[INFO] Shape final:", df_model.shape)

    print("\n[INFO] Distribuição do target:")
    print(df_model["target_supera_benchmark_60d"].value_counts())
    print(df_model["target_supera_benchmark_60d"].value_counts(normalize=True))

    print("\n[INFO] Amostra:")
    print(
        df_model[
            [
                "data_pregao",
                "ticker",
                "retorno_21d",
                "volatilidade_21d",
                "retorno_futuro_60d",
                "retorno_futuro_60d_benchmark",
                "target_supera_benchmark_60d",
            ]
        ].head()
    )


if __name__ == "__main__":
    main()