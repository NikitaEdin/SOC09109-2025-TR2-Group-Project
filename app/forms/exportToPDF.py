from flask import render_template_string
from xhtml2pdf import pisa

import app


def json_to_table(json_data):
    table = "<table class=\"table\">"

    for key in json_data:
        value = json_data[key]

        if isinstance(value, dict):
            value = json_to_table(value)

        table += "<tr><td>" + key + "</td><td>" + value + "</td></tr>"

    table += "</table>"

    return table


def export_form_to_pdf(json_data, destination, name="Document"):
    with app.app.app_context():
        css_file = open("app/static/css/exported_forms.css", "r")
        css_content = css_file.read()
        css_file.close()

        html_content = render_template_string(
            """
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>{{ name }}</title>
                <style>
                    {{ css_content }}
                </style>
            </head>
            <body class="container">
                <h2 class="mt-4 mb-3">{{ name }}</h2>
                
                {{ table|safe }}
            </body>
            </html>
            """,
            table=json_to_table(json_data),
            name=name,
            css_content=css_content
        )

        pisa_status = pisa.CreatePDF(
            html_content,
            dest=destination,
        )

        return pisa_status
