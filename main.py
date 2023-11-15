from copy import deepcopy
import PySimpleGUI as sg
import pyodbc
import pandas as pd

sql_ukaz_tags = "SELECT * FROM [Test_sql_log].[dbo].[TagTable]"
sqk_ukaz_floats = "SELECT * FROM [Test_sql_log].[dbo].[FloatTable]"
sql_ukaz_strings = "SELECT * FROM [Test_sql_log].[dbo].[StringTable]"

izb_sarze = True
izb_bitumen = True
izb_lfiler = True
izb_tfiler = True
izb_mineralos = True
izb_frezani = True
izb_aditiv = True
izb_k1 = True
izb_k2 = True
izb_k3 = True
izb_k4 = True
izb_k5 = True
izb_k6 = True

#-------------------------------------------#
#             spremenljivke za layout       #
#-------------------------------------------#
naslov_text = sg.Text("Statistika ", size=75)
povezava_text = sg.Text("Povezava ni vzpostavljena", text_color="red",
                        font=("Arial", 15), background_color="White", key="povezava")
driver_text = sg.Text("Driver:")
driver_input = sg.InputText("SQL Server", size=25, key="driver")
server_text = sg.Text("Server:")
server_input = sg.InputText("DESKTOP-2JDLM40\SQLEXPRESS", size=35, key="server")
baza_text = sg.Text("SQL baza:")
baza_input = sg.InputText("Test_sql_log", size=20, key="baza")
connect_button = sg.Button("Poveži se", key="connect")

rows = []
# Za izbrisati
header = ["TagName", "TagIndex", "TagType", "TagDataType"]
tagi_table = sg.Table(values=rows, headings=header,
                      auto_size_columns=True, expand_x=True, expand_y=True,
                      justification='center', key="tabela_tagov")
pridobi_podatke = sg.Button("Pokaži podatke", key="podatki")
# Do tukaj

header2 = ["Datum","ura", "milisekunde", "TagIndex", "Vrednost"]
vrednosti_table = sg.Table(values=rows, headings=header2,
                      auto_size_columns=True, expand_x=True,
                      justification='center', key="tabela_float")

header3 = ["Datum","ura", "milisekunde", "TagIndex", "Vrednost"]
recepti_table = sg.Table(values=rows, headings=header3,
                      auto_size_columns=True, expand_x=True,
                      justification='center', key="tabela_string")
#------------------------------------------------#
#                  Kolendar                      #
#------------------------------------------------#

kolendar_od_prikaz = sg.Input(key="kolendar_input_od", enable_events=True)
kolendar_od = sg.CalendarButton("Koledar", pad=None, key="kolendarod", target="kolendar_input_od",
                                font=('MS Sans Serif', 10, 'bold'),format=('%d %B, %Y'))

kolendar_do_prikaz = sg.Input(key="kolendar_input_do", enable_events=True)
kolendar_do = sg.CalendarButton("Koledar", pad=None, key="kolendardo",format=('%d %B, %Y'),
                                target="kolendar_input_do")
kolendar_layout = [kolendar_od, kolendar_od_prikaz, kolendar_do, kolendar_do_prikaz]

#------------------------------------------------#
#               tabela in checkboxi              #
#------------------------------------------------#
izbor_elementov_header = ["    Datum    ", " Recept ", "Sarže", "Bitumen Rec", "Bitumen Izd", "L Filer Rec",
                          "L Filer Izd", "T Filer Rec", "T Filer Izd", "Mineral OS Rec",
                          "Mineral OS Izd", "Frezani Rec", "Frezani Izd", "Aditiv Rec", "Aditiv Izd",
                          "K1 Rec", "K1 Izd", "K2 Rec", "K2 Izd", "K3 Rec", "K3 Izd", "K4 Rec", "K4 Izd",
                          "K5 Rec", "K5 Izd", "K6 Rec", "K6 Izd"]
izracun_table = sg.Table(values=rows, headings=izbor_elementov_header,
                      auto_size_columns=True, expand_x=True, num_rows=25, vertical_scroll_only=False,
                      justification='center', key="izracun", visible=False, alternating_row_color="green",
                         max_col_width=20)

recepti_listbox = sg.Listbox(rows,size=(50, 10), key="recepti",
                             enable_events=True)

dnevno_checkbox = sg.Checkbox("Sarže", key="dnevno", visible=False, enable_events=True, default=True)
bitumen_checkbox = sg.Checkbox("Bitumen", key="bitumen", visible=False, enable_events=True, default=True)
frezani_checkbox = sg.Checkbox("Frezani", key="frezani", visible=False, enable_events=True, default=True)
k1_checkbox = sg.Checkbox("K1", key="k1", visible=False, enable_events=True, default=True)
k2_checkbox = sg.Checkbox("K2", key="k2", visible=False, enable_events=True, default=True)
k3_checkbox = sg.Checkbox("K3", key="k3", visible=False, enable_events=True, default=True)
k4_checkbox = sg.Checkbox("K4", key="k4", visible=False, enable_events=True, default=True)
k5_checkbox = sg.Checkbox("K5", key="k5", visible=False, enable_events=True, default=True)
k6_checkbox = sg.Checkbox("K6", key="k6", visible=False, enable_events=True, default=True)
aditiv_checkbox = sg.Checkbox("Aditiv", key="aditiv", visible=False, enable_events=True, default=True)
l_filer_checkbox = sg.Checkbox("Lastni filer", key="lfiler", visible=False, enable_events=True, default=True)
t_filer_checkbox = sg.Checkbox("Tuj filer", key="tfiler", visible=False, enable_events=True, default=True)
mineral_os_checkbox = sg.Checkbox("Mineral OS", key="mineralos", visible=False, enable_events=True, default=True)
vrednost_statusbar = sg.StatusBar("0000 KG", key="vrednost", enable_events=True, visible=False)

checkbox_layout=[dnevno_checkbox, bitumen_checkbox, l_filer_checkbox, t_filer_checkbox,
                 mineral_os_checkbox, frezani_checkbox, aditiv_checkbox, k1_checkbox, k2_checkbox,
                 k3_checkbox, k4_checkbox, k5_checkbox, k6_checkbox]

progress_bar = sg.ProgressBar(1000, orientation="v", size=(15,20), key="progress")

checkbox_frame = sg.Frame("Minerali", [checkbox_layout], key="checkbox_frame")
layout = [[naslov_text, povezava_text],
          [driver_text, driver_input, server_text, server_input, baza_text, baza_input, connect_button],
          [kolendar_layout],
          [pridobi_podatke],
          [vrednosti_table,recepti_table],
          [recepti_listbox,progress_bar],
          [vrednost_statusbar],
          [checkbox_frame],
          [izracun_table]
          ]

window = sg.Window('Statistika 0.1', layout, size=(800,600),resizable=True, finalize=True)
window.maximize()

prikaz_table = window["izracun"]

povezava_vzpostavljena = 0
podatki_prejeti = 0
vse_vrednosti_receptov_po_receptu = {}
vse_vrednosti_dolocenega_recepta = {}
vse_vrednosti_dolocenega_recepta_list = []
new_list = []

def dodaj_vrstico(val = ""):
    displaycolumns = deepcopy(izbor_elementov_header)
    displaycolumns.append(val)
    prikaz_table.ColumnsToDisplay = displaycolumns
    prikaz_table.Widget.configure(displaycolumns=displaycolumns)
    izbor_elementov_header.append(val)


def izbrisi_vrstico(val=""):
    displaycolumns = deepcopy(izbor_elementov_header)
    displaycolumns.remove(val)
    prikaz_table.ColumnsToDisplay = displaycolumns
    prikaz_table.Widget.configure(displaycolumns=displaycolumns)
    izbor_elementov_header.remove(val)

    
#--------------------------------------------#
#              Začetek Zanke                 #
#--------------------------------------------#
while True:
    event, values = window.read()
    print(1, event)
    print(2, values)

#--------------------------------------------#
#            povezava z tagi                 #
#--------------------------------------------#

    if event == "connect":
        driver = values["driver"]
        server = values["server"]
        baza = values["baza"]
        log_podatki = "DRIVER=" + driver + "; SERVER=" + server + "; DATABASE=" + baza + ";"

        try:
            povezava = pyodbc.connect(log_podatki)
            povezava_vzpostavljena = 1
            window["povezava"].update("Povezava je vzpostavljena", text_color="green")
        except pyodbc.Error as ex:
            print("Povezava ni vzpostavljena")
            window["povezava"].update("Povezava ni vzpostavljena", text_color="red")
            sg.popup("Niste povezani z bazo... \nProsim vnesite pravilne podatke")
            povezava_vzpostavljena = 0

        if povezava_vzpostavljena == 1:
            cursor = povezava.cursor()
            df = pd.read_sql(sql_ukaz_tags, povezava)
            #print(df)
            #window["tabela_tagov"].update(values=df.values)

            if "dnevno" in df["TagName"].values:
                print("Dnevno je na seznamu")
                window["dnevno"].update(visible=True)
            if "bitumen\z_d_bit" in df["TagName"].values:
                window["bitumen"].update(visible=True)
            if "polnila\lp" in df["TagName"].values:
                window["lfiler"].update(visible=True)
            if "polnila\\tp" in df["TagName"].values:
                window["tfiler"].update(visible=True)
            if "minerali\OS" in df["TagName"].values:
                window["mineralos"].update(visible=True)
            if "Frezan\Zdozirana_Kol" in df["TagName"].values:
                window["frezani"].update(visible=True)
            if "VIATOP\Zdozirana" in df["TagName"].values:
                window["aditiv"].update(visible=True)
            if "minerali\k1" in df["TagName"].values:
                window["k1"].update(visible=True)
            if "minerali\k2g" in df["TagName"].values:
                window["k2"].update(visible=True)
            if "minerali\k3" in df["TagName"].values:
                window["k3"].update(visible=True)
            if "minerali\k4" in df["TagName"].values:
                window["k4"].update(visible=True)
            if "minerali\k5" in df["TagName"].values:
                window["k5"].update(visible=True)
            if "minerali\K6" in df["TagName"].values:
                window["k6"].update(visible=True)

            window["izracun"].update(visible=True)

        else:
            print("povezava ni vzpostavljena")
            window["izracun"].update(visible=False)

#---------------------------------------------------#
#           gumb poberi podatke                     #
#---------------------------------------------------#
    elif event == "podatki":
        if povezava_vzpostavljena == 1:
            cursor = povezava.cursor()
            try:
                df2 = pd.read_sql(sqk_ukaz_floats, povezava)
                df3 = pd.read_sql(sql_ukaz_strings, povezava)
                podatki_prejeti = 1
            except pyodbc.Error:
                print("podatki niso prejeti")
                podatki_prejeti = 0
            window["tabela_float"].update(values=df2.values)
            window["tabela_string"].update(values=df3.values)

            recepti = []
            recepti_vsi_podatki = []

            for index, row in df3.iterrows():
                if row["Val"] not in recepti:
                    if row["Val"] != None:
                        recepti.append(row["Val"])
                        recepti_vsi_podatki.append(row)

                    #print(recepti)

            window["recepti"].update(values=recepti)

#-----------------------------------------------#
#             izbor checkboxov                  #
#-----------------------------------------------#
    elif event == "dnevno":
        if values["dnevno"]:
            dodaj_vrstico("Sarže")
        else:
            izbrisi_vrstico("Sarže")

    elif event == "bitumen":
        if values["bitumen"]:
            dodaj_vrstico("Bitumen Rec")
            dodaj_vrstico("Bitumen Izd")
        else:
            izbrisi_vrstico("Bitumen Rec")
            izbrisi_vrstico("Bitumen Izd")

    elif event == "lfiler":
        if values["lfiler"]:
            dodaj_vrstico("L Filer Rec")
            dodaj_vrstico("L Filer Izd")
        else:
            izbrisi_vrstico("L Filer Rec")
            izbrisi_vrstico("L Filer Izd")

    elif event == "tfiler":
        if values["tfiler"]:
            dodaj_vrstico("T Filer Rec")
            dodaj_vrstico("T Filer Izd")
        else:
            izbrisi_vrstico("T Filer Rec")
            izbrisi_vrstico("T Filer Izd")

    elif event == "mineralos":
        if values["mineralos"]:
            dodaj_vrstico("Mineral OS Rec")
            dodaj_vrstico("Mineral OS Izd")
        else:
            izbrisi_vrstico("Mineral OS Rec")
            izbrisi_vrstico("Mineral OS Izd")

    elif event == "frezani":
        if values["frezani"]:
            dodaj_vrstico("Frezani Rec")
            dodaj_vrstico("Frezani Izd")
        else:
            izbrisi_vrstico("Frezani Rec")
            izbrisi_vrstico("Frezani Izd")

    elif event == "aditiv":
        if values["aditiv"]:
            dodaj_vrstico("Aditiv Rec")
            dodaj_vrstico("Aditiv Izd")
        else:
            izbrisi_vrstico("Aditiv Rec")
            izbrisi_vrstico("Aditiv Izd")

    elif event == "k1":
        if values["k1"]:
            dodaj_vrstico("K1 Rec")
            dodaj_vrstico("K1 Izd")
        else:
            izbrisi_vrstico("K1 Rec")
            izbrisi_vrstico("K1 Izd")

    elif event == "k2":
        if values["k2"]:
            dodaj_vrstico("K2 Rec")
            dodaj_vrstico("K2 Izd")
        else:
            izbrisi_vrstico("K2 Rec")
            izbrisi_vrstico("K2 Izd")

    elif event == "k3":
        if values["k3"]:
            dodaj_vrstico("K3 Rec")
            dodaj_vrstico("K3 Izd")
        else:
            izbrisi_vrstico("K3 Rec")
            izbrisi_vrstico("K3 Izd")

    elif event == "k4":
        if values["k4"]:
            dodaj_vrstico("K4 Rec")
            dodaj_vrstico("K4 Izd")
        else:
            izbrisi_vrstico("K4 Rec")
            izbrisi_vrstico("K4 Izd")

    elif event == "k5":
        if values["k5"]:
            dodaj_vrstico("K5 Rec")
            dodaj_vrstico("K5 Izd")
        else:
            izbrisi_vrstico("K5 Rec")
            izbrisi_vrstico("K5 Izd")

    elif event == "k6":
        if values["k6"]:
            dodaj_vrstico("K6 Rec")
            dodaj_vrstico("K6 Izd")
        else:
            izbrisi_vrstico("K6 Rec")
            izbrisi_vrstico("K6 Izd")

        """elif event == "bitumen":
        pass
        try:
            vrednost = 0
            for index, row in df2.iterrows():
                if row["TagIndex"] == 1:
                    vrednost = vrednost + row["Val"]
                    # print(vrednosti)
            int_vrednost = int(vrednost)
            str_vrednost = str(int_vrednost) + " Kg"
            window["vrednost"].update(value=(str_vrednost))
        except NameError:
            sg.popup("Niste povezani z bazo")"""

        """elif event == "lfiler":
        pass
        try:
            vrednost = 0
            for index, row in df2.iterrows():
                if row["TagIndex"] == 21:
                    vrednost = vrednost + row["Val"]
                    # print(vrednosti)
            int_vrednost = int(vrednost)
            str_vrednost = str(int_vrednost) + " Kg"
            window["vrednost"].update(value=(str_vrednost))
        except NameError:
            sg.popup("Niste povezani z bazo")"""
#-----------------------------------------------------#
#                       RECEPTI                       #
#-----------------------------------------------------#
    elif event == "recepti":
        del vse_vrednosti_receptov_po_receptu
        vse_vrednosti_receptov_po_receptu = {"DateAndTime":[]}#pd.DataFrame({"DateAndTime":[],"Militrm":[],"TagIndex":[],"Val":[],"Status":[],"Marker":[]})
        del vse_vrednosti_dolocenega_recepta
        vse_vrednosti_dolocenega_recepta = {"datum":[], "recept":[],"sarza":[], "bitumenrec":[],
                                            "bitumenizd":[], "lfilerrec":[], "lfilerizd":[], "tfilerrec":[], "tfilerizd":[],
                                            "mineralosrec":[], "mineralosizd":[],"frezanirec":[], "frezaniizd":[],
                                            "aditivrec":[], "aditivizd":[], "k1rec":[], "k1izd":[], "k2rec":[], "k2izd":[],
                                            "k3rec":[], "k3izd":[], "k4rec":[], "k4izd":[], "k5rec":[], "k5izd":[],
                                            "k6rec":[], "k6izd":[]}
        vse_vrstice = 0
        for index, row in df3.iterrows(): #gre čez vse vrstice receptov

            #poišče vse zapisane vrednosti receptov in jim shrani datum
            if row["Val"] == values["recepti"][0]:
                vse_vrednosti_receptov_po_receptu["DateAndTime"].append(row["DateAndTime"])
                print("RECEPT IZBRAN")
                vse_vrstice = vse_vrstice + 1
                #print(vse_vrednosti_receptov_po_receptu)

        trenutno_stetje = 0
        window["progress"].update(max=vse_vrstice, current_count = trenutno_stetje)

        for val in vse_vrednosti_receptov_po_receptu["DateAndTime"]:
            trenutno_stetje = trenutno_stetje + 1
            window["progress"].update(current_count=trenutno_stetje)
            for i, row in df2.iterrows():
                if val == row["DateAndTime"]:

                    if row["TagIndex"] == 1:
                        vse_vrednosti_dolocenega_recepta["datum"].append(str(row["DateAndTime"]))
                        vse_vrednosti_dolocenega_recepta["recept"].append(values["recepti"][0])
                        vse_vrednosti_dolocenega_recepta["bitumenizd"].append(round(row["Val"],4))
                        print("dodano")
                    elif row["TagIndex"] == 0:
                        vse_vrednosti_dolocenega_recepta["sarza"].append(row["Val"])
                    elif row["TagIndex"] == 2:
                        vse_vrednosti_dolocenega_recepta["frezaniizd"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 3:
                        vse_vrednosti_dolocenega_recepta["k1izd"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 4:
                        vse_vrednosti_dolocenega_recepta["k2izd"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 5:
                        vse_vrednosti_dolocenega_recepta["k3izd"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 6:
                        vse_vrednosti_dolocenega_recepta["k4izd"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 7:
                        vse_vrednosti_dolocenega_recepta["k5izd"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 8:
                        vse_vrednosti_dolocenega_recepta["k6izd"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 9:
                        vse_vrednosti_dolocenega_recepta["mineralosizd"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 10:
                        vse_vrednosti_dolocenega_recepta["lfilerizd"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 11:
                        vse_vrednosti_dolocenega_recepta["tfilerizd"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 12:
                        vse_vrednosti_dolocenega_recepta["bitumenrec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 13:
                        vse_vrednosti_dolocenega_recepta["frezanirec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 15:
                        vse_vrednosti_dolocenega_recepta["k1rec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 16:
                        vse_vrednosti_dolocenega_recepta["k2rec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 17:
                        vse_vrednosti_dolocenega_recepta["k3rec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 18:
                        vse_vrednosti_dolocenega_recepta["k4rec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 19:
                        vse_vrednosti_dolocenega_recepta["k5rec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 20:
                        vse_vrednosti_dolocenega_recepta["k6rec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 21:
                        vse_vrednosti_dolocenega_recepta["lfilerrec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 22:
                        vse_vrednosti_dolocenega_recepta["mineralosrec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 23:
                        vse_vrednosti_dolocenega_recepta["tfilerrec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 24:
                        vse_vrednosti_dolocenega_recepta["aditivrec"].append(round(row["Val"],4))
                    elif row["TagIndex"] == 25:
                        vse_vrednosti_dolocenega_recepta["aditivizd"].append(round(row["Val"],4))
        del vse_vrednosti_dolocenega_recepta_list
        vse_vrednosti_dolocenega_recepta_list = list(vse_vrednosti_dolocenega_recepta.values())
        dolzina_lista = 0
        for i in vse_vrednosti_dolocenega_recepta_list[0]:
            dolzina_lista = dolzina_lista + 1

        del new_list
        new_list = [["0" for x in range(len(vse_vrednosti_dolocenega_recepta_list))] for x in range(dolzina_lista)]
        print("_________________________________________________________________________")
        print(vse_vrednosti_dolocenega_recepta_list)
        print(dolzina_lista)
        print(len(vse_vrednosti_dolocenega_recepta_list))
        xx = 0
        yy = 0
        print(new_list)
        for i in vse_vrednosti_dolocenega_recepta_list:
            yy = 0
            for j in i:
                new_list[yy][xx]=j
                yy=yy+1
            xx=xx+1

        print("_________________________________________________________________________")
        print("_________________________________________________________________________")

        window["izracun"].update(values = new_list)

#------------------------------------------------------
#
#------------------------------------------------------

        """elif event == "tfiler":
        try: 
            vrednost = 0
            for index, row in df2.iterrows():
                if row["TagIndex"] == 23:
                    vrednost = vrednost + row["Val"]
                    # print(vrednosti)
            int_vrednost = int(vrednost)
            str_vrednost = str(int_vrednost) + " Kg"
            window["vrednost"].update(value=(str_vrednost))
        except NameError:
            sg.popup("Niste povezani z bazo")

        elif event == "mineralos":
        try:
            vrednost = 0
            for index, row in df2.iterrows():
                if row["TagIndex"] == 22:
                    vrednost = vrednost + row["Val"]
                    # print(vrednosti)
            int_vrednost = int(vrednost)
            str_vrednost = str(int_vrednost) + " Kg"
            window["vrednost"].update(value=(str_vrednost))
        except NameError:
            sg.popup("Niste povezani z bazo")"""

    elif event == sg.WIN_CLOSED:
        break

window.close()
