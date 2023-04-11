
config = pdfkit.configuration(wkhtmltopdf="/usr/lab/alum/0451778/Descargas/venv/libreria/bin/wkhtmltopdf.exe")

@auth.route("/diploma/<name>/<animal>", methods =['GET','POST'])
def pdf_template(name, animal):
    rendered = render_template("diploma.html", name = name, animal = animal, date = animal)
    pdf = pdfkit.from_string(rendered, output_path = "craftmy.pdf", configuration = config)

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = "inline; filename=output.pdf"  

    return response