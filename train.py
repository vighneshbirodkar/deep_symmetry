from __future__ import division, print_function
from external.slim import slim
import tensorflow as tf
from cnnutil import FolderReader
import numpy as np
from commons import get_pbar
from model import inference


SIZE = 32

x_train = tf.placeholder(tf.float32, shape=(None, SIZE, SIZE, 3))
y_train = tf.placeholder(tf.float32, shape=(None, 2))
keep_prob = tf.placeholder(tf.float32, shape=[])


y_pred = inference(x_train, is_training=True)
loss = slim.losses.cross_entropy_loss(y_pred, y_train)
optimize_op = tf.train.AdamOptimizer().minimize(loss)

correct_preds = tf.equal(tf.argmax(y_pred, 1), tf.argmax(y_train, 1))

fr = FolderReader('./samples', 32, 32)

sess = tf.Session()

sess.run(tf.initialize_all_variables())

saver = tf.train.Saver()

for epoch in range(100):
    pbar = get_pbar(fr.get_train_size())
    seen_samples = 0
    correct_samples = 0
    for x_batch, y_batch in fr.get_training_batch(100, transform=False):
        seen_samples += x_batch.shape[0]
        fd = {x_train: x_batch, y_train: y_batch}
        _, preds = sess.run([optimize_op, correct_preds], feed_dict=fd)
        cp = np.sum(preds)
        correct_samples += cp
        pbar.update(seen_samples, Accuracy=100*cp/x_batch.shape[0])

    pbar.finish()
    print('Training Accuracy = %f' %
          (100*float(correct_samples)/float(fr.get_train_size())))
    saver.save(sess, './models/model', global_step=epoch)
