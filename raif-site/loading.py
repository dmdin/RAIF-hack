from lxml import etree
import pandas as pd
import math


def load_data(filename):
    return pd.read_csv(filename)


def load_root(filename):
    with open(filename, encoding='utf-8') as fobj:
        xml = fobj.read()
    return etree.fromstring(xml.encode('utf-8'))


def get_uniques_id(data, param):
    return list(data[param].unique())


def decrypting_id_factor(root, ask):
    result = []
    for fac in root.getchildren()[1].getchildren()[1].getchildren():
        fac_id = int(fac.attrib['Id_Factor'])
        if fac_id == ask:
            qvalues = fac.getchildren()[2]
            for qv in qvalues:
                qid, qval = qv.getchildren()
                text = qval.text if ask == 3 else qval.text.capitalize()
                result.append((fac_id, int(qid.text), text))
    return sorted(result, key=lambda x: x[2])


def generate_frame(f):
    result = dict()

    if not all(list(map(lambda x: len(x[0]) > 0, f.values()))):
        return pd.DataFrame()
    result['10'] = [float(f['dist1'][0])]
    result['17'] = [float(f['dist2'][0])]
    result['2'] = [float(f['walls1'][0])]
    result['3'] = [float(f['walls2'][0])]
    result['33'] = [float(f['year'][0])]
    result['45'] = [float(f['level'][0])]
    result['5'] = [float(f['districts'][0])]
    result['56'] = [float(f['code'][0])]
    result['7'] = [float(f['area'][0])]

    return pd.DataFrame(result)


def preprocessing(data):
    data = data.copy()
    data["sum1"] = data["17"] + data["7"]
    data["mul2"] = data["7"] * data["5"]
    data['10_sin'] = data['10'].apply(transformation, args=('sin',))
    data['10_cos'] = data['10'].apply(transformation, args=('cos',))
    data['17_sin'] = data['17'].apply(transformation, args=('sin',))
    data['17_cos'] = data['17'].apply(transformation, args=('cos',))
    data['33_sin'] = data['33'].apply(transformation, args=('sin',))
    data['33_cos'] = data['33'].apply(transformation, args=('cos',))
    data['5_sin'] = data['5'].apply(transformation, args=('sin',))
    data['5_cos'] = data['5'].apply(transformation, args=('cos',))
    data['56_sin'] = data['56'].apply(transformation, args=('sin',))
    data['56_cos'] = data['56'].apply(transformation, args=('cos',))
    data['7_sin'] = data['7'].apply(transformation, args=('sin',))

    data['sum1_sin'] = data['sum1'].apply(transformation, args=('sin',))
    data['sum1_cos'] = data['sum1'].apply(transformation, args=('cos',))

    data['mul2_sin'] = data['mul2'].apply(transformation, args=('sin',))
    data['mul2_cos'] = data['mul2'].apply(transformation, args=('cos',))

    data = data.drop(['sum1', 'mul2'], axis=1)

    return data


def transformation(value, transform='square'):
    if transform == 'log':
        return 0 if math.log1p(value) == None else max(0, min(10 ** 3, math.log1p(value)))
    elif transform == 'sqrt':
        return math.sqrt(value + 3.0 / 8)
    elif transform == 'square':
        return value ** 2
    elif transform == 'sin':
        return math.sin(value)
    elif transform == 'cos':
        return math.cos(value)
