import tensorflow as tf
from tensorflow.keras import layers
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Flatten, BatchNormalization, InputLayer, LSTM, Bidirectional, Reshape
from keras.optimizers import Adam
from keras.utils.vis_utils import plot_model
from keras.callbacks import EarlyStopping, ModelCheckpoint

class get_model():

    def lstm_cell(self, model_name):
        model = Sequential()



        model.add(InputLayer(input_shape=(1, 1)))
        model.add(BatchNormalization())

        model.add(Bidirectional(LSTM(32, return_sequences=True)))
        model.add(Dropout(0.2))

        model.add(Bidirectional(LSTM(32, return_sequences=True)))
        model.add(Dropout(0.2))

        model.add(Bidirectional(LSTM(32, return_sequences=True)))
        model.add(Dropout(0.2))

        model.add(Flatten())

        model.add(Dense(16 , activation='relu'))

        model.add(Dense(1 , activation='relu'))

        model.compile(loss='mean_squared_error', optimizer=Adam(learning_rate=0.1), metrics=['accuracy'])

        model.summary()
        #save_name=model_name+'.png'
        plot_model(model, show_shapes=True, to_file=save_name)

        return model