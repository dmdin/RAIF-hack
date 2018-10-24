from flask import Flask, render_template, request, jsonify
from loading import *
from raifmodel.predict import *
from keras.models import load_model

app = Flask(__name__)


def preload(data_filename, xml_filename):
    data = load_data(data_filename)
    root = load_root(xml_filename)
    return decrypting_id_factor(root, 5), decrypting_id_factor(root, 2), decrypting_id_factor(root,
                                                                                              3), decrypting_id_factor(
        root, 56)


DISTRICTS, WALLS1, WALLS2, CODE = preload('res/merged_data.csv', 'res/FD_GKO_7.xml')
model = load_model('model/model-best.h5', custom_objects={'rmse': rmse})
# специально, чтобы с фласком не конфликтовал
model._make_predict_function()


@app.route('/')
def index():
    return render_template('index.html', districts=DISTRICTS, walls_list_1=WALLS1, walls_list_2=WALLS2, code=CODE)


@app.route('/process', methods=['POST'])
def process():
    df = generate_frame(dict(request.form))

    if df.empty:
        return jsonify({'error': 'Missing Data!'})
    else:
        data = preprocessing(df)
        result = predict(model, data)

        return jsonify({'predict': str(result)})


@app.route('/mean_cost', methods=['GET', 'POST'])
def mean_cost():
    pass


@app.route('/mean_year', methods=['GET', 'POST'])
def mean_year():
    pass


if __name__ == '__main__':
    app.run(debug=True)
