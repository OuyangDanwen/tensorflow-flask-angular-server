#!/usr/bin/python

# def predictImage():
# 	predict_command = ["/home/danwen/Work/Server/tensorflow/tensorflow/bazel-bin/tensorflow/examples/label_image/label_image", 
# 	"--output_layer=final_result", 
# 	"--labels=/home/danwen/Work/Server/tensorflow/retrained_model/output_labels.txt", 
# 	"--graph=/home/danwen/Work/Server/tensorflow/retrained_model/output_graph.pb", 
# 	"--image=/home/danwen/Work/Server/file_system/test_image/laptop.jpeg", 
# 	"--input_layer=Mul"]
# 	process = subprocess.Popen(predict_command, stdout=subprocess.PIPE)
# 	out, err = process.communicate()
# 	f = open("predict.txt", "wb")
# 	f.write(out)
# 	f.close()
# 	return out

import numpy as np
import tensorflow as tf
import os

imagePath = '/home/danwen/Work/Server/file_system/test_image/laptop.jpeg'
modelFullPath = '/home/danwen/Work/Server/tensorflow/retrained_model/output_graph.pb'
labelsFullPath = '/home/danwen/Work/Server/tensorflow/retrained_model/output_labels.txt'


def create_graph():
    """Creates a graph from saved GraphDef file and returns a saver."""
    # Creates graph from saved graph_def.pb.
    with tf.gfile.FastGFile(modelFullPath, 'rb') as f:
        graph_def = tf.GraphDef()
        graph_def.ParseFromString(f.read())
        _ = tf.import_graph_def(graph_def, name='')


def predictImage(filename):
    imagePath = filename
    answer = []

    if not tf.gfile.Exists(imagePath):
        tf.logging.fatal('File does not exist %s', imagePath)
        return imagePath

    image_data = tf.gfile.FastGFile(imagePath, 'rb').read()

    # Creates graph from saved GraphDef.
    create_graph()

    with tf.Session() as sess:

        softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
        predictions = sess.run(softmax_tensor,
                               {'DecodeJpeg/contents:0': image_data})
        predictions = np.squeeze(predictions)

        top_k = predictions.argsort()[-5:][::-1]  # Getting top 5 predictions
        f = open(labelsFullPath, 'rb')
        lines = f.readlines()
        labels = [str(w).replace("\n", "") for w in lines]
        for node_id in top_k:
            human_string = labels[node_id]
            score = predictions[node_id]
            print('%s (score = %.5f)' % (human_string, score))
        for index in top_k:
			answer.append(labels[index])
        os.remove(imagePath)
        return answer