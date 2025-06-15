import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from smtplib import SMTP
from email.mime.text import MIMEText

import pandas as pd
import os.path
import send_email
import csv
import datetime
import funcoes
import jax

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.service_account import ServiceAccountCredentials

TF_ENABLE_ONEDNN_OPTS=0
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]    #ok

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "XXXXXXX" #ID da sheet
SAMPLE_RANGE_NAME = "2025!R:V"  #Status na equalização
SAMPLE_RANGE_NAME_01 = "2025!C:H"  #Status na sheet
SAMPLE_RANGE_NAME_02 = "XXXXXXX"  #aba de e-mails

# video https://www.youtube.com/watch?v=l7pL_Y3fw-o

def main():
 
 
  ### Fazendo o login (inicio) ### OK
 
  creds = None

  if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())                                                    #Se der problema de credencial expirada, apenas apague o documento token.json e rode o programa
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          'credentials.json', SCOPES)
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

  ### Fazendo o login (Final) ### OK
  
  
  
  
  try:
    service = build("sheets", "v4", credentials=creds)

    ### Ler informações do sheets (inicio) ###
    sheet = service.spreadsheets()
    result_pedidos = (sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME, majorDimension='ROWS').execute()) #trocar o .get para .update se quiser editar uma célula
    result_nome_e_pn = (sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_01, majorDimension='ROWS').execute()) #trocar o .get para .update se quiser editar uma célula
    # result_efetivo = (sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_02, majorDimension='ROWS').execute()) 
    # result_material = (sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME_03, majorDimension='ROWS').execute()) 
        
    valores = result_pedidos['values']
    #efetivo = result_efetivo['values']
    nome_e_pn = result_nome_e_pn['values']
    
    #print(valores)
    #print(efetivo)
    
    '''for linha in valores[0:]:
      valor_terceira_coluna = linha[2]
      print(valor_terceira_coluna)'''
      
    nome_da_pasta = "Dados_30_dias"
    #caminho_pasta = "D:/OneDrive/Área de Trabalho/Codigos em Python/email_auto/Dados_30_dias/"
    #funcoes.cria_ou_selecio_pasta(nome_da_pasta)
    
    # ### Ler informações do sheets (final) ###
      
    #funcoes.criar_arquivo_csv(valores, caminho_pasta, max_arquivos=31)   
    
    ### compara o .csv com a planilha no google (inicio) ###
    funcoes.comparar_todas_celulas_com_arquivo_e_manda_email(nome_e_pn, valores, funcoes.cria_ou_seleciona_pasta(nome_da_pasta))  # Falta mandar email, se necessário.
    
   
    ### criar um csv com as linhas lidas (inicio) ###
    funcoes.criar_arquivo_csv(valores, funcoes.cria_ou_seleciona_pasta(nome_da_pasta), max_arquivos=31)  
     
    
    ### adicionar/editar uma informação (inicio) ###
    ### adicionar/editar uma informação (final) ###
    
  
  except HttpError as err:
    print(err)


if __name__ == "__main__":
  main()
