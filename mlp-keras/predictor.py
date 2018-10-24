import pandas as pd

from keras.models import Sequential
from keras.layers import Dense, Dropout, LeakyReLU
from keras.wrappers.scikit_learn import KerasRegressor
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from keras import backend
from keras import callbacks
from keras.callbacks import ModelCheckpoint
from keras import optimizers


# Функция потерь (RMSE)
def rmse(y_true, y_pred):
    return backend.sqrt(backend.mean(backend.square(y_pred - y_true), axis=-1))


def keras_model(weights='weights.h5'):
    # Создаем модель
    model = Sequential()
    # Добавляем полносвязные слои, в качестве функции активации - relu
    model.add(Dense(48, input_dim=24, kernel_initializer='normal', activation='relu'))
    model.add(Dense(12, kernel_initializer='normal', activation='relu'))
    model.add(Dense(6, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal', activation='linear'))
    # Если в модель передавались веса - подгружаем
    if weights is not None:
        model.load_weights(weights)
    # Собираем нашу модель, в качестве оптимизации - Adam
    model.compile(loss=rmse, optimizer='adam', metrics=[rmse])
    # Топология: 24 inputs -> [48 -> 24] -> [24 -> 12] -> [12 -> 6] -> 1 output
    return model


model = keras_model()

# Посчитаем RMSE на тестовых данных
model.evaluate(X_test, Y_test)
