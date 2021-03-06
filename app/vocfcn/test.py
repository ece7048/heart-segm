import caffe
from skimage.io import imread
from skimage.color import rgb2gray
from skimage import img_as_float
import matplotlib.pyplot as plt
import numpy as np

model = 'val.prototxt'
#weights = 'fcn16s-heavy-pascal.caffemodel'

weights = 'snapshot/train_iter_1000.caffemodel'

#caffe.set_mode_gpu();
#caffe.set_device(0);

net = caffe.Net(model, weights, caffe.TEST)

def load_image(img_dir, idx):
    im = imread('{}/img/{}.png'.format(img_dir, idx))


    in_ = im#np.array(im, dtype=np.float32)
    #in_ = in_[:, :, 2::-1]
    #in_ -= (104.00699, 116.66877, 122.67892)  # see val.prototxt
    #in_ = in_.transpose((2, 0, 1))
    return in_




def get_output(i):
    image = load_image('../../data/sbdd/dataset', 'img_{}'.format(i))
    res = net.forward()

    score = res['score_output2'].transpose((2, 3, 1, 0))
    label = res['label'].transpose((2, 3, 1, 0))
    print('score shape:', score.shape)
    print('label shape:', label.shape)
    score = score[:, :, :, 0]
    label = label[:, :, 0, 0]
    print(score.shape)
    print(label.shape, label.dtype)

    width = 3
    height = 2

    image = img_as_float(np.reshape(image[:, :, 0], image.shape[:2]))

    plt.subplot(height, width, 1)
    plt.title('target image')
    plt.imshow(image, cmap='gray')
    plt.subplot(height, width, 2)
    plt.title('network output\nlabel 0')
    plt.imshow(score[:, :, 0], cmap='gray')
    plt.subplot(height, width, 3)
    plt.title('network output\nlabel 1')
    plt.imshow(score[:, :, 1], cmap='gray')

    prob_threshold = 0.5
    binary_score = (score[:, :, 1] > prob_threshold).astype(np.float)

    plt.subplot(height, width, 4)
    plt.title('prob > {}'.format(prob_threshold))
    plt.imshow(binary_score, cmap='gray')

    print(image, image.shape)

    plt.subplot(height, width, 5)
    plt.title('image + output')
    plt.imshow(image + binary_score, cmap='gray')

    plt.subplot(height, width, 6)
    plt.title('image + grand truth')
    plt.imshow(image + label, cmap='gray')
    plt.savefig('output/img_{}.png'.format(i), bbox_inches='tight')


for i in range(10):
    get_output(i)
