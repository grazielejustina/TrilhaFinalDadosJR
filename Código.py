import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregando os arquivos CSVs
feedback_junho = pd.read_csv("C:\\Users\\grazi\\Documents\\Nova pasta\\feedback_junho2024.csv")
feedback_julho = pd.read_csv("C:\\Users\\grazi\\Documents\\Nova pasta\\feedback_julho2024.csv")

# Exibindo as primeiras linhas de cada arquivo para entender os dados
print(feedback_junho.head())
print(feedback_julho.head())

# Combinando os dois arquivos em um único DataFrame para análise conjunta
feedback_combined = pd.concat([feedback_junho, feedback_julho], ignore_index=True)

# Removendo espaços em branco de todas as colunas do tipo 'object' (strings)
feedback_combined = feedback_combined.apply(lambda x: x.str.strip() if x.dtype == "object" else x)

# Convertendo colunas relevantes para o tipo categórico
categorical_columns = [
    "atualmente_sou", "minha_equipe", "reunioes_do_time", "colaboracao_entre_membros",
    "ambiente_de_aprendizagem", "comunicacao_entre_membros", "satisfacao_geral_comunidade", "feedbacks"
]

for col in categorical_columns:
    if col in feedback_combined.columns:
        feedback_combined[col] = feedback_combined[col].astype('category')

# Convertendo a coluna 'horas_semanais_dedicadas' para numérico, substituindo valores inválidos por NaN
feedback_combined['horas_semanais_dedicadas'] = pd.to_numeric(feedback_combined['horas_semanais_dedicadas'], errors='coerce')

# Convertendo colunas de data para o formato datetime, se existirem
if 'data' in feedback_combined.columns:
    feedback_combined['data'] = pd.to_datetime(feedback_combined['data'], errors='coerce')

# Removendo linhas com valores NaN para a coluna de interesse
feedback_combined = feedback_combined.dropna(subset=['horas_semanais_dedicadas'])

# Estatísticas descritivas para variáveis numéricas
numerical_summary = feedback_combined.describe()

# Contagem de valores para cada variável categórica
categorical_summary = feedback_combined[categorical_columns].describe(include='category')

print(numerical_summary)
print(categorical_summary)

# Configuração inicial para o estilo dos gráficos
plt.figure(figsize=(15, 10))

# Gráfico 1: Distribuição das Horas Semanais Dedicadas
plt.subplot(2, 2, 1)
sns.histplot(feedback_combined['horas_semanais_dedicadas'], bins=10, color='skyblue', kde=True)
plt.title('Distribuição de Horas Semanais Dedicadas')
plt.xlabel('Horas Semanais Dedicadas')
plt.ylabel('Contagem')

# Gráfico 2: Contagem de Respostas - Reuniões do Time
plt.subplot(2, 2, 2)
sns.countplot(x='reunioes_do_time', data=feedback_combined, hue='reunioes_do_time', palette='pastel', legend=False)
plt.title('Satisfação com as Reuniões do Time')
plt.xlabel('Reuniões do Time')
plt.ylabel('Contagem')

# Gráfico 3: Contagem de Respostas - Colaboração entre Membros
plt.subplot(2, 2, 3)
sns.countplot(x='colaboracao_entre_membros', data=feedback_combined, hue='colaboracao_entre_membros', palette='viridis', legend=False)
plt.title('Satisfação com a Colaboração entre Membros')
plt.xlabel('Colaboração entre Membros')
plt.ylabel('Contagem')

# Gráfico 4: Satisfação Geral com a Comunidade
plt.subplot(2, 2, 4)
sns.countplot(x='satisfacao_geral_comunidade', data=feedback_combined, hue='satisfacao_geral_comunidade', palette='coolwarm', legend=False)
plt.title('Satisfação Geral com a Comunidade')
plt.xlabel('Satisfação Geral')
plt.ylabel('Contagem')

plt.tight_layout()
plt.show()

plt.figure(figsize=(15, 10))

# Gráfico 5 (Atualizado): Gráfico de Barras - Satisfação Geral e Horas Semanais Dedicadas
plt.subplot(2, 2, 1)
sns.barplot(x='satisfacao_geral_comunidade', y='horas_semanais_dedicadas', hue='satisfacao_geral_comunidade', data=feedback_combined, palette='muted', dodge=False)
plt.title('Média de Horas Semanais por Satisfação Geral')
plt.xlabel('Satisfação Geral')
plt.ylabel('Média de Horas Semanais')
plt.legend([],[], frameon=False)  # Removendo a legenda

# Gráfico 6 (Corrigido): Gráfico de Barras Empilhadas - Satisfação Geral por Mês
# Adicionando coluna de mês
feedback_combined['mes'] = ['Junho' if i < len(feedback_junho) else 'Julho' for i in feedback_combined.index]
satisfaction_by_month = feedback_combined.groupby(['mes', 'satisfacao_geral_comunidade'], observed=False).size().unstack(fill_value=0)

plt.subplot(2, 2, 2)
satisfaction_by_month.plot(kind='bar', stacked=True, color=['lightcoral', 'skyblue'], ax=plt.gca())
plt.title('Satisfação Geral com a Comunidade por Mês')
plt.xlabel('Mês')
plt.ylabel('Contagem')

# Gráfico 7: Heatmap - Correlação entre Variáveis Numéricas
plt.subplot(2, 2, 3)
# Filtrando apenas as colunas numéricas para o heatmap
numerical_data = feedback_combined.select_dtypes(include='number')
sns.heatmap(numerical_data.corr(), annot=True, cmap='coolwarm', center=0)
plt.title('Mapa de Calor das Correlações')

plt.tight_layout()
plt.show()

# Cálculo da Taxa de Satisfação Geral
satisfied_conditions = ['satisfeito', 'muito satisfeito']
total_responses = len(feedback_combined)
satisfied_responses = feedback_combined['satisfacao_geral_comunidade'].isin(satisfied_conditions).sum()
satisfaction_rate = (satisfied_responses / total_responses) * 100

# Cálculo da Taxa de Engajamento
engaged_members = feedback_combined[feedback_combined['horas_semanais_dedicadas'] > 5].shape[0]
engagement_rate = (engaged_members / total_responses) * 100

print(f'Taxa de Satisfação: {satisfaction_rate:.2f}%')
print(f'Taxa de Engajamento: {engagement_rate:.2f}%')