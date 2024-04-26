from reportlab.pdfgen import canvas


c = canvas.Canvas("hello-world.pdf")
question = input('voer wat in: ')
c.drawString(100,750,question)
c.save()
