import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Caminho do CSV gerado pelos experimentos
csv_path = "resultados/experiment_metrics.csv"
if not os.path.exists(csv_path):
    print(f"Ficheiro {csv_path} não encontrado. Execute primeiro o run_experiments.py!")
    exit(1)

df = pd.read_csv(csv_path)

# Filtra apenas execuções bem-sucedidas (ALLOW e found = True)
df_sucesso = df[(df["status"] == "ALLOW") & (df["found"] == True)]

if df_sucesso.empty:
    print("Aviso: Nenhum dado com status ALLOW e found=True encontrado para plotar.")
    exit(1)

# Configuração de estilo profissional para os gráficos
sns.set_theme(style="whitegrid")
os.makedirs("resultados", exist_ok=True)

# 1. Gráfico de Custo da Solução por Método/Variante
plt.figure(figsize=(12, 6))
sns.barplot(
    data=df_sucesso, x="metodo_variante", y="path_cost", ci=None, palette="viridis"
)
plt.title(
    "Comparação: Custo Médio da Solução por Método e Variante",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Método / Variante", fontsize=12)
plt.ylabel("Custo do Caminho (Path Cost)", fontsize=12)
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("resultados/custo_por_metodo.png", dpi=300)
plt.close()

# 2. Gráfico de Estados Expandidos por Método/Variante
plt.figure(figsize=(12, 6))
sns.barplot(
    data=df_sucesso, x="metodo_variante", y="expanded_nodes", ci=None, palette="magma"
)
plt.title(
    "Comparação: Média de Estados Expandidos por Método e Variante",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Método / Variante", fontsize=12)
plt.ylabel("Estados Expandidos", fontsize=12)
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("resultados/expansoes_por_metodo.png", dpi=300)
plt.close()

# 3. Gráfico Bônus (Recomendado): Tamanho Máximo da Fronteira
plt.figure(figsize=(12, 6))
sns.barplot(
    data=df_sucesso,
    x="metodo_variante",
    y="max_frontier_size",
    ci=None,
    palette="crest",
)
plt.title(
    "Comparação: Tamanho Máximo da Fronteira por Método e Variante",
    fontsize=14,
    fontweight="bold",
)
plt.xlabel("Método / Variante", fontsize=12)
plt.ylabel("Tamanho Máximo da Fronteira", fontsize=12)
plt.xticks(rotation=20)
plt.tight_layout()
plt.savefig("resultados/fronteira_por_metodo.png", dpi=300)
plt.close()

print("Gráficos gerados com sucesso na pasta 'resultados/'!")
print(" - custo_por_metodo.png")
print(" - expansoes_por_metodo.png")
print(" - fronteira_por_metodo.png")
