from flask import Flask, render_template
import xml.etree.ElementTree as ET

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/consume-panama')
def consume_panama():
    return render_template('data.html', data=get_vaccination_data('PAN'))


@app.route('/consume-mexico')
def consume_mexico():
    return render_template('data.html', data=get_vaccination_data('MEX'))


def get_vaccination_data(country_code):
    tree = ET.parse('templates/API_SH.IMM.MEAS_DS2_en_xml_v2_5381695.xml')
    root = tree.getroot()
    data = []
    for data_node in root.findall("data"):
        for record in data_node.findall("record"):
            for field in record.findall("field"):
                if field.get("key") == country_code:
                    data.append({
                        "Country_or_Area": record.find("field[@name='Country or Area']").text,
                        "Item": record.find("field[@name='Item']").text,
                        "Year": record.find("field[@name='Year']").text,
                        "Value": record.find("field[@name='Value']").text
                    })
    return data


if __name__ == '__main__':
    app.run(debug=True)
