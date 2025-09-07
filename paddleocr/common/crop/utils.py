import cv2
import numpy as np


# 锐化
def custom_blur_demo(image):
    kernel = np.array([[0, -1, 0], [-1, 7, -1], [0, -1, 0]], np.float32)  # 锐化
    dst = cv2.filter2D(image, -1, kernel=kernel)
    dst = cv2.convertScaleAbs(dst)
    return dst


def prewitt(src):
    prewitt_x = np.array([[-1, 0, 1],
                          [-1, 0, 1],
                          [-1, 0, 1]], dtype=np.float32)
    prewitt_y = np.array([[-1, -1, -1],
                          [0, 0, 0],
                          [1, 1, 1]], dtype=np.float32)

    prewitt_grad_x = cv2.convertScaleAbs(cv2.filter2D(src, cv2.CV_16S, prewitt_x))
    prewitt_grad_y = cv2.convertScaleAbs(cv2.filter2D(src, cv2.CV_16S, prewitt_y))
    return prewitt_grad_x, prewitt_grad_y


def calculate_points(dst):
    point_x = []
    point_y = []

    # 找dst的元素为零的索引（x，y）返回为一个二维列表
    for point in np.argwhere(dst == 0):
        point_x.append(point[1])
        point_y.append(point[0])
    return point_x, point_y


def compare_size(dict_values, num, width):
    for v in dict_values:
        # 最短宽度的点距与宽度的比例是0.02（密码区那两个点最短）
        if abs(v - num) < (0.02 * width):
            return False
    return True


def get_x_point_coordinate(dst, width, height):
    old_y = 0
    n = 0
    y2x = {0: []}
    # 找dst的元素为零的索引（x，y）返回为一个二维列表
    for i, j in np.argwhere(dst == 0):
        if (i - old_y) < (0.03 * height):
            if compare_size(y2x[n], j, width):
                y2x[n].append(int(j))
        else:
            n += 1
            y2x[n] = [int(j)]
        old_y = i

    return y2x


# 查找第三行的x坐标
def length_judgment(y2x_dict):
    if y2x_dict is None:
        return None
    for _, v in y2x_dict.items():
        if len(v) == 9:
            # print(v)
            return v
    return None


def get_address_and_phone_point(point_xy):
    x_min, y_min, x_max, y_max = point_xy
    ap_x_min = int((x_max + 4 * x_min) // 5)
    ap_y_min = int((y_min + y_max) // 2)
    ap_x_max = int(x_max)
    ap_y_max = int((3 * y_max + y_min) // 4)
    return ap_x_min, ap_y_min, ap_x_max, ap_y_max
