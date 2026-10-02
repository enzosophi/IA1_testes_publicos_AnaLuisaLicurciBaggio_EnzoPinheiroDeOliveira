import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carrega os dados gerados
df = pd.read_csv("resultados/experiment_metrics.csv")
df_sucesso = df[df["found"] == True]

sns.set_theme(style="whitegrid")

# Gráfico 1: Custo da solução por algoritmo
plt.figure(figsize=(10, 6))
sns.barplot(data=df_sucesso, x="algoritmo", y="path_cost", ci=None, palette="viridis")
plt.title("Custo Médio da Solução por Método de Busca")
plt.xlabel("Algoritmo")
plt.ylabel("Custo do Caminho")
plt.savefig("resultados/custo_por_metodo.png")
plt.close()

# Gráfico 2: Estados expandidos por algoritmo
plt.figure(figsize=(10, 6))
sns.barplot(
    data=df_sucesso, x="algoritmo", y="expanded_nodes", ci=None, palette="magma"
)
plt.title("Média de Estados Expandidos por Método de Busca")
plt.xlabel("Algoritmo")
plt.ylabel("Estados Expandidos")
plt.savefig("resultados/expansoes_por_metodo.png")
plt.close()

print("Gráficos gerados e salvos na pasta resultados/ com sucesso!")
