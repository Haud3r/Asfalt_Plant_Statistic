import PySimpleGUI as sg
from datetime import date
#------------------------------#
#      Naslovna vrstica        #
#------------------------------#

naslov_text = sg.Text("Statistika ", size=75)
povezava_text = sg.Text("Povezava ni vzpostavljena", text_color="red",
                        font=("Arial", 15), background_color="White", key="povezava")

#------------------------------#
#      povezava v bazo         #
#------------------------------#
driver_text = sg.Text("Driver:")
driver_input = sg.InputText("SQL Server", size=25, key="driver")
server_text = sg.Text("Server:")
server_input = sg.InputText("DESKTOP-2JDLM40\SQLEXPRESS", size=35, key="server")
baza_text = sg.Text("SQL baza:")
baza_input = sg.InputText("Test_sql_log", size=20, key="baza")
connect_button = sg.Button("Poveži se", key="connect")

#------------------------------#
#      Samo za test            #
#------------------------------#
# kasneje izbriši
rows = []
header = ["TagName", "TagIndex", "TagType", "TagDataType"]
tagi_table = sg.Table(values=rows, headings=header,
                      auto_size_columns=True, expand_x=True, expand_y=True,
                      justification='center', key="tabela_tagov")

#------------------------------#
#      Izbira datuma           #
#------------------------------#
izbor_combo = sg.Combo(["Dnevno", "Datumsko", "Celoten prikaz"], size=(20,3),
                       enable_events=True, key='izborcombo', default_value="Dnevno")

kolendar_od_prikaz = sg.Input(key="kolendar_input_od", enable_events=True, size=20, visible=False)
kolendar_od = sg.CalendarButton("Od", pad=None, key="kolendarod", target="kolendar_input_od",
                                font=('MS Sans Serif', 10, 'bold'), format=('%Y-%m-%d'),
                                visible=False)
kolendar_do_prikaz = sg.Input(key="kolendar_input_do", enable_events=True, size=20,visible=False)
kolendar_do = sg.CalendarButton("Do", pad=None, key="kolendardo", format=('%Y-%m-%d'),
                                target="kolendar_input_do", visible=False)

kolendar_dnevno_prikaz = sg.Input(key="kolendar_dnevno", enable_events=True, size=15, visible=True,
                                  default_text=date.today())
kolendar_dnevno = sg.CalendarButton("Datum", pad=None, key="kolendardnevno", target="kolendar_dnevno",
                                font=('MS Sans Serif', 10, 'bold'), format=('%Y-%m-%d'),
                                visible=True)

pridobi_podatke = sg.Button("Pokaži podatke", key="podatki")


izbira_vnosa_layout = [pridobi_podatke, izbor_combo, kolendar_od, kolendar_od_prikaz, kolendar_do, kolendar_do_prikaz,
                       kolendar_dnevno, kolendar_dnevno_prikaz]

izbira_vnosa_frame = sg.Frame("Izbira vnosa", [izbira_vnosa_layout], key="checkbox_frame")

#----------------------
#      podatki gumb
#----------------------



###############################################

#--------------------
#    izbira recepta
#--------------------
recepti_listbox = sg.Listbox(rows,size=(50, 10), key="recepti",
                             enable_events=True)
progress_bar = sg.ProgressBar(1000, orientation="v", size=(15,20), key="progress")
poberi_vse_button =sg.Button("Vsi recepti", key="poberivse")

dnevno_checkbox = sg.Checkbox("Sarže", key="dnevno", visible=False, enable_events=True, default=True, font=("Arial", 15))
bitumen_checkbox = sg.Checkbox("Bitumen", key="bitumen", visible=False, enable_events=True, default=True, font=("Arial", 15))
frezani_checkbox = sg.Checkbox("Frezani", key="frezani", visible=False, enable_events=True, default=True, font=("Arial", 15))
k1_checkbox = sg.Checkbox("K1", key="k1", visible=False, enable_events=True, default=True, font=("Arial", 15))
k2_checkbox = sg.Checkbox("K2", key="k2", visible=False, enable_events=True, default=True, font=("Arial", 15))
k3_checkbox = sg.Checkbox("K3", key="k3", visible=False, enable_events=True, default=True, font=("Arial", 15))
k4_checkbox = sg.Checkbox("K4", key="k4", visible=False, enable_events=True, default=True, font=("Arial", 15))
k5_checkbox = sg.Checkbox("K5", key="k5", visible=False, enable_events=True, default=True, font=("Arial", 15))
k6_checkbox = sg.Checkbox("K6", key="k6", visible=False, enable_events=True, default=True, font=("Arial", 15))
aditiv_checkbox = sg.Checkbox("Aditiv", key="aditiv", visible=False, enable_events=True, default=True, font=("Arial", 15))
l_filer_checkbox = sg.Checkbox("Lastni filer", key="lfiler", visible=False, enable_events=True, default=True, font=("Arial", 15))
t_filer_checkbox = sg.Checkbox("Tuj filer", key="tfiler", visible=False, enable_events=True, default=True, font=("Arial", 15))
mineral_os_checkbox = sg.Checkbox("Mineral OS", key="mineralos", visible=False, enable_events=True, default=True, font=("Arial", 15))
vrednost_statusbar = sg.StatusBar("0000 KG", key="vrednost", enable_events=True, visible=False, font=("Arial", 15))

checkbox_layout=[dnevno_checkbox, bitumen_checkbox, l_filer_checkbox, t_filer_checkbox,
                 mineral_os_checkbox, frezani_checkbox, aditiv_checkbox, k1_checkbox, k2_checkbox,
                 k3_checkbox, k4_checkbox, k5_checkbox, k6_checkbox]


checkbox_frame = sg.Frame("Minerali", [checkbox_layout], key="checkbox_frame", font=("Arial", 25))

izbor_elementov_header = ["    Datum    ", " Recept ", "Sarže", "Bitumen Rec", "Bitumen Izd", "L Filer Rec",
                          "L Filer Izd", "T Filer Rec", "T Filer Izd", "Mineral OS Rec",
                          "Mineral OS Izd", "Frezani Rec", "Frezani Izd", "Aditiv Rec", "Aditiv Izd",
                          "K1 Rec", "K1 Izd", "K2 Rec", "K2 Izd", "K3 Rec", "K3 Izd", "K4 Rec", "K4 Izd",
                          "K5 Rec", "K5 Izd", "K6 Rec", "K6 Izd"]

izracun_table = sg.Table(values=rows, headings=izbor_elementov_header,
                         auto_size_columns=True, expand_x=True, num_rows=25, vertical_scroll_only=False,
                         justification='center', key="izracun", visible=False, alternating_row_color="green",
                         max_col_width=20)
skupno_izdozirano_text = sg.Text("Skupno izdozirano", text_color="Black",
                        font=("Arial", 20), background_color="LightGrey")
st_sarz_text = sg.Text("Število sarž: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnosarz")
skupno_bitumen_text = sg.Text("Bitumen: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnobitumen")
skupno_lfiler_text = sg.Text("Lastni filer: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnolfiler")
skupno_tfiler_text = sg.Text("Tuj filer: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnotfiler")
skupno_frezani_text = sg.Text("Frezani: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnofrezani")
skupno_aditiv_text = sg.Text("Aditiv: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnoaditiv")
skupno_mineral_text = sg.Text("Obhod sita: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnomineral")
skupno_k1_text = sg.Text("K1: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnok1")
skupno_k2_text = sg.Text("K2: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnok2")
skupno_k3_text = sg.Text("K3: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnok3")
skupno_k4_text = sg.Text("K4: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnok4")
skupno_k5_text = sg.Text("K5: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnok5")
skupno_k6_text = sg.Text("K6: ", text_color="Black",
                        font=("Arial", 15), background_color="LightGrey", key="skupnok6")

skupno_izdozirano_layout = [[skupno_izdozirano_text],[st_sarz_text,skupno_bitumen_text, skupno_lfiler_text,
                            skupno_tfiler_text, skupno_frezani_text, skupno_aditiv_text, skupno_mineral_text],
                            skupno_k1_text, skupno_k2_text, skupno_k3_text, skupno_k4_text, skupno_k5_text, skupno_k6_text]

layout = [[naslov_text, povezava_text],
          [driver_text, driver_input, server_text, server_input, baza_text, baza_input, connect_button],
          [izbira_vnosa_frame],
          [recepti_listbox, progress_bar, poberi_vse_button],
          [vrednost_statusbar],
          [checkbox_frame],
          [izracun_table],
          [skupno_izdozirano_layout]
          ]
