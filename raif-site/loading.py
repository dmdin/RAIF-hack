from lxml import etree
import pandas as pd


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
                result.append((fac_id, int(qid.text), qval.text))
    return result