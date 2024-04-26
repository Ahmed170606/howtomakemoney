from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import json
import random
import os


output_folder = 'INVOICE'
input_folder = 'JSON_IN'
processed_folder = 'JSON_PROCESSED'

for filename in os.listdir(input_folder):
    if filename.endswith('.json'):
        json_file_path = os.path.join(input_folder, filename)
        pdf_filename = os.path.join(output_folder, f"{os.path.splitext(filename)[0]}.pdf")
        processed_json_path = os.path.join(processed_folder, filename)

        with open(json_file_path) as json_file:
            factuur = json.load(json_file)


        factuurcode = str(factuur['order']['ordernummer'])
        factuurdatum = str(factuur['order']['orderdatum'])
        betaaltermijn = str(factuur['order']['betaaltermijn'])
        klant_naam = str(factuur['order']['klant']['naam'])
        klant_adres = str(factuur['order']['klant']['adres'])
        klant_postcode = str(factuur['order']['klant']['postcode'])
        klant_stad = str(factuur['order']['klant']['stad'])
        kvk = str(factuur['order']['klant']['KVK-nummer'])

        c = canvas.Canvas(pdf_filename, pagesize=A4)
        # factuur name/date
        c.setFont("Helvetica-Bold", 29)
        c.drawString(60, 780, "FACTUUR")
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 730, "Factuurnummer:")
        c.drawString(50, 730, "DATUM:")
        c.setFont("Helvetica", 12)
        c.drawString(200, 710, factuurcode)
        c.drawString(50, 710, factuurdatum)

        # bedrijf naam/bank etc
        c.setFont("Helvetica-Bold", 17)
        c.drawString(375, 730, "TechFlow Solutions BV")
        c.setFont("Helvetica-Bold", 10)
        c.drawString(375, 710, "Keizersgracht 123, 1015 CJ")
        c.drawString(375, 690, "Amsterdam")
        c.drawString(375, 670, "+31 (0)20 123 4567")
        c.drawString(375, 650, "TechFlow@hotmail.com")
        c.drawString(375, 630, "KVK: 24598309")
        c.drawString(375, 610, "BTW-code: NL005633771B01")
        c.drawString(375, 590, "Bank: ING Nederland")
        c.drawString(375, 570, "IBAN: NL28 INGB 1234 5678 90")

        # klant info
        c.setFont("Helvetica-Bold", 13)
        c.drawString(50, 590, "FACTUUR AAN:")
        c.setFont("Helvetica", 12)
        c.drawString(50, 570, klant_naam)
        c.drawString(50, 550, klant_stad)
        c.drawString(50, 530, klant_adres)
        c.drawString(50, 510, klant_postcode)
        c.drawString(50, 490, f"KVK: {kvk}")

        c.setFont("Helvetica-Bold", 11)
        c.drawString(50, 446, "VERKOPER")
        random_klant_nr = str(random.randint(1, 4999))
        c.drawString(150, 446, "KLANT NR")
        c.drawString(245, 446, "BETALINGSVOORWAARDEN")
        c.drawString(435, 446, "VERVALDATUM")
        c.setFont("Helvetica", 11)

        c.drawString(52, 430, 'Ahmed/shar')
        c.drawString(152, 430, random_klant_nr)
        c.drawString(247, 430, betaaltermijn)
        c.drawString(437, 430, '-----')
        c.rect(50,440, 95, 20)
        c.rect(145,440, 95, 20)
        c.rect(240,440, 190, 20)
        c.rect(430,440, 110, 20)



        c.rect(50,390, 500,1 )
        c.setFont("Helvetica-Bold", 11)
        c.drawString(55, 400, "AANTAL")
        c.drawString(130, 400, "OMSCHRIJVING")
        c.drawString(260, 400, "PRIJS PER EENHEID")
        c.drawString(400, 400, "REGELTOTAAL")

        y_positie = 345
        totaal_excl_btw = 0
        btw_percentage = 21
        regeltotalen_excl_btw = []
        for product in factuur['order']['producten']:
            productnaam = str(product['productnaam'])
            aantal_product = str(product['aantal'])
            prijs_excl_btw = str(product['prijs_per_stuk_excl_btw'])
            btw = str(product['btw_percentage'])

            c.setFont("Helvetica", 10)
            # aantal product
            c.drawString(55, y_positie, aantal_product)
            # productnaam
            c.drawString(110, y_positie, productnaam)
            #prijs per eenheid
            c.drawString(260, y_positie, prijs_excl_btw)
            #regeltotaal berkenen
            product_totaal = product['aantal'] * product['prijs_per_stuk_excl_btw'] 
            regeltotalen_excl_btw.append(product_totaal)
            # regeltotaal
            c.drawString(400, y_positie, str(product_totaal))
            #btw berekenen  
            y_positie -= 15

        totaal_excl_btw = sum(regeltotalen_excl_btw)
        btw_bedrag = totaal_excl_btw * (btw_percentage / 100)
        # totaal incl btw
        totaal_berekening = totaal_excl_btw + btw_bedrag



        # sub totaal/btw/totaal
        c.rect(390,250, 125, 15)
        c.rect(390,235, 125, 15)
        c.rect(390,220, 125, 15)
        c.drawString(465, 253, f"$ {totaal_excl_btw:.2f}" )
        c.drawString(465, 240, f"${btw_bedrag:.2f}" )
        c.drawString(465, 225, f"$ {totaal_berekening:.2f}")
        c.setFont("Helvetica-Bold", 12)
        c.drawString(332, 253, "Subtotaal")
        c.drawString(365, 240, "Btw")
        c.drawString(350, 225, "Totaal")



        c.drawString(50, 120, "Gelieve u klant- en factuurnummer te vermelden.")
        c.save()

        os.rename(json_file_path, processed_json_path)