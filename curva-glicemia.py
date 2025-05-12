import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.title("Simulador de Curva Glicêmica")

glicemia_inicial = st.number_input("Glicemia inicial (mg/dL)", min_value=50, max_value=400, value=100)

t = np.arange(0, 24*60, 5)
glicemia = np.ones_like(t) * glicemia_inicial

# Inputs das refeições
st.subheader("Refeições")
num_refeicoes = st.number_input("Quantas refeições?", min_value=0, max_value=10, value=3)
refeicoes = []

for i in range(num_refeicoes):
    st.markdown(f"### Refeição {i + 1}")
    hora_refeicao = st.slider(f"Horário da refeição {i + 1} (em horas)", min_value=0.0, max_value=23.5, step=0.5, key=f"hora_refeicao_{i}")
    carbo_em_g = st.number_input(f"Quantidade de carboidratos (em g) da refeição {i+1}", min_value=0, max_value=300, value=50, key=f"carbo_refeicao_{i}")
    refeicoes.append({'hora_refeicao': hora_refeicao, 'carbo_em_g': carbo_em_g})


# Inputs das insulinas
st.subheader("Doses de Insulina")
num_insulinas = st.number_input("Quantas aplicações de insulina?", min_value=0, max_value=10, value=2)
insulinas = []

for i in range(num_refeicoes):
    st.markdown(f"### Insulina {i + 1}")
    hora_insulina = st.slider(f"Horário da aplicação {i+1} da insulina (em horas)", min_value=0.0, max_value=23.5, step=0.5, key=f"hora_insulina_{i}")
    dose = st.number_input(f"Unidades da insulina {i+1}", min_value=0, max_value=50, value=5, key=f"dose_{i}")
    insulinas.append({'hora_insulina': hora_insulina, 'dose':dose})


#Funções para os efeitos
def efeito_refeicao(t, carbo_em_g, hora_refeicao):
    t0 = (hora_refeicao*60) + 45 # Considerando 45 min para a refeição ser de fato absorvida e a glicose cair no sangue
    pico_glicemico = carbo_em_g*3 # Considerando que cada grama de carboidrato aumenta a glicemia em 3 mg/dL
    gaussiana = pico_glicemico * np.exp(-((t - t0)/30)**2)
    return gaussiana

def efeito_insulina(t, unidades, hora_insulina):
    t0 = (hora_insulina*60)
    pico_efeito = unidades*30 # Considerando que cada unidade de insulina reduz 30mg/dL
    gaussiana = -pico_efeito * np.exp(-((t - t0)/60)**2)


# aplicar efeitos
for r in refeicoes:
    glicemia += efeito_refeicao(t, r['carbo_em_g'], r['hora_refeicao'])

for i in insulinas:
    glicemia += efeito_insulina(t, i['dose'], i['hora_insulina'])

st.subheader("Curva simulada de glicemia")
fig, ax = plt.subplots()
ax.plot(t/60, glicemia, label="Glicemia (mg/dL)")
ax.set_xlabel("Tempo (horas)")
ax.set_ylabel("Glicemia (mg/dL)")
ax.set_title("Variação da glicemia ao longo do dia")
ax.grid(True)
st.pyplot(fig)