''''
Created By: rchrdpdrz
Date:09/15/2022
required modules:
requests
beautifulsoup
colorama
env:pipenv
'''
import requests
from bs4 import BeautifulSoup
from colorama import Fore,init
init()

def main() -> None:
    '''receives an ID number and proceeds to download
the user information hosted on the cne web site'''
    print(Fore.YELLOW+'V(cedula) para venezolanos\nE(cedula) para extranjeros\npara salir \'n\'\n')
    id_number_raw=input(Fore.WHITE + 'Cedula: ')
    id_status=id_number_raw[0].upper()
    id_number=''.join(i for i in id_number_raw[1:len(id_number_raw)])
    if id_number.isdigit() and id_status=='V' or id_status=='E':
        print(id_scraping(id_number,id_status))
    elif id_status.lower() == 'n':
        exit()
    else:
        print(Fore.RED+'\nFormato incorrecto\n')
    return main()


def id_scraping(num,status):
    '''
the ID function is in charge of making a request
to the cne (national electoral council)
page which contains information of all
Venezuelan citizens of legal age registered
in the electoral system,by means of this request
you can obtain the public information of the page
which is transformed using the beautifulsoup library
so that the data can be visible in a much more comfortable way.
'''
    try:
        response = requests.get(f'http://www.cne.gob.ve/web/registro_electoral/ce.php?nacionalidad={status}&cedula={num}')
        if response.status_code == 200:
            payload=response.content
            html=BeautifulSoup(payload,'html.parser')
            text=html.text.splitlines()
            info = [i for i in text if i.strip()]
            # by sorting the html we can see that depending on where the word 'estatus'
            # appears we can know if they are deceased or not registered.
            if info[4] == 'ESTATUS':
                load=Fore.RED + '\n Fallecido \n'
            elif info[3] == 'ESTATUS' or info[1] == 'ESTATUS':
                load=Fore.BLUE + '\n No Registrado \n'
            else:
                load=Fore.GREEN + f'''
{info[4]} {info[5]}
{info[6]} {info[7]}
{info[8]} {info[9]}
{info[10]} {info[11]}
{info[14]} {info[15]}\n'''
            return load
    except requests.exceptions.HTTPError as errh:
        return f'{Fore.RED}\nHttp Error:{errh},\n'
    except requests.exceptions.ConnectionError as errc:
        return f'{Fore.RED}\nError Connecting:{errc},\n'
    except requests.exceptions.Timeout as errt:
        return f'{Fore.RED}\nTimeout Error:{errt},\n'
    except requests.exceptions.RequestException as err:
        return f'{Fore.RED}\nOOps: Something Else{err},\n'

if __name__=='__main__':
    main()
    