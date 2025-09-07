import cv2
import numpy as np

from common.crop.utils import custom_blur_demo, prewitt, length_judgment, calculate_points, get_x_point_coordinate, \
    get_address_and_phone_point


def invoice_box_by_cv(src, enhancement=False):
    if src.ndim == 2:
        gray_src = src
    else:
        gray_src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    gray_src = cv2.bitwise_not(gray_src)
    binary_src = cv2.adaptiveThreshold(gray_src, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 21, -7)
    binary_src = custom_blur_demo(binary_src)
    binary_src = cv2.morphologyEx(binary_src, cv2.MORPH_CLOSE, np.ones((3, 3), np.uint8))
    p_x, p_y = prewitt(binary_src)
    if enhancement:
        p_x = cv2.morphologyEx(p_x, cv2.MORPH_CLOSE, np.ones((4, 4), np.uint8))
        p_y = cv2.morphologyEx(p_y, cv2.MORPH_CLOSE, np.ones((4, 4), np.uint8))

    # 提取水平线
    hline = cv2.getStructuringElement(cv2.MORPH_RECT, (int((src.shape[1] / 20)), 1), (-1, -1))
    # 提取垂直线
    vline = cv2.getStructuringElement(cv2.MORPH_RECT, (1, int((src.shape[0] / 20))), (-1, -1))
    dst_vline = cv2.morphologyEx(p_x, cv2.MORPH_OPEN, vline)
    dst_vline = cv2.bitwise_not(dst_vline)
    dst_hline = cv2.morphologyEx(p_y, cv2.MORPH_OPEN, hline)
    dst_hline = cv2.bitwise_not(dst_hline)

    dst = dst_hline + dst_vline

    point_x, point_y = calculate_points(dst)
    if len(point_x) == 0 or len(point_y) == 0:
        return None, None, None, None
    point_x_max = max(point_x) + 5
    point_y_max = max(point_y) + 5
    point_x_min = min(point_x) - 5
    point_y_min = min(point_y) - 5
    box = (point_x_min, point_y_min, point_x_max, point_y_max)
    w, h = point_x_max - point_x_min, point_y_max - point_y_min
    y2x = get_x_point_coordinate(dst, w, h)
    return w, h, box, y2x


def invoice_module_box(src):
    w, h, box, y2x = invoice_box_by_cv(src)
    if length_judgment(y2x) is None:
        return None, None, None

    (point_x_min, point_y_min, point_x_max, point_y_max) = box
    location_list = sorted(length_judgment(y2x))

    # 发票抬头
    name = (point_x_min + 0.275 * w, point_y_min - 0.26 * h, point_x_min + 0.695 * w, point_y_min - 0.13 * h)

    # 发票校验信息
    check_info = (point_x_min + 0.700 * w, point_y_min - 0.275 * h, point_x_min + 0.972 * w, point_y_min - 0.015 * h)

    # 机器编号
    no = (point_x_min + 5, point_y_min - 0.074 * h, point_x_min + 0.20 * w, point_y_min - 0.016 * h)

    # 购买方的框
    buyer_x_min, buyer_y_min = point_x_min + 0.040 * w, point_y_min
    buyer_x_max, buyer_y_max = point_x_min + 0.575 * w, point_y_min + 0.24 * h
    buyer = (buyer_x_min, buyer_y_min, buyer_x_max, buyer_y_max)
    ap_x_min, ap_y_min, ap_x_max, ap_y_max = get_address_and_phone_point(buyer)
    # print(ap_x_min, ap_y_min, ap_x_max, ap_y_max)
    # cv2.rectangle(src, (ap_x_min, ap_y_min), (ap_x_max, ap_y_max), color=(0, 0, 255), thickness=None, lineType=None, shift=None)
    # cv2.imshow("circle1", src)
    # cv2.waitKey()
    buyer_ap_im = src[ap_y_min:ap_y_max, ap_x_min:ap_x_max]
    # cv2.imshow("im", buyer_ap_im)
    # cv2.waitKey()

    # 货物或服务名称
    commodity = (location_list[0] - 5, point_y_min + 0.278 * h, location_list[1] + 5, point_y_min + 0.65 * h)

    # 规格型号
    specification = (location_list[1] - 5, point_y_min + 0.278 * h, location_list[2] + 5, point_y_min + 0.65 * h)

    # 单位
    unit = (location_list[2] - 5, point_y_min + 0.276 * h, location_list[3] + 5, point_y_min + 0.65 * h)

    # 数量
    number = (location_list[3] - 5, point_y_min + 0.276 * h, location_list[4] + 5, point_y_min + 0.65 * h)
    # cv2.rectangle(src, (int(number[0]), int(number[1])), (int(number[2]), int(number[3])), color=(0, 0, 255), thickness=None, lineType=None, shift=None)
    # cv2.imshow("circle0", src)
    # cv2.waitKey()

    # 单价
    unit_price = (location_list[4] - 5, point_y_min + 0.276 * h, location_list[5] + 5, point_y_min + 0.65 * h)
    # cv2.rectangle(src, (int(unit_price[0]), int(unit_price[1])), (int(unit_price[2]), int(unit_price[3])), color=(0, 0, 255), thickness=None, lineType=None, shift=None)
    # cv2.imshow("circle1", src)
    # cv2.waitKey()

    # 金额
    price = (location_list[5] - 5, point_y_min + 0.276 * h, location_list[6] + 5, point_y_min + 0.65 * h)

    # 税率
    tax_rate = (location_list[6] - 5, point_y_min + 0.276 * h, location_list[7] + 5, point_y_min + 0.65 * h)

    # 税额
    taxes = (location_list[7] - 5, point_y_min + 0.276 * h, point_x_max + 5, point_y_min + 0.65 * h)

    # 合计金额
    total_price = (location_list[5] - 5, point_y_min + 0.610 * h, location_list[6] + 5, point_y_min + 0.705 * h)

    # 合计税额
    total_taxes = (location_list[7] - 5, point_y_min + 0.610 * h, point_x_max + 5, point_y_min + 0.705 * h)

    # 价税合计
    amount = (location_list[1] - 5, point_y_min + 0.690 * h, point_x_min + 0.995 * w, point_y_min + 0.785 * h)

    # 销售方的框
    seller_x_min, seller_y_min = point_x_min + 0.040 * w, point_y_min + 0.77 * h
    seller_x_max, seller_y_max = point_x_min + 0.575 * w, point_y_min + 1 * h
    seller = (seller_x_min, seller_y_min, seller_x_max, seller_y_max)
    ap_x_min, ap_y_min, ap_x_max, ap_y_max = get_address_and_phone_point(seller)
    # cv2.rectangle(src, (int(seller_x_min), int(seller_y_min)), (int(seller_x_max), int(seller_y_max)), color=(0, 0, 255), thickness=None, lineType=None, shift=None)
    # print(ap_x_min, ap_y_min, ap_x_max, ap_y_max)
    # cv2.rectangle(src, (ap_x_min, ap_y_min), (ap_x_max, ap_y_max), color=(0, 0, 255), thickness=None, lineType=None, shift=None)
    # cv2.imshow("circle1", src)
    # cv2.waitKey()
    seller_ap_im = src[ap_y_min:ap_y_max, ap_x_min:ap_x_max]
    # cv2.imshow("im2", seller_ap_im)
    # cv2.waitKey()

    invoice_box_info = {
        "名称": name,
        "校验信息": check_info,
        "编号": no,
        "购买方": buyer,
        "货物或应税劳务、服务名称": commodity,
        "规格型号": specification,
        "单位": unit,
        "数量": number,
        "单价": unit_price,
        "金额": price,
        "税率": tax_rate,
        "税额": taxes,
        "合计金额": total_price,
        "合计税额": total_taxes,
        "价税合计": amount,
        "销售方": seller
    }
    # print(invoice_box_info)
    return invoice_box_info, buyer_ap_im, seller_ap_im


# src = cv2.imread("/Users/cipher/Desktop/3.png")
# invoice_module_box(src)