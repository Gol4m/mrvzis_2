import numpy as np
import math as m
from PIL import Image, ImageDraw

MAX_ITERATIONS = 75


def convert_in_ones(Y):
    #
    Y_new = Y
    for n in range(len(Y_new[0])):
        if 0 <= Y[0][n][0]:
            Y_new[0][n][0] = 1
        else:
            Y_new[0][n][0] = -1
    return Y_new


def if_equal(Y, X):
    for j in range(len(X)):
        k = 0
        for i in range(len(Y[0])):
            if Y[0][i][0] == X[j][i][0]:
                k = k + 1
        if k == len(Y[0]):
            return True
    return False


def draw_image(path, Y, SIZE):
    image = Image.new('1', (SIZE, SIZE), "white")
    draw = ImageDraw.Draw(image)
    index = 0
    for i in range(SIZE):
        for j in range(SIZE):
            if Y[index][0] < 0:
                clr = 0
            else:
                clr = 1
            index = index + 1
            draw.point((i, j), clr)
    image.save(path)
    image.show()


def activation_function(Y):
    for i in range(len(Y)):
        for j in range(len(Y[i])):
            Y[i][j] = th(Y[i][j])
    return Y


def sh(x):
    return m.exp(x) - m.exp(-x)


def ch(x):
    return m.exp(x) + m.exp(-x)


def th(x):
    return sh(x) / ch(x)


def transparent(X):
    return X.T


def get_weights(X, SIZE):
    W = np.zeros((SIZE**2, SIZE**2))
    for n in range(len(X)):
        ups = (W @ X[n] - X[n]) @ transparent(W @ X[n] - X[n])
        W = W + (ups / (transparent(X[n]) @ X[n] - transparent(X[n]) @ W @ X[n]))
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
                    required_pixel = one
                else:
                    required_pixel = negative_one
                x[index] = required_pixel
                index = index + one
        X.append(x)
    return X


def get_image_and_weights(img_path, SIZE):
    X = get_image(img_path, SIZE)
    W = get_weights(X, SIZE)
    return X, W


def while_cycle(X, W, SIZE):
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
        if if_equal(Y_new, X):
            print("Распознал!")
            print("Восстановленное изображение: image_result/img.png")
            draw_image(f"output_images/img.png", Y[0], SIZE)
            flag = False
        iteration = iteration + 1
        pass


def main():
    SIZE = 30
    img_path = ["normal_images/0.png", "normal_images/1.png",
                "normal_images/2.png", "normal_images/3.png",
                "normal_images/4.png", "normal_images/5.png",
                "normal_images/6.png", "normal_images/7.png",
                "normal_images/8.png", "normal_images/9.png"]

    X, W = get_image_and_weights(img_path, SIZE)

    while_cycle(X, W, SIZE)


if __name__ == "__main__":
    main()

