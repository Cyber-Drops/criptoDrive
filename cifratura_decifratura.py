from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from os import path

#verifica esistenza chiavi
def simmetric_k_exist(s_k_name:str):
    '''
    Verifica presenza della chiave simmetrica
    :param s_k_name: path + nome chiave simmetrica
    :return: bool (True se esiste, False se non esiste)
    '''
    if path.exists(s_k_name):
        return True
    else:
        return False

def public_k_exist(publ_k_name:str):
    '''
       Verifica presenza della chiave publica
       :param publ_k_name: path + nome chiave publica
       :return: bool (True se esiste, False se non esiste)
       '''
    if path.exists(publ_k_name):
        return True
    else:
        return False

def private_k_exist(priv_k_name:str):
    '''
       Verifica presenza della chiave privata
       :param s_k_name: path + nome chiave privata
       :return: bool (True se esiste, False se non esiste)
       '''
    if path.exists(priv_k_name):
        return True
    else:
        return False

#generazione delle chiavi
def new_simmetryc_key(s_k_name:str):
    '''
    Genera la chiave simmetrica
    :param s_k_name: path + nome chiave simmetrica
    '''
    key = Fernet.generate_key()
    with open(s_k_name, "wb") as s_key:
        s_key.write(key)

def new_rsa_key(public_exponent: int, key_size: int):
    '''
    Genera chiave privata e publica, algoritmo rsa
    :param public_exponent: int default 65537
    :param key_size: int default 2048
    :return: private_key, public_key
    '''
    public_exponent = 65537
    key_size = 2048
    private_key = rsa.generate_private_key(
        public_exponent=public_exponent,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()  # creo la chiave pubblica dalla privata
    return private_key, public_key

def serializza_priv_key(private_key, alg_pw:bytes):
    '''
    Serializza la chiave privata, con algoritmo di Encoding .pem, formato .pkcs8,
    cifrato con password.
    :param private_key: chiave privata da new_rsa_key
    :param alg_pw: passwor nel formato bytes string
    :return: priv_key_serial: chiave privata serializzata
    '''
    priv_key_serial = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(alg_pw),
    )
    return priv_key_serial

def serializza_pub_key(public_key):
    '''
    Serializza la chiave privata, con algoritmo di Encoding .pem, formato publico
    :param public_key: chiave privata generata da new_rsa_key
    :return: pub_key_serial: chiave publica serializzata
    '''
    pub_key_serial = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )
    return pub_key_serial

def export_key(priv_k_name:str, publ_k_name, priv_key_serial, pub_key_serial):
    '''
    Esporta lla chiave privata e publica su file
    :param priv_k_name: path + nome chiave privata
    :param publ_k_name: path + nome chiave publica
    :param priv_key_serial: chiave privata serializzata tramite serializza_priv_key()
    :param pub_key_serial: chiave publica serializzata tramite serializza_pub_key()
    '''
    with open(priv_k_name, 'wb') as f: f.write(priv_key_serial)
    with open(publ_k_name, 'wb') as f: f.write(pub_key_serial)
#CARICA CHIAVI

def carica_asimmetr_k(priv_k_name:str, publ_k_name:str, alg_pw:bytes):
    with open(publ_k_name, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
        key_file.read(),
       )
    with open(priv_k_name, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
        key_file.read(),
        password = alg_pw,
       )
    return public_key, private_key

def carica_simmetric_k(s_k_name:str):
    with open(s_k_name, "rb") as f:
        simmetr_key = f.read()
        s_token = Fernet(simmetr_key)
    return simmetr_key, s_token

#CIFRATURA E DECIFRATURA CHIAVE SIMMETRICA
def cifra_s_key(s_key:bytes, pub_key:bytes ):
   pass

def decifra_s_key(s_k_name:str, priv_k_name:str):
  pass

#CIFTRAURA FILE
def s_cifra_file(s_token,root:str, files:list):
    '''
    Cifra i file con la chiave simmetrica
    :param root: path + file da cifrare
    :param files: nome file da cifrare
    :return: None
    '''
    for f in files:
        if ".py" not in f and ".key" not in f and ".pem" not in f and ".json" not in f:
            path_file = f"{root}\{f}"
            with open(path_file, "rb") as file:
                file_data = file.read()
                cipher = s_token.encrypt(file_data)
            with open(path_file, "wb") as file:
                file.write(cipher)

#DECIFRATURA
def s_decifra_file(s_token, root:str, files:list):
    for f in files:
        if ".py" not in f and ".key" not in f and ".pem" not in f and ".json" not in f :
            path_file = f"{root}\{f}"
            with open(path_file, "rb") as file:
                file_data = file.read()
                plain = s_token.decrypt(file_data)
            with open(path_file, "wb") as file:
                file.write(plain)


