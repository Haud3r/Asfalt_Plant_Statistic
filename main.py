from copy import deepcopy
import PySimpleGUI as sg
import pyodbc
import pandas as pd
from datetime import date

from layout import izbor_elementov_header, layout

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

window = sg.Window('Statistika 0.1', layout, size=(800, 600), resizable=True, finalize=True)
window.maximize()

prikaz_table = window["izracun"]

povezava_vzpostavljena = 0
podatki_prejeti = 0
vse_vrednosti_receptov_po_receptu = {}
vse_vrednosti_dolocenega_recepta = {}
vse_vrednosti_dolocenega_recepta_list = []
new_list = []
izbira_prikaza_vrstic = 1   #1 = dnevno, 2 = Datumsko od do, 3 = vse
dan_za_prikaz = date.today() #za izbiro 1
dan_od_za_prikaz = ""
dan_do_za_prikaz = ""

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
            #cursor = povezava.cursor()
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

    elif event == "kolendar_dnevno":
        dan_za_prikaz = values["kolendar_dnevno"]
        print(dan_za_prikaz)

    elif event == "kolendar_input_od":
        dan_od_za_prikaz = values["kolendar_input_od"]

    elif event == "kolendar_input_do":
        dan_do_za_prikaz = values["kolendar_input_do"]
#---------------------------------------------------#
#           gumb poberi recepte                     #
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
            if izbira_prikaza_vrstic == 1 and dan_za_prikaz != "":
                for index, row in df3.iterrows():
                    print("dan", dan_za_prikaz)
                    print(row["DateAndTime"].date())
                    if row["Val"] not in recepti and row["DateAndTime"].date().strftime("%Y-%m-%d") == dan_za_prikaz:
                        if row["Val"] != None:
                            recepti.append(row["Val"])
                            #recepti_vsi_podatki.append(row)
            elif izbira_prikaza_vrstic == 2:
                if dan_od_za_prikaz != "" and dan_do_za_prikaz != "":
                    if dan_od_za_prikaz <= dan_do_za_prikaz:
                        for index, row in df3.iterrows():
                            print("dan", dan_za_prikaz)
                            print(row["DateAndTime"].date())
                            if (row["Val"] not in recepti and
                                row["DateAndTime"].date().strftime("%Y-%m-%d") >= dan_od_za_prikaz and
                                row["DateAndTime"].date().strftime("%Y-%m-%d") <= dan_do_za_prikaz):
                                if row["Val"] != None:
                                    recepti.append(row["Val"])
                    else:
                        sg.popup("Datumi se ne ujemajo")
                else:
                    sg.popup("Prosim izberite\ndatume za prikaz")


            elif izbira_prikaza_vrstic == 3:
                for index, row in df3.iterrows():
                    print("dan", dan_za_prikaz)
                    print(row["DateAndTime"].date())
                    if row["Val"] not in recepti:
                        if row["Val"] != None:
                            recepti.append(row["Val"])
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
            if izbira_prikaza_vrstic == 1:
                if row["Val"] == values["recepti"][0] and row["DateAndTime"].date().strftime("%Y-%m-%d") == dan_za_prikaz:
                    vse_vrednosti_receptov_po_receptu["DateAndTime"].append(row["DateAndTime"])
                    print("RECEPT IZBRAN")
                    vse_vrstice = vse_vrstice + 1
            #row["DateAndTime"].date().strftime("%Y-%m-%d") >= dan_od_za_prikaz and
                               # row["DateAndTime"].date().strftime("%Y-%m-%d") <= dan_do_za_prikaz)
            elif izbira_prikaza_vrstic == 2:
                if (row["Val"] == values["recepti"][0] and
                    row["DateAndTime"].date().strftime("%Y-%m-%d") >= dan_od_za_prikaz and
                    row["DateAndTime"].date().strftime("%Y-%m-%d") <= dan_do_za_prikaz):
                    vse_vrednosti_receptov_po_receptu["DateAndTime"].append(row["DateAndTime"])
                    print("RECEPT IZBRAN")
                    vse_vrstice = vse_vrstice + 1

            elif izbira_prikaza_vrstic == 3:
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

                    if row["TagIndex"] == 0:
                        vse_vrednosti_dolocenega_recepta["datum"].append(str(row["DateAndTime"]))
                        vse_vrednosti_dolocenega_recepta["recept"].append(values["recepti"][0])
                        vse_vrednosti_dolocenega_recepta["sarza"].append(row["Val"])
                        print("dodano")
                    elif row["TagIndex"] == 1:
                        vse_vrednosti_dolocenega_recepta["bitumenizd"].append(round(row["Val"],4))
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
            window["izracun"].update(values=new_list)

        #window["izracun"].update(values = new_list)

#------------------------------------------------------
#
#------------------------------------------------------
    elif event == "izborcombo":
        if values["izborcombo"] == "Dnevno":
            izbira_prikaza_vrstic = 1
            window["kolendarod"].update(visible=False)
            window["kolendardo"].update(visible=False)
            window["kolendar_input_od"].update(visible=False)
            window["kolendar_input_do"].update(visible=False)

            window["kolendardnevno"].update(visible=True)
            window["kolendar_dnevno"].update(visible=True)
        elif values["izborcombo"] == "Datumsko":
            izbira_prikaza_vrstic = 2
            window["kolendarod"].update(visible=True)
            window["kolendar_input_od"].update(visible=True)
            window["kolendardo"].update(visible=True)
            window["kolendar_input_do"].update(visible=True)

            window["kolendardnevno"].update(visible=False)
            window["kolendar_dnevno"].update(visible=False)
        elif values["izborcombo"] == "Celoten prikaz":
            izbira_prikaza_vrstic = 3
            window["kolendarod"].update(visible=False)
            window["kolendardo"].update(visible=False)
            window["kolendar_input_od"].update(visible=False)
            window["kolendar_input_do"].update(visible=False)

            window["kolendardnevno"].update(visible=False)
            window["kolendar_dnevno"].update(visible=False)

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
