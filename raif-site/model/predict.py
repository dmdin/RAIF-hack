from keras.models import load_model
from keras import backend
from sklearn.externals import joblib
import tensorflow as tf


def rmse(y_true, y_pred):
    return backend.sqrt(backend.mean(backend.square(y_pred - y_true), axis=-1))


def predict(model, X):
    scalerX = joblib.load('model/scaler.save')
    scalery = joblib.load('model/scalery.save')

    X_scaled = scalerX.transform(X.as_matrix())
    return scalery.inverse_transform(model.predict(X_scaled))[0][0]
