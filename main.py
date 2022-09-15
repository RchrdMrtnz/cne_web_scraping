''''
Created By: rchrdpdrz
Date:09/15/2022
required modules:
requests
beautifulsopu
colorama
'''
import requests
from bs4 import BeautifulSoup
from colorama import Fore,init
init()

def dni(num):
    '''
the dni function is in charge of making a request
to the cne (national electoral council)
page which contains information of all
Venezuelan citizens of legal age registered
in the electoral system,by means of this request
you can obtain the public information of the page
which is transformed using the beautifulsoup library
so that the data can be visible in a much more comfortable way.
'''
    try:
        response = requests.get(f'http://www.cne.gob.ve/web/registro_electoral/ce.php?nacionalidad=V&cedula={num}')
        if response.status_code == 200:
            payload=response.content
            html=BeautifulSoup(payload,'html.parser')
            text=html.text.splitlines()
            info = [i for i in text if i.strip()]
            deceased=f'{info[4]}'
            unregistered=f'{info[3]}'
            if deceased == 'ESTATUS':
                final=Fore.RED + ' Fallecido '
            elif unregistered == 'ESTATUS':
                final=Fore.BLUE + ' No Registrado '
            else:
                final=Fore.GREEN + f'''
{info[4]} {info[5]}
{info[6]} {info[7]}
{info[8]} {info[9]}
{info[10]} {info[11]}
{info[14]} {info[15]}'''
            return final
    except requests.exceptions.HTTPError as errh:
        print ("Http Error:",errh)
    except requests.exceptions.ConnectionError as errc:
        print ("Error Connecting:",errc)
    except requests.exceptions.Timeout as errt:
        print ("Timeout Error:",errt)
    except requests.exceptions.RequestException as err:
        print ("OOps: Something Else",err)

while True:
    dni_number=input('Cedula: ')
    if dni_number.isdigit():
        print(dni(dni_number))
    else:
        print(Fore.RED+'\nSolo Numeros\n')
    print(Fore.WHITE)
    continuar=input('Enter para continuar "n" para salir\n')
    if continuar.lower() == 'n' or continuar.lower() == 'no':
        break
    