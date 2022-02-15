import pathLocale
import os
import io
import mimetypes
from pathLocale import path_scan
from cifratura_decifratura import simmetric_k_exist, private_k_exist, public_k_exist,carica_simmetric_k, carica_asimmetr_k,\
                            new_rsa_key, new_simmetryc_key, serializza_priv_key, serializza_pub_key, export_key, s_cifra_file, \
                            s_decifra_file
from googleapiclient.http import MediaFileUpload,MediaIoBaseDownload

def elabora_path(path_selected):
    #path_tree = path_scan(pathLocale.directory)
    #print(path_tree)
    path_tree = path_scan(path_selected)
    '''
    files_list = path_tree[path_selected][1]
    path_root = list(path_tree.keys())[0]
    print(path_root)
    print(files_list)
    '''
    return path_tree
        #path_root, files_list

def gestisci_key(nome_s_k: str,nome_pri_k: str,nome_pub_key: str,alg_passw: bytes):
    passw = alg_passw
    if not simmetric_k_exist(nome_s_k):
        new_simmetryc_key(s_k_name=nome_s_k)
    simmetric_key, token = carica_simmetric_k(s_k_name=nome_s_k)
    if not private_k_exist(priv_k_name=nome_pri_k) and not public_k_exist(publ_k_name=nome_pub_key):
        private_key, public_key = new_rsa_key(65537, 2048)
        priv_key_serial = serializza_priv_key(private_key=private_key, alg_pw=passw)
        pub_key_serial = serializza_pub_key(public_key=public_key)
        export_key(priv_k_name=nome_pri_k, publ_k_name=nome_pub_key, priv_key_serial=priv_key_serial,
                   pub_key_serial=pub_key_serial)
    public_key, private_key = carica_asimmetr_k(priv_k_name=nome_pri_k, publ_k_name=nome_pub_key, alg_pw=passw)
    return simmetric_key, token, public_key, private_key

def cifratura(token, path_root: str ,files_list: list):
    s_cifra_file(s_token=token,root=path_root,files=files_list)

def decifra(token, path_root: str, files_list: list):
    s_decifra_file(s_token=token, root=path_root, files=files_list)

def upload_fileservice(service,root,files):
    for f in files:
        if ".py" not in f and ".key" not in f and ".pem" not in f and ".json" not in f:
            path_file = f"{root}\{f}"
            path_root, extension = os.path.splitext(path_file)
            mime = mimetypes.types_map[extension]
            file_meta = {'name':f}
            media = MediaFileUpload(path_file, mimetype=mime, chunksize=262144, resumable=True)
            page_token = None
            response = service.files().list(q=f"name = '{f}'",
                                            spaces='drive',
                                            fields='nextPageToken, files(id, name)',
                                            pageToken=page_token).execute()  # ritorna un json
            print("resp", response)
            if not response['files']:
                print("nuovo")
                file = service.files().create(media_body=media, body=file_meta).execute()
                '''
                response = None
                while response is None:
                    status, response = file.next_chunk()
                    if status:
                        print("Uploaded %d%%" % int(status.progress() * 100))
                        print("complete")'''
            else:
                print("aggiorna")
                for file in response.get('files', []):
                    fileid = file.get('id')
                    file = service.files().update(media_body=media, body=file_meta, fileId=fileid).execute()


def download_fileservice(service,root,files):
    for f in files:
        if ".py" not in f and ".key" not in f and ".pem" not in f and ".json" not in f:
            path_file = f"{root}\{f}"
            path_root, extension = os.path.splitext(path_file)
            mime = mimetypes.types_map[extension]
            file_meta = {'name': f}
            media = MediaFileUpload(path_file, mimetype=mime, chunksize=262144, resumable=True)
            page_token = None
            response = service.files().list(q=f"name = '{f}'", spaces='drive', fields='nextPageToken, files(id, name)',
                                    pageToken=page_token).execute()  # ritorna un json
            if not response['files']:
                continue
            else:
                for file in response.get('files', []):
                    fileid = file.get('id')
                    filed = service.files().get_media(fileId=fileid)
                    fh = io.FileIO(path_file, mode='wb')# il path completo con il file
                    downloader = MediaIoBaseDownload(fh, filed)
                    done = False
                    while done is False:
                        status, done = downloader.next_chunk()
                        print("Download %d%%." % int(status.progress() * 100))



#UPGRADE METADATI
mimetypes.add_type("image/jpeg",".jfif")





