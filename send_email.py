import smtplib
import email.mime.text

#Envio de email quando o formulário for preenchido.

# def enviar_email_solicitacao(pessoa, pn) :
#     corpo_do_email =f"""
#     Olá, {pessoa}. 
     
#     A sua solicitação de pedido de PN {pn} foi recebida com sucesso.
#     Logo será gerado o seu número de pedido.
     
     
#     Todas as caracteristicas do seu pedido podem sem visualizadas na planilha do seguinte link :
#     XXXXXXX
    
#     Caso precise solicitar algum material, segue o link do formulário de solicitação :
#     XXXXXXX
     
#     Respeitosamente, Provedoria.
#     """
    
#     msg = email.message.Message()
#     msg['Subject'] = "Solicitação Recebida." 
#     msg['From'] = 'XXXXXXX'
#     msg['To'] = "XXXXXXX"  #Testenado com o meu email mesmo
    
#     password = 'XXXXXXX'
    
#     #Configurações de comunicação 
#     msg.add_header('Content_Type', 'text/html')
#     msg.set_payload(corpo_do_email)
#     s = smtplib.SMTP('smtp.gmail.com: 587')
#     s.starttls()
    
#     #credenciais de login
#     s.login(msg['From'],password)
#     s.sendmail(msg['From'],[msg['To']], msg.as_string().encode('utf-8'))
#     print('Email enviado com sucesso.')   
    

##################################################################################

# Envio de email quando o numero de pedido for gerado

def enviar_email_pedido_gerado(nome, valor_pedido_google) :
    corpo_do_email =f"""
    Olá, {nome[0]}. 
     
    O seu pedido foi gerado com o número {valor_pedido_google[0]} e consta com o Status  "{valor_pedido_google[2]}".
    
    PN : {nome[3]}
    Nomenclatura : {nome[4]}
    Quantidade : {nome[5]} 
     
    Todas as caracteristicas do seu pedido podem sem visualizadas na planilha do seguinte link :
    XXXXXXX
    
    Caso precise solicitar algum material, segue o link do formulário de solicitação :
    XXXXXXX
     
    Respeitosamente, XXXXXXX.
    """
    
    msg = email.message.Message()
    msg['Subject'] = "Pedido Gerado" 
    msg['From'] = 'XXXXXXX'
    msg['To'] = f'{valor_pedido_google[4]}' 
    
    password = 'upjwvfsbozuyejca'
    
    #Configurações de comunicação 
    msg.add_header('Content_Type', 'text/html')
    msg.set_payload(corpo_do_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    
    #credenciais de login
    s.login(msg['From'],password)
    s.sendmail(msg['From'],[msg['To']], msg.as_string().encode('utf-8'))
    print('(Geração de Pedido)Email enviado com sucesso.') 
    
    
##################################################################################
    
    # Envio de email quando houver alguma ataulização de status.
    
def enviar_email_status (nome, status_csv, valor_pedido_google) :
    corpo_do_email =f"""
    Olá, {nome[0]}. 
     
    O seu pedido de número {valor_pedido_google[0]} teve uma atualização e consta com o Status de {valor_pedido_google[2]}.
        
    PN : {nome[3]}
    Nomenclatura : {nome[4]}
    Quantidade : {nome[5]}
    Status anterior : {status_csv}
     
     
    Todas as caracteristicas do seu pedido podem ser visualizadas na planilha do seguinte link :
    XXXXXXX
    
    Caso precise solicitar algum material, segue o link do formulário de solicitação :
    XXXXXXX
     
    Respeitosamente, XXXXXXX.
    """
    
    msg = email.message.Message()
    msg['Subject'] = "Atualização de Status." 
    msg['From'] = 'XXXXXXX'
    msg['To'] = f"{valor_pedido_google[4]}"  
    
    password = 'XXXXXXX'
    
    #Configurações de comunicação 
    msg.add_header('Content_Type', 'text/html')
    msg.set_payload(corpo_do_email)
    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    
    #credenciais de login
    s.login(msg['From'],password)
    s.sendmail(msg['From'],[msg['To']], msg.as_string().encode('utf-8'))
    print('(Mudança de Status)Email enviado com sucesso.') 
    
    
    
    
# pessoa = "3S Fulano"
# pn = "70150-07100-043"
# status_anterior = "Solicitado"
# status = "Autorizado"
# pedido = "12399895"

# enviar_email_status (pessoa, pedido, status, status_anterior) 
# enviar_email_pedido_gerado(pessoa, pn , pedido, status) 
# enviar_email_solicitacao(pessoa, pn) 