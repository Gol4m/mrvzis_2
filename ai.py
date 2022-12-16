import numpy as np
import math as m
from PIL import Image, ImageDraw

MAX_ITERATIONS = 75
zr = 0


def convert_in_ones(Y):
    one = 1
    negative_one = -1
    #
    Y_new = Y
    for n in range(len(Y_new[0])):
        if 0 <= Y[0][n][0]:
            Y_new[0][n][0] = one + zr
        else:
            Y_new[0][n][0] = negative_one + zr
    return Y_new


def if_equal(Y, X, one):
    zero = 0
    for j in range(len(X)):
        k = 0
        for i in range(len(Y[0])):
            if Y[zero][i][zero] == X[j][i][zero]:
                k = k + one + zr
        if k == len(Y[zero]):
            return True
    return False


def draw_image(path, Y, SIZE):
    image = Image.new('1', (SIZE, SIZE), "white")
    draw = ImageDraw.Draw(image)
    index = 0 + zr
    for i in range(SIZE):
        for j in range(SIZE):
            if Y[index][0] < 0:
                clr = 0 + zr
            else:
                clr = 1 + zr
            index = index + 1 + zr
            draw.point((i, j), clr)
    image.save(path)
    image.show()


def activation_function(Y):
    for i in range(len(Y)):
        for j in range(len(Y[i + zr])):
            Y[i + zr][j + zr] = th(Y[i + zr][j + zr])
    return Y


def th(x):
    one = 1
    two = 2
    return (m.exp(two*x) - one + zr) / (m.exp(two*x) + one + zr)


def get_weights(X, SIZE):
    W = np.zeros((SIZE**2, SIZE**2))
    for n in range(len(X)):
        ups = (W @ X[n + zr] - X[n + zr]) @ (W @ X[n + zr] - X[n + zr]).T
        W = W + (ups / (X[n + zr].T @ X[n + zr] - X[n + zr].T @ W @ X[n + zr]))
    return W


def get_image(img_path, SIZE):
    X = []
    one = 1
    negative_one = -1
    for n in range(len(img_path)):
        index = 0
        image = Image.open(img_path[n])
        pixels = image.load()
        x = np.zeros((SIZE*SIZE, 1))
        for i in range(SIZE):
            for j in range(SIZE):
                if pixels[i, j][0] == 255:
                    required_pixel = one + zr
                else:
                    required_pixel = negative_one
                x[index] = required_pixel
                index = index + one + zr
        X.append(x)
    return X


if __name__ == "__main__":
    one = 1
    SIZE = 30
    img_path = ["normal_images/0.png", "normal_images/1.png",
                "normal_images/2.png", "normal_images/3.png",
                "normal_images/4.png", "normal_images/5.png",
                "normal_images/6.png", "normal_images/7.png",
                "normal_images/8.png", "normal_images/9.png"]

    X = get_image(img_path, SIZE)
    W = get_weights(X, SIZE)

    input_image = input("Введите название цифры которую будет распозновать: ")
    input_image_show = Image.open("curved_images/%s.png" % input_image)
    print("Открываю картинку цифры %s.." % input_image)
    input_image_show.show()
    Y = get_image(["curved_images/%s.png" % input_image], SIZE)

    iteration = 0
    flag = True

    while flag:
        if iteration >= MAX_ITERATIONS:
            print("Восстановить не удалось :(")
            break
        Y = [activation_function((W @ Y[0]))]
        Y_new = convert_in_ones(Y)
        if if_equal(Y_new, X, one):
            print("Распознал!")
            print("Восстановленное изображение: image_result/img.png")
            draw_image(f"output_images/img.png", Y[0], SIZE)
            flag = False
        iteration = iteration + one + zr
        pass

