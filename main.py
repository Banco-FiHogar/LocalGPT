

prompt = """
[INST] [INST] pin pesos [/INST] I understand that you are an agent of customer service for RESET, the first 100% digital bank in the Dominican Republic. You are going to read the customer service manual to know how to interact with them. If you are unsure of what the customer wants, you should ask them questions to clarify. Remember that the customer's questions are because they trust you and expect you to have answers about their money. Here are some questions with their correct answers:
* TRANSFERENCIA DE DINERO. Respuesta: Con tu cuenta puedes enviar y recibir dinero de cualquier banco nacional de forma inmediata y sin costo adicional.
* RECARGA DE DINERO. Respuesta: Para depositar o cargar balance a tu cuenta Reset, puedes hacerlo a través de transferencias bancarias o depósitos en efectivo en nuestra red de comercios aliados.
* RECARGA DE CUENTA. Respuesta: Para depositar o cargar balance a tu cuenta Reset, puedes hacerlo a través de transferencias bancarias o depósitos en efectivo en nuestra red de comercios aliados.
[INST] Ahora eres un agente de servicio al cliente en RESET, la primera banca 100% digital de la Republica Dominicana. Lo que vas a leer ahora es el manual de servicio al cliente para que sepas como interactuar con ellos. Si te pregunta algo de lo que no tienes información sobre como responder responde \"Permítenos unos minutos para poder atenderte\". Si te preguntan de borrar la cuenta responde \"Tener tu cuenta Reset no te cuesta $0 y es totalmente GRATIS, puedes dejarla abierta, sin saldo y no pasa nada, ¿aun así quieres continuar para cancelarla? Para cancelar tu cuenta Reset debes enviar un correo a ayuda@reset.do con los siguientes datos: un selfie con tu cédula en mano número de celular registrado en Reset razón de cancelación Una vez enviado el correo, te estarán contactando de nuestro equipo para validar las informaciones y proceder a cancelar la cuenta. Te recordamos que la cuenta debe estar sin saldo al momento de la cancelación.
"""


import streamlit as st
import requests

# Function to handle sending requests to the GPT model with detailed prompt engineering
def send_request(user_input):
    endpoint = 'https://api.together.xyz/v1/chat/completions'
    payload = {
        "model": "codellama/CodeLlama-34b-Instruct-hf",
        "max_tokens": 512,
        "prompt": (prompt + user_input + " [/INST]"),
        "temperature": 0,
        "top_p": 0,
        "top_k": 50,
        "repetition_penalty": 1,
        "stop": ["</s>", "[INST]"],
        "job": "851469ba4afe1290-CLT"
    }
    headers = {
        "Authorization": "Bearer 4c4785ef91a79f55e3eed8a13df8447695c2c64dd2a3c9994fe704bb25d1d5d2"
    }
    response = requests.post(endpoint, json=payload, headers=headers)
    response_json = response.json()
    return response_json

# Streamlit UI
st.title('RESET Modelo Local')
user_input = st.text_area("Type your customer service query here:")

if st.button('Send'):  # Adding a button to send the user input
    response = send_request(user_input)
    if response and 'choices' in response and len(response['choices']) > 0 and 'message' in response['choices'][0]:
        # Adjusting to access 'content' within 'message'
        st.write(response['choices'][0]['message']['content'])
    else:
        st.error("An error occurred. Please try again.")
