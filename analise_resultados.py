
import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = "resultados_experimentos.csv"

try:
    df = pd.read_csv(CSV_PATH, encoding="utf-8")
except FileNotFoundError:
    data = [
        {
            "cenário": "Prompt Seguro",
            "taxa_detecção": 1.0,
            "falsos_positivos": 1.0,
            "latência_média_ms": 13.28,
            "throughput_req_por_segundo": 75.28,
        },
        {
            "cenário": "Prompt Injection 1",
            "taxa_detecção": 1.0,
            "falsos_positivos": 0.0,
            "latência_média_ms": 8.73,
            "throughput_req_por_segundo": 114.6,
        },
        {
            "cenário": "Prompt Injection 2",
            "taxa_detecção": 1.0,
            "falsos_positivos": 0.0,
            "latência_média_ms": 8.56,
            "throughput_req_por_segundo": 116.76,
        },
        {
            "cenário": "Prompt Longo Demais",
            "taxa_detecção": 1.0,
            "falsos_positivos": 0.0,
            "latência_média_ms": 8.97,
            "throughput_req_por_segundo": 111.46,
        },
    ]
    df = pd.DataFrame(data)

print("✅ Dados carregados:")
print(df)

def plot_metric(df, column, ylabel, title, filename):
    plt.figure()
    plt.bar(df["cenário"], df[column])
    plt.xlabel("Cenário")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()
    print(f"📊 Gráfico salvo: {filename}")


plot_metric(
    df,
    "taxa_detecção",
    "Taxa de detecção",
    "Taxa de detecção por cenário",
    "grafico_taxa_detec.png",
)

plot_metric(
    df,
    "falsos_positivos",
    "Falsos positivos (proporção)",
    "Taxa de falsos positivos por cenário",
    "grafico_falsos_positivos.png",
)

plot_metric(
    df,
    "latência_média_ms",
    "Latência média (ms)",
    "Latência média por cenário",
    "grafico_latencia.png",
)

plot_metric(
    df,
    "throughput_req_por_segundo",
    "Req/s",
    "Throughput por cenário",
    "grafico_throughput.png",
)

OUTPUT_XLSX = "analise_resultados.xlsx"

with pd.ExcelWriter(OUTPUT_XLSX, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="dados_brutos", index=False)

    metrics_cols = [
        "taxa_detecção",
        "falsos_positivos",
        "latência_média_ms",
        "throughput_req_por_segundo",
    ]
    resumo = pd.DataFrame(
        {
            "métrica": metrics_cols,
            "mínimo": [df[c].min() for c in metrics_cols],
            "máximo": [df[c].max() for c in metrics_cols],
            "média": [df[c].mean() for c in metrics_cols],
        }
    )
    resumo.to_excel(writer, sheet_name="resumo_estatistico", index=False)

    workbook = writer.book
    worksheet_graficos = workbook.add_worksheet("graficos")

    worksheet_graficos.write("B2", "Gráfico: Taxa de detecção")
    worksheet_graficos.insert_image("B3", "grafico_taxa_detec.png")

    worksheet_graficos.write("B20", "Gráfico: Falsos positivos")
    worksheet_graficos.insert_image("B21", "grafico_falsos_positivos.png")

    worksheet_graficos.write("M2", "Gráfico: Latência média (ms)")
    worksheet_graficos.insert_image("M3", "grafico_latencia.png")

    worksheet_graficos.write("M20", "Gráfico: Throughput (req/s)")
    worksheet_graficos.insert_image("M21", "grafico_throughput.png")

print(f"✅ Arquivo Excel gerado: {OUTPUT_XLSX}")
print("Pronto! Use esse XLS no relatório e na apresentação.")
