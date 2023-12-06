from io import StringIO
from pyexpat import model
from pyexpat.errors import messages
import pandas as pd
import openai
from bs4 import BeautifulSoup
import requests
from datetime import datetime

# Configura tu clave de API de OpenAI
openai.api_key = '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'

# Tu código para obtener la tabla con BeautifulSoup
website = 'https://invertaxi-sas.online/informe.php'
result = requests.get(website)
content = result.text
soup = BeautifulSoup(content, 'lxml')
table = soup.find('table')

# print(table)

html_table_string = str(table)

df = pd.read_html(StringIO(html_table_string))[0]

# Convertir la columna 'MOVIL' a tipo numérico solo si contiene valores numéricos
df['MOVIL'] = pd.to_numeric(df['MOVIL'], errors='coerce').astype('Int64')  # Usar 'Int64' para permitir NaN

# Convertir la columna 'PLACA' y 'NOVEDAD' a tipo texto (object)
df['PLACA'] = df['PLACA'].astype(str)
df['NOVEDAD'] = df['NOVEDAD'].astype(str)

by_movil = df.sort_values('MOVIL')
print(by_movil)

# # Realiza consultas al modelo de OpenAI para analizar la columna NOVEDAD
# for index, row in df.iterrows():
#     novedad_texto = row['NOVEDAD']

#     # Realiza una consulta al modelo de OpenAI para obtener análisis de la novedad
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {
#                 "role": "user",
#                 "content": "Contesta 'esto es una prueba'"
#             }
#         ],
#     )

#     # Extrae información relevante de la respuesta de OpenAI si es necesario
#     analisis_novedad = response["choices"][0]

#     # Aquí puedes hacer lo que necesites con el análisis de la novedad, por ejemplo, clasificar T_D y T_N

#     # # Ejemplo: Si el análisis contiene "de 6 am a 6 pm", asigna 'N' a T_D
#     # if "de 6 am a 6 pm" in analisis_novedad:
#     #     df.at[index, 'T_D'] = 'N'

#     # # Ejemplo: Si el análisis contiene "de 6 pm a 12 media noche", asigna 'N' a T_N
#     # if "de 6 pm a 12 media noche" in analisis_novedad:
#     #     df.at[index, 'T_N'] = 'N'
#     print(analisis_novedad)

# # Obtener la fecha actual y formatearla
# fecha_actual = datetime.now().strftime('%d%b%Y')

# # Especifica el nombre del archivo Excel con la fecha actual
# nombre_archivo_excel = f'informe_{fecha_actual}.xlsx'

# # Guarda el DataFrame en un archivo Excel
# df.to_excel(nombre_archivo_excel, index=False)

# print(f"Archivo Excel '{nombre_archivo_excel}' creado exitosamente.")
