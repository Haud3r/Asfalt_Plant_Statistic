import PySimpleGUI as sg

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
header = ["TagName", "TagIndex", "TagType", "TagDataType"]
tagi_table = sg.Table(values=rows, headings=header,
                      auto_size_columns=True, expand_x=True, expand_y=True,
                      justification='center', key="tabela_tagov")

kolendar_od_prikaz = sg.Input(key="kolendar_input_od", enable_events=True)
kolendar_od = sg.CalendarButton("Koledar", pad=None, key="kolendarod", target="kolendar_input_od",
                                font=('MS Sans Serif', 10, 'bold'), format=('%Y-%m-%d 00:00:00'))
kolendar_do_prikaz = sg.Input(key="kolendar_input_do", enable_events=True)
kolendar_do = sg.CalendarButton("Koledar", pad=None, key="kolendardo", format=('%d %B, %Y'),
                                target="kolendar_input_do")
kolendar_layout = [kolendar_od, kolendar_od_prikaz, kolendar_do, kolendar_do_prikaz]

pridobi_podatke = sg.Button("Pokaži podatke", key="podatki")
header2 = ["Datum","ura", "milisekunde", "TagIndex", "Vrednost"]
vrednosti_table = sg.Table(values=rows, headings=header2,
                           auto_size_columns=True, expand_x=True,
                           justification='center', key="tabela_float")
header3 = ["Datum","ura", "milisekunde", "TagIndex", "Vrednost"]
recepti_table = sg.Table(values=rows, headings=header3,
                         auto_size_columns=True, expand_x=True,
                         justification='center', key="tabela_string")

recepti_listbox = sg.Listbox(rows,size=(50, 10), key="recepti",
                             enable_events=True)
progress_bar = sg.ProgressBar(1000, orientation="v", size=(15,20), key="progress")

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

checkbox_frame = sg.Frame("Minerali", [checkbox_layout], key="checkbox_frame")

izbor_elementov_header = ["    Datum    ", " Recept ", "Sarže", "Bitumen Rec", "Bitumen Izd", "L Filer Rec",
                          "L Filer Izd", "T Filer Rec", "T Filer Izd", "Mineral OS Rec",
                          "Mineral OS Izd", "Frezani Rec", "Frezani Izd", "Aditiv Rec", "Aditiv Izd",
                          "K1 Rec", "K1 Izd", "K2 Rec", "K2 Izd", "K3 Rec", "K3 Izd", "K4 Rec", "K4 Izd",
                          "K5 Rec", "K5 Izd", "K6 Rec", "K6 Izd"]

izracun_table = sg.Table(values=rows, headings=izbor_elementov_header,
                         auto_size_columns=True, expand_x=True, num_rows=25, vertical_scroll_only=False,
                         justification='center', key="izracun", visible=False, alternating_row_color="green",
                         max_col_width=20)

layout = [[naslov_text, povezava_text],
          [driver_text, driver_input, server_text, server_input, baza_text, baza_input, connect_button],
          [kolendar_layout],
          [pridobi_podatke],
          [vrednosti_table, recepti_table],
          [recepti_listbox, progress_bar],
          [vrednost_statusbar],
          [checkbox_frame],
          [izracun_table]
          ]
