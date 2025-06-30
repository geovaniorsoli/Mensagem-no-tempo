import datetime
import pywhatkit
from dotenv import load_dotenv
import os

load_dotenv()

def sendMessage(NUMBER, MESSAGE, YEAR, MONTH, DAY, HOUR, MIN):
    try:
        sendDate = datetime.datetime(YEAR, MONTH, DAY, HOUR, MIN, 0, 0)
    except ValueError as e:
        print(f"Erro ao criar a data de envio. Verifique se o ano, mês, dia, hora e minuto são válidos: {e}")
        return

    now = datetime.datetime.now()
    
    if sendDate < now:
        print(f"Erro: A data e hora agendadas ({sendDate.strftime('%d/%m/%Y às %H:%M')}) já passaram em relação à hora atual ({now.strftime('%d/%m/%Y às %H:%M')}).")
        print("Por favor, agende para uma data e hora futuras.")
        return
    
    waitTime = (sendDate - now).total_seconds()
    
    if waitTime < 30: # Por exemplo, se faltar menos de 30 segundos, não vale a pena agendar
        print("Erro: O tempo de agendamento é muito curto para o pywhatkit (menos de 30 segundos restantes).")
        print(f"Hora atual: {now.strftime('%H:%M:%S')}, Hora agendada: {sendDate.strftime('%H:%M:%S')}")
        return # Sai da função se o tempo for muito curto

    print(f"Mensagem agendada para: {sendDate.strftime('%d/%m/%Y às %H:%M:%S')}\n") 
    print(f"A mensagem será enviada em aproximadamente {int(waitTime)} segundos.")
    
    try:
        pywhatkit.sendwhatmsg(NUMBER, MESSAGE, HOUR, MIN, wait_time=20, tab_close=True)
        
        print("Mensagem enviada com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao enviar a mensagem: {e}")

# --- Execução Principal ---
if __name__ == "__main__":
    # Captura as variáveis do .env
    NUMBER = os.getenv('WHATSAPP_NUMERO')
    MESSAGE = os.getenv('WHATSAPP_MENSAGEM')
    
    # Pega as variáveis de data e hora como strings e converte
    YEAR_STR = os.getenv('SEND_YEAR')
    MONTH_STR = os.getenv('SEND_MONTH')
    DAY_STR = os.getenv('SEND_DAY')
    HOUR_STR = os.getenv('SEND_HOUR')
    MIN_STR = os.getenv('SEND_MIN')

    # Verifica se todas as variáveis foram carregadas
    
    
    if not all([NUMBER, MESSAGE, YEAR_STR, MONTH_STR, DAY_STR, HOUR_STR, MIN_STR]):
        print("Erro: Verifique se todas as variáveis (WHATSAPP_NUMERO, WHATSAPP_MENSAGEM, SEND_YEAR, SEND_MONTH, SEND_DAY, SEND_HOUR, SEND_MIN) estão definidas no seu arquivo .env.")
    else:
        try:
            # Converte as strings para inteiros
            YEAR = int(YEAR_STR)
            MONTH = int(MONTH_STR)
            DAY = int(DAY_STR)
            HOUR = int(HOUR_STR)
            MIN = int(MIN_STR)
            
            # Validação básica de hora e minuto (o datetime.datetime já valida a data)
            if not (0 <= HOUR <= 23 and 0 <= MIN <= 59):
                print("Erro: A hora deve estar entre 0 e 23, e o minuto entre 0 e 59.")
            else:
                sendMessage(NUMBER, MESSAGE, YEAR, MONTH, DAY, HOUR, MIN)
        except ValueError as e:
            print(f"Erro de conversão: YEAR, MONTH, DAY, HOUR e MIN no arquivo .env devem ser números inteiros. Detalhe: {e}")
        except Exception as e:
            print(f"Ocorreu um erro inesperado: {e}")