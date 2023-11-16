import fpdf
from datetime import date
import pandas
def naredi_pdf(naslov = " ", vrsta = 1, datum = " ", datumod = " ", datumdo = " ",
               kraj = " ", vrednosti = {}):

    pdf = fpdf.FPDF(orientation="P", unit="mm", format="A4")

    pdf.add_page()

    pdf.set_xy(70, 10)
    pdf.set_font(family="Times", style="B", size=16)
    pdf.cell(w=70, h=10, txt="DELOVNO POROCILO", border=1)

    pdf.set_xy(10, 20)
    pdf.set_font(family="Times", style="B", size=12)
    pdf.multi_cell(w=50, h=6, txt=naslov, border=1)

    kraj_datum = f"{kraj},  {date.today()}"
    pdf.set_xy(150, 20)
    pdf.set_font(family="Times", style="B", size=12)
    pdf.cell(w=50, h=6, txt=kraj_datum, border=1)

    if vrsta == 1:
        datum_izpis = f"Dnevni izpis porabljene mase za dan: {datum}"
        pdf.set_xy(10, 60)
        pdf.set_font(family="Times", style="B", size=12)
        pdf.cell(w=100, h=6, txt=datum_izpis, border=1)


    for y in range(80, 250, 8):
        pdf.line(10, y, 200, y)




    pdf.output(f"Izpis{date.today()}.pdf")

naredi_pdf(naslov="Asfaltna Tehnika\ncesta 123\n123 Krsko\nSlovenija", kraj = "Krsko",
           datum = "2023-01-01",
           vrednosti={"recept":"surf1", "st. sarz":15, "Bitumen":1500})
