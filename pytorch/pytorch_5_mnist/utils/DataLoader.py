#! /bin/python
#用于数据提取
import torchvision.datasets as data_set

mnist_test = data_set.MNIST(root="./mnist/MNIST_train", train=False, dowload=False)
mnist_test = data_set.MNIST(root="./mnist/MNIST_test", train=False, dowload=False)

