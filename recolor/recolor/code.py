class Deuteranopia:
    def __init__(self, image):
        """
        :param image: Image holder object to perform operations on.
        """
        self._image_to_simulate = image.get_image()
        self._image_to_recolor = image.get_image()
        self.finale = image.get_image()
        self._shape = image.shape()
        self.simulated, self.recolored = True, True

    def simulate(self):
        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                red, green, blue = self._image_to_recolor.item(i, j, 2), self._image_to_recolor.item(i, j, 1), \
                                   self._image_to_recolor.item(i, j, 0)
                self._image_to_simulate.itemset((i, j, 2), 0.625 * red + 0.375 * green)
                self._image_to_simulate.itemset((i, j, 1), 0.7 * red + 0.3 * green)
                self._image_to_simulate.itemset((i, j, 0), 0.3 * green + 0.7 * blue)

        self.simulated = True

        return cv2.cvtColor(self._image_to_simulate, cv2.COLOR_BGR2RGB)

    def recolor(self):
        simulated = self._image_to_simulate if self.simulated else cv2.cvtColor(self.simulate(), cv2.COLOR_RGB2BGR)

        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                red, green, blue = self._image_to_recolor.item(i, j, 2), self._image_to_recolor.item(i, j, 1), \
                                   self._image_to_recolor.item(i, j, 0)

                blue_s, green_s, red_s = simulated.item(i, j, 0), simulated.item(i, j, 1), simulated.item(i, j, 2)

                if all([green > blue + 40, red < green + 40]) or all([0.9 * red > red_s, 0.9 * blue > blue_s,
                                                                      0.9 * green > green_s]):
                    w, a, b, v = radians(abs(blue - blue_s) + abs(green_s - green) + abs(red - red_s)), 0.017, 1.182,\
                                 atan(blue / sqrt(red ** 2 + green ** 2))
                    r = (pi / 2 + v) / 2
                    tg = (w + b) * r * a
                    q0, q1, q2, q3 = 2 * cos(tg / 2), 2 * sin(tg / 2) * cos(radians(red)), \
                        sin(tg / 2) * cos(radians(green)), sin(tg / 2) * cos(radians(blue))

                    _ = (np.matrix([[2 * (q2 ** 2 + q3 ** 2), 2 * (q1 * q2 - q0 * q3), 2 * (q0 * q2 + q1 * q3)],
                                   [0.5 + 2 * (q1 * q2 + q0 * q3), 1 - (2 * (q1 ** 2 + q3 ** 2)),
                                    2 * (q2 * q3 - q0 * q1)],
                                   [0.5 + 2 * (q1 * q3 - q0 * q2), 2 * (q0 * q1 + q2 * q3),
                                    1 - (2 * (q1 ** 2 + q2 ** 2))]]) @
                         np.matrix([red - red_s, green - green_s, blue - blue_s]).T) + np.matrix([red, green, blue]).T

                    self._image_to_recolor.itemset((i, j, 2), abs(_[0][0]))
                    self._image_to_recolor.itemset((i, j, 1), abs(_[1][0]))
                    self._image_to_recolor.itemset((i, j, 0), abs(_[2][0]))

        self.recolored = True

        return cv2.cvtColor(self._image_to_recolor, cv2.COLOR_BGR2RGB)

    def final(self):
        image_to_slaughter = self._image_to_recolor if self.recolored else cv2.cvtColor(self.recolor(),
                                                                                        cv2.COLOR_RGB2BGR)

        for i in range(self._shape[0]):
            for j in range(self._shape[1]):
                red, green, blue = self._image_to_recolor.item(i, j, 2), self._image_to_recolor.item(i, j, 1), \
                                   self._image_to_recolor.item(i, j, 0)

                image_to_slaughter.itemset((i, j, 2), red + -9.65373614e-16 * green + -6.98226199e-16 * blue)
                image_to_slaughter.itemset((i, j, 1), green - 1.57859836e-1 * blue)
                image_to_slaughter.itemset((i, j, 0), -8.88178420e-15 * red + -7.77156117e-16 * blue)
        return cv2.cvtColor(image_to_slaughter, cv2.COLOR_BGR2RGB)










from tools import Image, Deuteranopia
from tools.new_name import newest
from os import getcwd
from os.path import abspath
from matplotlib import use, pyplot as plt


def process(path):
    use('TkAgg')
    if '\\' in path:
        path = path.split('\\')[-1]

    dexter = Deuteranopia(image=Image(file_path=path))

    plt.subplot(221)
    plt.imshow(Image(file_path=path).get_rgb())
    plt.title('Original Image')
    plt.xticks([]), plt.yticks([])

    simulated = dexter.simulate()
    recolored = dexter.recolor()
    simulated_recolored = dexter.final()

    del dexter

    plt.subplot(222)
    plt.imshow(simulated)
    plt.title('Simulated Image')
    plt.xticks([]), plt.yticks([])

    plt.subplot(223)
    plt.imshow(recolored)
    plt.title('Recolored Image')
    plt.xticks([]), plt.yticks([])

    plt.subplot(224)
    plt.imshow(simulated_recolored)
    plt.title('Simulated Recolored Image')
    plt.xticks([]), plt.yticks([])
    _ = newest(path=getcwd() + '\\static\\img\\')
    if not _:
        _ = '0.png'
    else:
        _ = str(int(_[:_.index('.')].split('\\')[-1]) + 1) + '.png'
    plt.savefig(abspath(path=getcwd() + '\\static\\img\\' + _))
