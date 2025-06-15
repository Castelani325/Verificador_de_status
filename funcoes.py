import os
import datetime
import csv
import send_email

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime

#######################################################################################################

def criar_arquivo_csv(valores, caminho_pasta, max_arquivos=30):
    """Cria um arquivo de texto com os dados da planilha, incrementando um número no nome.

    Args:
        valores: Lista de valores a serem escritos no arquivo.
        caminho_pasta: Caminho completo da pasta onde o arquivo será salvo.
        max_arquivos: Número máximo de arquivos a serem mantidos.
    """

    os.makedirs(caminho_pasta, exist_ok=True)

    # Lista os arquivos existentes na pasta, ordenados por data de modificação
    arquivos_existentes = sorted(
        [f for f in os.listdir(caminho_pasta) if f.startswith("Dados_dia")],
        key=lambda x: os.path.getmtime(os.path.join(caminho_pasta, x)))

    # Se o número de arquivos exceder o limite, remove o mais antigo
    if len(arquivos_existentes) >= max_arquivos:
        arquivo_mais_antigo = os.path.join(caminho_pasta, arquivos_existentes[0])
        os.remove(arquivo_mais_antigo)

    # Gera um nome de arquivo único com data e hora
    data_hora = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    numero_arquivo = len(arquivos_existentes) + 1
    nome_arquivo = f"Dados_dia{numero_arquivo}_{data_hora}.csv"
    caminho_completo = os.path.join(caminho_pasta, nome_arquivo)

    # Cria o arquivo e escreve os dados
    with open(caminho_completo, 'w') as arquivo:
        for linha in valores:
            arquivo.write(','.join(linha) + '\n')

    print(f"Dados salvos em {caminho_completo}")
   
#######################################################################################################
   
def retorna_mais_atual(caminho_pasta):  # retorna o arquivo mais recente de uma pasta
    arquivos = os.listdir(caminho_pasta)
    arquivos_com_data = []
    
    for arquivo in arquivos :
        caminho_completo = os.path.join(caminho_pasta,arquivo)
        timestamp = os.path.getmtime(caminho_completo)
        data_modificacao = datetime.datetime.fromtimestamp(timestamp)
        arquivos_com_data.append((arquivo, data_modificacao))
        
    arquivo_ordenado = sorted(arquivos_com_data, key=lambda x: x[1], reverse = True)
    arquivo_mais_recente = arquivo_ordenado[0]
    
    
    return os.path.join(caminho_pasta, arquivo_mais_recente[0])
    #print(os.path.join(caminho_pasta, arquivo_mais_recente[0]))
   
#######################################################################################################

def comparar_todas_celulas_com_arquivo_e_manda_email(nome_e_pn, valores, caminho_pasta):
    
    # Lê o arquivo CSV
    data_frame = pd.read_csv(retorna_mais_atual(caminho_pasta), encoding='ISO-8859-1',sep=',')
    # Acessa a coluna com o Numeros do pedido
    coluna_numero_csv = data_frame['Número do pedido']

    i=0
    for pedido_csv in coluna_numero_csv :
        for nomes, valor_pedido_google in zip(nome_e_pn,valores) :       
            if str(pedido_csv) == str(valor_pedido_google[0]) :
                
                status = retorna_o_status_do_csv(valor_pedido_google[0], data_frame)
                
                
                print(pedido_csv, valor_pedido_google[0])
                print(status, valor_pedido_google[2] + " " + str(i))
                print(valor_pedido_google[4])
                print(nomes)
                
                if status == valor_pedido_google[2]:
                    print('STATUS IGUAIS')
                    print(f'{i} \n')
                   
                else:
                    print('DIFERENTE')
                    print(f'{i} \n')
                    
                    
                    
                    if status == '-' or status == '' :
                        send_email.enviar_email_pedido_gerado(nomes,valor_pedido_google)
                    elif status != valor_pedido_google[2] :
                        send_email.enviar_email_status(nomes, status, valor_pedido_google)
                i+=1
                  
#######################################################################################################
                
def retorna_o_status_do_csv(numero_pedido, data_frame): #OK
    pedidos = data_frame['Número do pedido']
    status = data_frame["STATUS"]
    for i in range(0, len(pedidos)):
        if pedidos[i] == numero_pedido:
            return status[i]
    return "sem status"

#######################################################################################################

def cria_ou_seleciona_pasta (nome_da_pasta) :  #OK
    
    pasta_atual = os.getcwd() 
    
    caminho_completo = os.path.join(pasta_atual,nome_da_pasta)
    
    if os.path.exists(caminho_completo) : 
        print(f"A pasta '{nome_da_pasta}' já existe")
    else :
        os.makedirs(caminho_completo)
        print(f'A pasta {nome_da_pasta} foi criada')
        
    return caminho_completo
    
#######################################################################################################