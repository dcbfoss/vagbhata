#sudo -H pip3 install tensorflow
import pandas as pd
from math import floor
import numpy as np
from tensorflow.keras.models import Sequential, clone_model
from tensorflow.keras.layers import Dropout, Dense, Input, Flatten
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
import keras
data=pd.read_excel('V3_2_ML_input_NO_MAIN_GL.xlsx',sheet_name=['chikitsa','kalpa',
                                              'nidana','shareera'])
dataset_1 = data.get('chikitsa') 
dataset_2 = data.get('kalpa')
dataset_3 = data.get('nidana') 
dataset_4 = data.get('shareera')

dataset_1 = dataset_1.drop(['Text_Type','Book', 'Chapter', 'Window'], axis = 1)
dataset_2 = dataset_2.drop(['Text_Type','Book', 'Chapter', 'Window'], axis = 1)
dataset_3 = dataset_3.drop(['Text_Type','Book', 'Chapter', 'Window'], axis = 1)
dataset_4 = dataset_4.drop(['Text_Type','Book', 'Chapter', 'Window'], axis = 1)

labels_1 = (dataset_1.to_numpy())[:,-1]
labels_2 = (dataset_2.to_numpy())[:,-1]
labels_3 = (dataset_3.to_numpy())[:,-1]
labels_4 = (dataset_4.to_numpy())[:,-1]
scaler = MinMaxScaler()

norm_dataset_1 = pd.DataFrame(scaler.fit_transform(dataset_1.values[:,:-1]), columns=dataset_1.columns[:-1])
norm_dataset_2 = pd.DataFrame(scaler.fit_transform(dataset_2.values[:,:-1]), columns=dataset_2.columns[:-1])
norm_dataset_3 = pd.DataFrame(scaler.fit_transform(dataset_3.values[:,:-1]), columns=dataset_3.columns[:-1])
norm_dataset_4 = pd.DataFrame(scaler.fit_transform(dataset_4.values[:,:-1]), columns=dataset_4.columns[:-1])

feature_data_1 = norm_dataset_1.to_numpy()
feature_data_2 = norm_dataset_2.to_numpy()
feature_data_3 = norm_dataset_3.to_numpy()
feature_data_4 = norm_dataset_4.to_numpy()

train_size = round(len(feature_data_1) * 0.7) + 1
x_train1, y_train1 = feature_data_1[:train_size], labels_1[:train_size] 
x_test1, y_test1 = feature_data_1[train_size:], labels_1[train_size:]

train_size = round(len(feature_data_2) * 0.7) + 1
x_train2, y_train2 = feature_data_2[:train_size], labels_2[:train_size] 
x_test2, y_test2 = feature_data_2[train_size:], labels_2[train_size:]

train_size = round(len(feature_data_3) * 0.7) + 1
x_train3, y_train3 = feature_data_3[:train_size], labels_3[:train_size] 
x_test3, y_test3 = feature_data_3[train_size:], labels_3[train_size:]

train_size = round(len(feature_data_4) * 0.7) + 1
x_train4, y_train4 = feature_data_4[:train_size], labels_4[:train_size] 
x_test4, y_test4 = feature_data_4[train_size:], labels_4[train_size:]
'''
model = Sequential()
model.add(Input(shape = (14, )))
model.add(Dense(14, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(28, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(56, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(28, activation='relu'))
model.add(Dropout(0.2))
model.add(Dense(14, activation= 'relu'))
model.add(Dropout(0.2))
model.add(Dense(1, activation='sigmoid'))
'''
'''
model = Sequential()
model.add(Input(shape = (14, )))
model.add(Dense(14,activation='sigmoid',use_bias=True))
model.add(Dense(28, activation='softmax',use_bias=True))
model.add(Dense(14, activation='sigmoid',use_bias=True))
model.add(Dropout(0.1))
model.add(Dense(1, activation='sigmoid',use_bias=False))


'''
model = Sequential()
model.add(Input(shape = (14, )))
model.add(Dense(14,activation='sigmoid',use_bias=True))
model.add(Dense(28, activation='softmax',use_bias=True))
model.add(Dropout(0.1))
model.add(Dense(14, activation='sigmoid',use_bias=True))
model.add(Dense(1, activation='tanh',use_bias=False))

model2 = clone_model(model)
model3 = clone_model(model)
model4 = clone_model(model)
models = [model, model2, model3, model4]

opt = keras.optimizers.Adam(learning_rate=0.01)
for m in models:
    m.compile(optimizer=opt, loss='binary_crossentropy', metrics = ['accuracy'])

callback = tf.keras.callbacks.EarlyStopping(monitor='loss')

model.fit(x_train1,y_train1,callbacks=[callback], epochs=1000)
model2.fit(x_train2, y_train2,callbacks=[callback], epochs=1000)
model3.fit(x_train3, y_train3,callbacks=[callback], epochs=1000)
model4.fit(x_train4, y_train4,callbacks=[callback], epochs=1000)



print("Evaluated=",model.evaluate(x_test1, y_test1))
print("Evaluated=",model2.evaluate(x_test2, y_test2))
print("Evaluated=",model3.evaluate(x_test3, y_test3))
print("Evaluated=",model4.evaluate(x_test4, y_test4))

tf.keras.utils.plot_model(model, show_shapes=True)
