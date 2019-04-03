import  tensorflow as tf
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import  matplotlib.pyplot as plt


class Prediction:
    def __init__(self, dataset):
        self.dataset = dataset
        self.width_data = dataset.shape[0]
        self.height_data = dataset.shape[1]
        self.data = dataset.values

    def initiate_training(self):
        train_start = 0
        train_end = int(np.floor(0.8 * self.width_data))
        test_start = train_end + 1
        test_end = self.width_data

        data_train = self.data[np.arange(train_start, train_end), :]
        data_test = self.data[np.arange(test_start, test_end)]
        Prediction.scale_data(self, data_train, data_test)

    def scale_data(self, data_train, data_test):
        scaler = MinMaxScaler(feature_range=(-1,1))
        scaler.fit(data_train)
        data_train = scaler.transform(data_train)
        data_test = scaler.transform(data_test)

        X_train = data_train[:,1:]
        y_train = data_train[:,0]

        X_test = data_test[:,1:]
        y_test = data_test[:,0]

        Prediction.ml_portion(self, X_test, X_train, y_test, y_train)

    def ml_portion(self, X_test, X_train, y_test, y_train):
        n_stocks = X_train.shape[1]
        num_neurons_1 = 1024
        num_neurons_2 = 512
        num_neurons_3 = 256
        num_neurons_4 = 128

        net = tf.InteractiveSession()
        X = tf.placeholder(dtype=tf.float32, shape=[None, n_stocks])
        Y = tf.placeholder(dtype=tf.float32, shape=[None])

        sigma = 1
        weight_init = tf.variance_scaling_initializer(mode="fan_avg", distribution="uniform", scale=sigma)
        bias_initializer = tf.zeros_initializer()

        W_hidden_1 = tf.Variable(weight_init([n_stocks, num_neurons_1]))
        bias_hidden_1 = tf.Variable(bias_initializer([num_neurons_1]))

        W_hidden_2 = tf.Variable(weight_init([num_neurons_1, num_neurons_2]))
        bias_hidden_2 = tf.Variable(bias_initializer([num_neurons_2]))

        W_hidden_3 = tf.Variable(weight_init([num_neurons_2, num_neurons_3]))
        bias_hidden_3 = tf.Variable(bias_initializer([num_neurons_3]))

        W_hidden_4 = tf.Variable(weight_init([num_neurons_3, num_neurons_4]))
        bias_hidden_4 = tf.Variable(bias_initializer([num_neurons_4]))

        W_out = tf.Variable(weight_init([num_neurons_4, 1]))
        bias_out = tf.Variable(bias_initializer([1]))

        hidden_1 = tf.nn.relu(tf.add(tf.matmul(X, W_hidden_1), bias_hidden_1))
        hidden_2 = tf.nn.relu(tf.add(tf.matmul(hidden_1, W_hidden_2), bias_hidden_2))
        hidden_3 = tf.nn.relu(tf.add(tf.matmul(hidden_2, W_hidden_3), bias_hidden_3))
        hidden_4 = tf.nn.relu(tf.add(tf.matmul(hidden_3, W_hidden_4), bias_hidden_4))

        out = tf.transpose(tf.add(tf.matmul(hidden_4, W_out), bias_out))

        mse = tf.reduce_mean(tf.squared_difference(out, Y))

        optimizer = tf.train.AdamOptimizer().minimize(mse)

        net.run(tf.global_variables_initializer())

        plt.ion()
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        line1, = ax1.plot(y_test)
        line2, = ax1.plot(y_test * 0.5)
        plt.show()

        batch_size = 256
        mse_train = []
        mse_test = []

        epochs = 10
        for e in range(epochs):
            shuffle_ind = np.random.permutation(np.arange(len(y_train)))
            X_train = X_train[shuffle_ind]
            y_train = y_train[shuffle_ind]

            for i in range(0, len(y_train) // batch_size):
                start = i * batch_size
                batch_x = X_train[start:start + batch_size]
                batch_y = y_train[start:start + batch_size]

                net.run(optimizer, feed_dict={X: batch_x, Y:batch_y})

                if np.mod(i, 50) == 0:
                    # MSE train and test
                    mse_train.append(net.run(mse, feed_dict={X: X_train, Y: y_train}))
                    mse_test.append(net.run(mse, feed_dict={X: X_test, Y: y_test}))
                    print('MSE Train: ', mse_train[-1])
                    print('MSE Test: ', mse_test[-1])
                    # Prediction
                    pred = net.run(out, feed_dict={X: X_test})
                    line2.set_ydata(pred)
                    plt.title('Epoch ' + str(e) + ', Batch ' + str(i))
                    plt.pause(.01)
                    plt.show()

        mse_final = net.run(mse, feed_dict={X: X_test, Y: y_test})
        print(mse_final)