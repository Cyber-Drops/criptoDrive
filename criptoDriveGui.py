from breezypythongui import EasyFrame
from tkinter import filedialog
from autent_oauthV2 import autenticazione, build_service
import os
from tkinter import PhotoImage
import socket
import pathLocale
import cryptoDrive

#Finestra Principale
class CriptoDriveGui(EasyFrame):
    def __init__(self):
        EasyFrame.__init__(self, title="][---CriptoDrive---][",width=800, height=500, resizable=False)

        # Disposizione Pannelli
        dataPanel = self.addPanel(row=0, column=0, background="white")
        radioPanel = self.addPanel(row=1, column= 0, background="")
        buttonPanel = self.addPanel(row=2, column=0, background="black")

        # Panel Uno
        dataPanel.addLabel(text="PATH: ", row=0, column=0, sticky="NSEW")
        dataPanel.addLabel(text="Path_Simmetryc_Key:", row= 1, column=0, sticky="NSEW")
        dataPanel.addLabel(text="Path_Private_Key:", row= 2, column=0, sticky="NSEW")
        dataPanel.addLabel(text="Path_Public_Key:", row= 3, column=0, sticky="NSEW")
        dataPanel.addLabel(text="Alg_password:", row=4, column=0, sticky="NSEW")

        self.FilePath = dataPanel.addTextField(text="seleziona cartella", row=0, column=1, width=70, sticky="EW")
        self.S_K_Path = dataPanel.addTextField(text="simmetryc .key", row=1, column=1, width=70, sticky="EW")
        self.Priv_K_Path = dataPanel.addTextField(text="private key .pem", row=2, column=1, width=70, sticky="EW")
        self.Pub_K_Path = dataPanel.addTextField(text="public key .pem", row=3, column=1, width=70, sticky="EW")
        self.Alg_Passw = dataPanel.addTextField(text="", row=4, column=1, width=70, sticky="EW")

        self.bt_file_path = dataPanel.addButton(text="Seleziona", row=0, column=2, command=self.selezionaPath)
        self.bt_s_key = dataPanel.addButton(text="Simmetric_key", row=1, column=2, command=self.select_s_key)
        self.bt_priv_key = dataPanel.addButton(text="Private_key", row=2, column=2, command=self.select_priv_key)
        self.bt_pub_key = dataPanel.addButton(text="Public_key", row=3, column=2, command=self.select_pub_key)

        #Panel tre
        # Radio_label
        self.radioLabel = radioPanel.addLabel(text="Modalità", row=0, column=1)
        self.radioLabel["height"] = 0
        #Key_radioGroup
        self.Key_radioGroup = radioPanel.addRadiobuttonGroup(row=1,column=1, orient="horizontal")
        defaultKrb = self.Key_radioGroup.addRadiobutton(text="NewSimmetricKey")
        self.Key_radioGroup.setSelectedButton(defaultKrb)
        self.Key_radioGroup.addRadiobutton(text="NewRsaKey")
        self.Key_radioGroup.addRadiobutton(text="BothKey")
        self.Key_radioGroup.addRadiobutton(text="KeyExist")
        #Path_radioGroup
        self.Path_radioGroup = radioPanel.addRadiobuttonGroup(row=2, column=1, orient="horizontal")
        defaultPrb = self.Path_radioGroup.addRadiobutton(text="LocalPath")
        self.Path_radioGroup.setSelectedButton(defaultPrb)
        self.Path_radioGroup.addRadiobutton(text="Recursive")
        #Folder_radioGroup
        self.Folder_radioGroup = radioPanel.addRadiobuttonGroup(row=3,column=1, orient="horizontal")
        defaultFold = self.Folder_radioGroup.addRadiobutton(text="Generale")
        self.Folder_radioGroup.setSelectedButton(defaultFold)
        self.Folder_radioGroup.addRadiobutton(text="DriveFolder")
        #Reomote_radioGroup
        self.Remote_radioGroup = radioPanel.addRadiobuttonGroup(row=4, column=1, orient="horizontal")
        defaultRrb = self.Remote_radioGroup.addRadiobutton(text="Nothing")
        self.Remote_radioGroup.setSelectedButton(defaultRrb)
        self.Remote_radioGroup.addRadiobutton(text="Upload")
        self.Remote_radioGroup.addRadiobutton(text="Download")


        # Panel quattro
        self.new_directory = buttonPanel.addButton(text="DriveFolder", row=0, column=0, command=self.directory_drive)
        self.buttonCifra = buttonPanel.addButton(text="Cifra->", row=0, column=0, columnspan=2, command=self.cifra)
        self.buttonCifra["width"] = 20
        self.buttonCifra["height"] = 2
        self.buttonDecifra = buttonPanel.addButton(text="Decifra->", row=1, column=0, columnspan=2, command=self.decifra)
        self.buttonDecifra["width"] = 20
        self.buttonDecifra["height"] = 2
        self.buttonHelp = buttonPanel.addButton(text="??Help??", row=1,column=1, columnspan=2, command=self.help)
        self.buttonHelp["width"] = 15
        self.buttonHelp["height"] = 2
        self.LabelAuthor = buttonPanel.addLabel("Autore: Simone Tempesta\nwww.cyber-drops.com", row=3, column=0,columnspan=2)

    def selezionaPath(self):
        self.nomeDirect = filedialog.askdirectory(parent=self, title="CipherUpload")
        #self.nomeDirect = filedialog.askopenfilenames()
        self.FilePath.setText(self.nomeDirect)
        self.selected_path = self.nomeDirect
        #self.path_root, self.files_list =
        self.path_tree = cryptoDrive.elabora_path(self.selected_path)

    def select_s_key(self):
        key_radio_button = self.Key_radioGroup.getSelectedButton()["text"]
        if key_radio_button == "NewSimmetricKey" or key_radio_button == "BothKey":
            self.nome_s_k = filedialog.askdirectory(title="directory Key")
            self.S_K_Path.setText(f"{self.nome_s_k}/simmetric.key")
            self.nome_s_k = f"{self.nome_s_k}/simmetric.key"
        else:
            self.nome_s_k = filedialog.askopenfilename(title="Simmetryc Key",filetypes=[("simmetry_key", ".key")])
            self.S_K_Path.setText(self.nome_s_k)

    def select_priv_key(self):
        key_radio_button = self.Key_radioGroup.getSelectedButton()["text"]
        if key_radio_button == "NewRsaKey" or key_radio_button == "BothKey":
            self.nome_pri_k = filedialog.askdirectory(title="directory Key")
            self.Priv_K_Path.setText(f"{self.nome_pri_k}/private.pem")
            self.nome_pri_k = f"{self.nome_pri_k}/private.pem"
        else:
            self.nome_pri_k = filedialog.askopenfilename(title="Private Key",filetypes=[("private_key", ".pem")])
            self.Priv_K_Path.setText(self.nome_pri_k)

    def select_pub_key(self):
        key_radio_button = self.Key_radioGroup.getSelectedButton()["text"]
        if key_radio_button == "NewRsaKey" or key_radio_button == "BothKey":
            self.nome_pub_key = filedialog.askdirectory(title="directory Key")
            self.Pub_K_Path.setText(f"{self.nome_pub_key}/public.pem")
            self.nome_pub_key = f"{self.nome_pub_key}/public.pem"
        else:
            self.nome_pub_key = filedialog.askopenfilename(title="Public Key",filetypes=[("public_key", ".pem")])
            self.Pub_K_Path.setText(self.nome_pub_key)

    def directory_drive(self):
        pass

    def share_file_folder(self):
        pass

    def cifra(self):
        passw =self.Alg_Passw.getText()
        passw = bytes(passw, "UTF-8")
        simmetric_key, token, public_key, private_key = cryptoDrive.gestisci_key(nome_s_k=self.nome_s_k,nome_pri_k=self.nome_pri_k,nome_pub_key=self.nome_pub_key,alg_passw=passw)
        path_radio_button = self.Path_radioGroup.getSelectedButton()["text"]
        remote_radio_button = self.Remote_radioGroup.getSelectedButton()["text"]
        folder_radio_button = self.Folder_radioGroup.getSelectedButton()["text"]
        if remote_radio_button == "Upload":
            service = self.connetti()
        if path_radio_button == "LocalPath":
            files_list = self.path_tree[self.selected_path][1]
            path_root = list(self.path_tree.keys())[0]
            cryptoDrive.cifratura(token=token, path_root=path_root, files_list=files_list)
            self.buttonCifra["state"] = "disable"
            self.buttonDecifra["state"] = "normal"
            if remote_radio_button == "Upload" and folder_radio_button == "Generale":
                folderid = None
                cryptoDrive.upload_fileservice(service=service,root=path_root,files=files_list,folderid=folderid)
            if remote_radio_button == "Upload" and folder_radio_button == "DriveFolder":
                self.drive_folder = filedialog.askdirectory(title="Drive Directory")
                folderid = cryptoDrive.create_folder(service=service,folder_name=self.drive_folder)
                cryptoDrive.upload_fileservice(service=service, root=path_root, files=files_list, folderid=folderid)
        else:
            for directory in self.path_tree.keys():
                path_root = directory
                files_list = self.path_tree[directory][1]
                cryptoDrive.cifratura(token=token, path_root=path_root, files_list=files_list)
                self.buttonCifra["state"] = "disable"
                self.buttonDecifra["state"] = "normal"
                if remote_radio_button == "Upload":
                    cryptoDrive.upload_fileservice(service, path_root, files_list)

    def decifra(self):
        passw = self.Alg_Passw.getText()
        passw = bytes(passw, "UTF-8")
        simmetric_key, token, public_key, private_key = cryptoDrive.gestisci_key(nome_s_k=self.nome_s_k,nome_pri_k=self.nome_pri_k,nome_pub_key=self.nome_pub_key,alg_passw=passw)
        path_radio_button = self.Path_radioGroup.getSelectedButton()["text"]
        remote_radio_button = self.Remote_radioGroup.getSelectedButton()["text"]
        if remote_radio_button == "Download":
            print("connetti")
            service = self.connetti()
        if path_radio_button == "LocalPath":
            files_list = self.path_tree[self.selected_path][1]
            path_root = list(self.path_tree.keys())[0]
            print(remote_radio_button)
            if remote_radio_button == "Download":
                cryptoDrive.download_fileservice(service, path_root, files_list)
            cryptoDrive.decifra(token=token, path_root=path_root, files_list=files_list)
            self.buttonDecifra["state"] = "disable"
            self.buttonCifra["state"] = "normal"
        else:
            for directory in self.path_tree.keys():
                path_root = directory
                files_list = self.path_tree[directory][1]
                if remote_radio_button == "Download":
                    cryptoDrive.download_fileservice(service, path_root, files_list)
                cryptoDrive.decifra(token=token, path_root=path_root, files_list=files_list)
                self.buttonDecifra["state"] = "disable"
                self.buttonCifra["state"] = "normal"

    def connetti(self):
        scopes = ["https://www.googleapis.com/auth/drive"]
        service = "dirve"
        version = "v3"
        a_token = filedialog.askopenfilename(title="OAUTH2",filetypes=[("token", ".json")])
        c_secret = filedialog.askopenfilename(title="OAUTH2",filetypes=[("c_secret", ".json")])
        c_secret_path, extension = os.path.splitext(c_secret)
        if a_token == "":
            a_token = c_secret_path
        creds = autenticazione(scopes=scopes,token=a_token,client_scret=c_secret)
        service = build_service(service=service,version=version,creds=creds)
        return service

    def help(self):
        pass

def main():
    CriptoDriveGui().mainloop()
if __name__ == "__main__":
    main()
    '''
    def selezionaFile(self):
        self.nomeFile = filedialog.LoadFileDialog.ok_command()
       '''

