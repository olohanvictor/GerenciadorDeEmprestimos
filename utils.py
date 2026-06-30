from datetime import datetime

def formatar_cpf_str(texto):
    cpf = ''.join(filter(str.isdigit, texto))
    if len(cpf) > 11: 
        cpf = cpf[:11]
        
    if len(cpf) > 9:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    elif len(cpf) > 6:
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:]}"
    elif len(cpf) > 3:
        return f"{cpf[:3]}.{cpf[3:]}"
    return cpf


def formatar_data_str(texto):
    data = ''.join(filter(str.isdigit, texto))
    if len(data) > 8: 
        data = data[:8]
        
    if len(data) > 4:
        return f"{data[:2]}/{data[2:4]}/{data[4:]}"
    elif len(data) > 2:
        return f"{data[:2]}/{data[2:]}"
    return data


def es_data_valida(data):
    try:
        datetime.strptime(data, "%d/%m/%Y")
        return True
    except:
        return False