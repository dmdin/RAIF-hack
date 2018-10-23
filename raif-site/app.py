from flask import Flask, render_template, request, jsonify
from loading import *

app = Flask(__name__)


def preload(data_filename, xml_filename):
    data = load_data(data_filename)
    root = load_root(xml_filename)
    return decrypting_id_factor(root, 5), decrypting_id_factor(root, 2), decrypting_id_factor(root, 3)


DISTRICTS, WALLS1, WALLS2 = preload('res/merged_data.csv', 'res/FD_GKO_7.xml')


@app.route('/')
def index():
    return render_template('index.html', districts=DISTRICTS, walls_list_1=WALLS1, walls_list_2=WALLS2)


@app.route('/process', methods=['POST'])
def process():
    area = request.form['area']
    level = request.form['level']
    year = request.form['year']
    walls1 = request.form['walls1']
    walls2 = request.form['walls2']
    districts = request.form['districts']

    if area and level and year and districts and walls1 and walls2:
        print(area, level, year, walls1, walls2, districts)
        return jsonify(
            {'area': area, 'level': level, 'year': year, 'walls1': walls1, 'walls2': walls2, 'districts': districts})
    return jsonify({'error': 'Missing Data!'})


if __name__ == '__main__':
    app.run(debug=True)
