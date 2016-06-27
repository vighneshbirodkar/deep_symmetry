from external import slim


def inference(inp, is_training):
    conv1 = slim.ops.conv2d(inp, 32, [5, 5], scope='conv1',
                            is_training=is_training)
    pool1 = slim.ops.max_pool(conv1, [2, 2], 2, scope='pool1')

    conv2 = slim.ops.conv2d(pool1, 64, [5, 5], scope='conv2',
                            is_training=is_training)
    pool2 = slim.ops.max_pool(conv2, [2, 2], 2, scope='pool2')

    flat = slim.ops.flatten(pool2)
    dense = slim.ops.fc(flat, 1024, is_training=is_training)
    dense_dropped = slim.ops.dropout(dense, is_training=is_training)

    y_pred = slim.ops.fc(dense_dropped, 2, activation=None,
                         is_training=is_training)
    return y_pred
