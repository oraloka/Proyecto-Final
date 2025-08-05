from flask import render_template, make_response
import pdfkit
import os

def generar_pdf_factura(factura, detalles):
    html = render_template('cliente/factura_pdf.html', factura=factura)
    pdf = pdfkit.from_string(html, False)
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = f'attachment; filename=factura_{factura.id}.pdf'
    return response

# Requiere tener wkhtmltopdf instalado y pdfkit configurado
# Ejemplo de uso en una ruta:
# return generar_pdf_factura(factura, detalles)
