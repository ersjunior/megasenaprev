import streamlit as st
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Carregar os dados
@st.cache_data
def load_data():
    file_path = 'dataset/mega_sena_asloterias_ate_concurso_2802.xlsx'  # Atualize para o caminho correto do arquivo
    excel_data = pd.ExcelFile(file_path)
    df = excel_data.parse('sorteios')
    return df

df = load_data()

# Configurar o modelo
def train_model(df):
    features = df[['bola 1', 'bola 2', 'bola 3', 'bola 4', 'bola 5', 'bola 6']].dropna().values

    X = features[:-1]
    y = features[1:]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model, features

model, features = train_model(df)

# Realizar previsões
def generate_predictions(model, features, n_predictions=12):
    last_draw = features[-1].reshape(1, -1)
    predictions = []
    num_sorteio = int(df['Concurso'].max()) + 1

    for i in range(n_predictions):
        next_draw = model.predict(last_draw)
        sorted_draw = np.sort(next_draw.flatten())  # Ordenar os valores das bolas
        predictions.append({'Sorteio': num_sorteio,
                            'bola 1': sorted_draw[0],
                            'bola 2': sorted_draw[1],
                            'bola 3': sorted_draw[2],
                            'bola 4': sorted_draw[3],
                            'bola 5': sorted_draw[4],
                            'bola 6': sorted_draw[5]})
        last_draw = next_draw
        num_sorteio += 1

    return pd.DataFrame(predictions)

# Streamlit Interface
st.title("Previsões da Mega Sena")

st.header("Dados Carregados")
st.write(df.head())

if st.button("Treinar Modelo e Prever Próximos Sorteios"):
    st.write("Treinando o modelo e gerando previsões...")
    forecast_df = generate_predictions(model, features)
    st.subheader("Próximos Sorteios Previstos")
    st.dataframe(forecast_df)

    st.download_button(
        label="Baixar Previsões em CSV",
        data=forecast_df.to_csv(index=False),
        file_name="previsoes_mega_sena.csv",
        mime="text/csv"
    )
