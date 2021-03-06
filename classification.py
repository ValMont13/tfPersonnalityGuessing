import tensorflow as tf
import sys

def printPersonality(personalityNumber):
    personalities = [ 'Sportive', 'Geek', 'Artist', 'Nightlife', 'Crazy' ];
    print(personalities[personalityNumber[0]]);

x_data = [
    [2, 0, 3, 1, 4],
    [2, 4, 3, 1, 4],
    [2, 1, 3, 1, 1],
    [0, 1, 2, 2, 3],
    [0, 1, 0, 2, 0],
    [0, 0, 1, 2, 0],
    [1, 2, 2, 4, 1],
    [3, 2, 3, 4, 3],
    [1, 4, 2, 4, 1],
    [4, 4, 1, 0, 3],
    [4, 0, 1, 0, 3],
    [3, 4, 1, 0, 3],
    [3, 3, 4, 3, 2],
    [3, 3, 3, 3, 2],
    [3, 3, 4, 3, 4],
]
# [ 3, 3, 0, 0, 2 ]
# [ 0, 0, 0, 0, 1 ]
y_data = [
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [1, 0, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 0, 0, 0, 1],
]

questionCount = 5
personalities = 5

X = tf.placeholder("float", [None, questionCount])
Y = tf.placeholder("float", [None, personalities])
nb_classes = personalities
W = tf.Variable(tf.random_normal([questionCount, nb_classes]), name="weight")
b = tf.Variable(tf.random_normal([nb_classes]), name="bias")
hypothesis = tf.nn.softmax(tf.matmul(X, W) + b)
cost = tf.reduce_mean(-tf.reduce_sum(Y * tf.log(hypothesis), axis=1))
optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1).minimize(cost)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for step in range(5000):
        sess.run(optimizer, feed_dict={X: x_data, Y: y_data})
        if step % 400 == 0:
            print('Step: ', step, '\nCost: ', sess.run(cost, feed_dict={ X: x_data, Y: y_data }))
    a = sess.run(hypothesis, feed_dict={ X: [[2, 0, 3, 1, 4]]})
    print('\nClassic test:')
    printPersonality(sess.run(tf.argmax(a, 1)))
    b = sess.run(hypothesis, feed_dict={ X: [[0, 1, 0, 2, 0]]})
    print('Classic test:')
    printPersonality(sess.run(tf.argmax(b, 1)))
    c = sess.run(hypothesis, feed_dict={ X: [[1, 2, 2, 4, 1]]})
    print('Classic test:')
    printPersonality(sess.run(tf.argmax(c, 1)))
    #custom
    print('\nSpecial one')
    d = sess.run(hypothesis, feed_dict={ X: [[float(sys.argv[1]), float(sys.argv[2]), float(sys.argv[3]), float(sys.argv[4]), float(sys.argv[5])]]})
    printPersonality(sess.run(tf.argmax(d, 1)))
    print ([v for v in tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)])
    saver = tf.train.Saver([v for v in tf.get_collection(tf.GraphKeys.GLOBAL_VARIABLES)])
    # Use a saver_def to get the "magic" strings to restore
    saver_def = saver.as_saver_def()
    print(saver_def.filename_tensor_name)
    print(saver_def.restore_op_name)

    # write out 3 files 
    saver.save(sess, './trained_model.sd')
    tf.train.write_graph(sess.graph_def, '.', 'trained_model.proto', as_text=False)
    tf.train.write_graph(sess.graph_def, '.', 'trained_model.txt', as_text=True)