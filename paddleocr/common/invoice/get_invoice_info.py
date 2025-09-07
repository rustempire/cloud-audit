import re

from collections import defaultdict


def get_ad_txt(result):
    t_l = []
    if len(result[0]) > 1:
        for t in result[0]:
            if len(t[1][0]) > 1:
                t_l.append(t[1][0].replace(":", "").replace("：", ""))
        return "".join(t_l)
    return None


def get_invoice_name(name):
    n_l = []
    zeng_i = 0
    if "增" in name:
        zeng_i = name.index("增")
        n_l.append(name[:zeng_i])
        n_l.append("增值税")
    if "电" in name[zeng_i:] or "子" in name[zeng_i:]:
        n_l.append("电子")
    if "普" in name[-4:] or "通" in name[-4:]:
        n_l.append("普通")
        n_l.append(name[-2:])
    elif "专" in name[-4:] or "用" in name[-4:]:
        n_l.append("专用")
        n_l.append(name[-2:])
    else:
        n_l.append(name[-4:])

    return "".join(n_l)


class Invoice:
    """
    增值税电子发票结构化识别
    """

    def __init__(self, result, box, filename):
        self.box = box
        self.result = result
        self.res = {"文件名": filename}
        self.name()  # 发票名称
        self.code()  # 发票代码
        self.number()  # 发票号码
        self.date()  # 开票日期
        self.check_code()  # 校验码
        self.no()  # 机器编号
        self.total_price()  # 合计金额
        self.total_taxes()  # 合计税额
        self.amount()  # 价税合计
        self.sellingParties()  # 交易双方信息
        self.commodity()  # 中间部分信息
        self.check_unit_price_num()  # 校验单价和数量

    def name(self):
        """
        发票名称
        """
        name = {"发票名称": ""}
        for r, v in self.result.items():
            k = r.split("卍")[0]
            x_min, y_min, x_max, y_max = self.box["名称"]
            if (x_min < v[0] < x_max) and (y_min < v[1] < y_max):
                res = re.findall('^[\u4e00-\u9fa5]{4,}发票$', k)
                res += re.findall('^[\u4e00-\u9fa5]{4,}票$', k)
                if len(res) > 0:
                    name["发票名称"] = get_invoice_name(res[0])
                    del self.result[r]
                    break
        self.res.update(name)

    def code(self):
        """
        发票代码
        """
        No = {"发票代码": ""}
        for r, v in self.result.items():
            k = r.split("卍")[0]
            x_min, y_min, x_max, y_max = self.box["校验信息"]
            if (x_min < v[0] < x_max) and (y_min < v[1] < y_max):
                res = re.findall(r'(?:代码:|代码：|代码)(\d{12}|\d{10})', k)
                res += re.findall(r'(?:(?<!\d)\d{12}(?!\d))', k)
                res += re.findall(r'(?:(?<!\d)\d{10}(?!\d))', k)
                if len(res) > 0:
                    No['发票代码'] = res[0].replace('代码:', '').replace('代码：', '').replace('代码', '').replace('碗', '税')
                    del self.result[r]
                    break
        self.res.update(No)

    def number(self):
        """
        发票号码
        """
        nu = {"发票号码": ""}
        for r, v in self.result.items():
            k = r.split("卍")[0]
            x_min, y_min, x_max, y_max = self.box["校验信息"]
            if (x_min < v[0] < x_max) and (y_min < v[1] < y_max):
                res = re.findall(r'(?:号码:|号码：|号码)\d{8}', k)
                res += re.findall(r'(?:(?<!\d)\d{8}(?!\d))', k)

                if len(res) > 0:
                    nu["发票号码"] = res[0].replace('号码:', '').replace('号码：', '').replace('号码', '')
                    del self.result[r]
                    break
        self.res.update(nu)

    def date(self):
        """
        开票日期
        """
        da = {"开票日期": ""}
        for r, v in self.result.items():
            k = r.split("卍")[0]
            x_min, y_min, x_max, y_max = self.box["校验信息"]
            if (x_min < v[0] < x_max) and (y_min < v[1] < y_max):
                res = re.findall(r'(?:期:|期：|期)[0-9]{1,4}年[0-9]{1,2}月[0-9]{1,2}日', k)
                res += re.findall(r'(?:期:|期：|期)[0-9]{8}', k)
                res += re.findall(r'[0-9]{1,4}年[0-9]{1,2}月[0-9]{1,2}日', k)
                if len(res) > 0:
                    da["开票日期"] = res[0].replace('期:', '').replace('期：', '').replace('期', '')
                    del self.result[r]
                    break
        self.res.update(da)

    def check_code(self):
        """
        校验码
        """
        check = {'校验码': ""}
        for r, v in self.result.items():
            k = r.split("卍")[0]
            x_min, y_min, x_max, y_max = self.box["校验信息"]
            if (x_min < v[0] < x_max) and (y_min < v[1] < y_max):
                res = re.findall(r'(?:校验码:|校验码：|校验码)[0-9]{20}', k)
                res += re.findall(r'[0-9]{20}', k)
                if len(res) > 0:
                    check['校验码'] = res[0].replace('校验码:', '').replace('校验码：', '').replace('校验码', '')
                    del self.result[r]
                    break
        self.res.update(check)

    def no(self):
        """
        机器编号
        """
        no = {'机器编号': ""}
        for r, v in self.result.items():
            k = r.split("卍")[0]
            x_min, y_min, x_max, y_max = self.box["编号"]
            if (x_min < v[0] < x_max) and (y_min < v[1] < y_max):
                res = re.findall(r'(?:号:|号：|号)[0-9]{1,12}', k)
                res += re.findall('[0-9]{1,12}', k)
                if len(res) > 0:
                    no['机器编号'] = res[0].replace('号:', '').replace('号：', '').replace('号', '')
                    del self.result[r]
                    break
        self.res.update(no)

    def total_price(self):
        """
        合计金额
        """
        price = {"合计金额": ""}
        for r, v in self.result.items():
            k = r.split("卍")[0]
            x_min, y_min, x_max, y_max = self.box["合计金额"]
            if (x_min < v[0] < x_max) and (y_min < v[1] < y_max):
                res = re.findall('￥[0-9]{1,8}.[0-9]{1,2}', k)
                res += re.findall('¥[0-9]{1,8}.[0-9]{1,2}', k)
                res += re.findall('[0-9]{1,8}.[0-9]{1,2}', k)
                if len(res) > 0:
                    price['合计金额'] = res[0].replace('￥', '').replace('¥', '')
                    del self.result[r]
                    break
        self.res.update(price)

    def total_taxes(self):
        """
        合计税额
        """
        taxes = {"合计税额": ""}
        for r, v in self.result.items():
            x_min, y_min, x_max, y_max = self.box["合计税额"]
            k = r.split("卍")[0]
            if (x_min < v[0] < x_max) and (y_min < v[1] < y_max):
                res = re.findall('￥[0-9]{1,8}.[0-9]{1,2}', k)
                res += re.findall('¥[0-9]{1,8}.[0-9]{1,2}', k)
                res += re.findall('[0-9]{1,8}.[0-9]{1,2}', k)
                if len(res) > 0:
                    taxes['合计税额'] = res[0].replace('￥', '').replace('¥', '')
                    del self.result[r]
                    break
        self.res.update(taxes)
        # del self.box["total_taxes"]

    def amount(self):
        """
        价税合计（大小写）
        """
        amount = {"价税合计": ""}
        lu = defaultdict(str)
        i = 0
        res_key = []
        for r, v in self.result.items():
            if i == 2:
                break
            k = r.split("卍")[0]
            x_min, y_min, x_max, y_max = self.box["价税合计"]
            if (x_min < v[0] < x_max) and (y_min < v[1] < y_max) and len(k) > 1:
                upper = re.findall('[壹贰叁肆伍陆柒捌玖拾佰仟万亿圆(元)角分零整]{2,}', k.replace("参", "叁").replace("叁叁", "叁"))
                lower = re.findall('￥[0-9]{1,8}.[0-9]{1,2}', k)
                lower += re.findall('[0-9]{1,8}.[0-9]{1,2}', k)
                if len(lower) > 0:
                    i += 1
                    lu["l"] = lower[0].replace('￥', '')
                    res_key.append(r)
                if len(upper) > 0:
                    i += 1
                    lu["u"] = upper[0]
                    res_key.append(r)
        if lu:
            amount["价税合计"] = "{}（小写）{}".format(lu["u"], lu["l"])
            for r in res_key:
                del self.result[r]
        self.res.update(amount)

    def sellingParties(self):
        for cls in ["购买方", "销售方"]:
            res_key = []
            x_min, y_min, x_max, y_max = self.box[cls]
            y_avg = (y_max - y_min) / 4
            y1, y2, y3 = y_min + y_avg, y_min + 2 * y_avg, y_min + 3 * y_avg
            for r, v in self.result.items():
                k = r.split("卍")[0]
                if x_min < v[0] < x_max and len(k) > 1:
                    if y_min < v[1] < y1:
                        res = re.findall('(?:称:|称：|称)[\u4e00-\u9fa5]{2,}', k)
                        res += re.findall('^[\u4e00-\u9fa5]{2,}', k)
                        if len(res) > 0:
                            name = res[0].replace('称:', '').replace('称：', '').replace('称', '')
                            self.res.update({"{}名称".format(cls): name})
                            res_key.append(r)
                        else:
                            self.res.update({"{}名称".format(cls): ""})

                    elif y1 < v[1] < y2:
                        res = re.findall('(?:号:|号：|号)[0-9A-Z]{20}|[0-9A-Z]{18}|[0-9A-Z]{17}|[0-9A-Z]{15}', k)
                        res += re.findall('^[0-9A-Z]{20}|[0-9A-Z]{18}|[0-9A-Z]{17}|[0-9A-Z]{15}$', k)
                        if len(res) > 0:
                            taxId = res[0].replace('号:', '').replace('号：', '').replace('号', '')
                            self.res.update({"{}纳税人识别号".format(cls): taxId})
                            res_key.append(r)
                        else:
                            self.res.update({"{}纳税人识别号".format(cls): ""})

                    elif y2 < v[1] < y3:
                        res = re.findall(r'((?:话:|话：|话|:|：).*)', k)
                        res += re.findall(
                            r'(.*(?:\d{3}-\d{8}|\d{4}-\d{7}|(?:13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$))',
                            k)
                        if len(res) > 0:
                            addressPhone = res[0].replace('话:', '').replace('话：', '').replace('话', '').replace('：',
                                                                                                               '').replace(
                                ':', '')
                            self.res.update({"{}地址、电话".format(cls): addressPhone})
                            res_key.append(r)
                        else:
                            self.res.update({"{}地址、电话".format(cls): ""})

                    elif y3 < v[1] < y_max:
                        res = re.findall('(?:号:|号：|号)[0-9\u4e00-\u9fa5]{14,}', k)
                        res += re.findall('^[0-9\u4e00-\u9fa5]{14,}', k)
                        if len(res) > 0:
                            bank = res[0].replace('号:', '').replace('号：', '').replace('号', '')
                            self.res.update({"{}开户行及账号".format(cls): bank})
                            res_key.append(r)
                        else:
                            self.res.update({"{}开户行及账号".format(cls): ""})
                    else:
                        continue
        for r in res_key:
            del self.result[r]

    def commodity(self):
        """
        中间部分信息
        """
        for cls in ["货物或应税劳务、服务名称", "规格型号", "单位", "数量", "单价", "金额", "税率", "税额"]:
            x_min, y_min, x_max, y_max = self.box[cls]
            middle_data = {}
            res_key = []
            for r, v in self.result.items():
                k = r.split("卍")[0]
                if (x_min < v[0] < x_max) and (y_min < v[1] < y_max):
                    middle_data[v[1]] = k
                    res_key.append(r)
            if middle_data:
                middle_data = dict(sorted(middle_data.items(), key=lambda x: x[0]))
                if cls in ["单价", "金额", "税额"]:
                    money = []
                    for m in middle_data.values():
                        mn = re.findall(r'\-{0,1}[0-9]*\.[0-9]{2,}', m)
                        if mn:
                            money.append(mn[0])
                    self.res.update({cls: ",".join(money)})
                elif cls == "税率":
                    rate = []
                    for r in middle_data.values():
                        rn = re.findall(r'((?:\d|[1-9]\d|100)(?:.\d{1,3})?%$)', r)
                        if rn:
                            rate.append(rn[0])
                    self.res.update({cls: ",".join(rate)})
                elif cls == "数量":
                    num = []
                    for n in middle_data.values():
                        nn = re.findall(r'(\d+)', n)
                        if nn:
                            num.append(nn[0])
                    self.res.update({cls: ",".join(num)})
                else:
                    self.res.update({cls: "".join(middle_data.values())})
            else:
                self.res.update({cls: ""})
            for r in res_key:
                del self.result[r]

    def check_unit_price_num(self):
        if "," in self.res["金额"]:
            price_l = [float(p) for p in self.res["金额"].split(",")]
            if str(sum(price_l)) in self.res["合计金额"]:
                self.res["数量"] = str("1," * len(price_l))[:-1]

        else:
            if self.res["金额"] in self.res["合计金额"]:
                self.res["单价"] = self.res["金额"]
                if self.res["数量"] == "":
                    self.res["数量"] = "1"

    def check_address_and_phone(self, buyer_ap, seller_ap):
        buyer_ap_txt = get_ad_txt(buyer_ap)
        seller_ap_txt = get_ad_txt(seller_ap)
        if buyer_ap_txt is not None and buyer_ap_txt[-5:] not in self.res["购买方地址、电话"]:
            self.res["购买方地址、电话"] = buyer_ap_txt
        if seller_ap_txt is not None and seller_ap_txt[-5:] not in self.res["销售方地址、电话"]:
            self.res["销售方地址、电话"] = seller_ap_txt
