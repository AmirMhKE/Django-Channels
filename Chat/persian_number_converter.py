def convert(ls):
    shapes = {"0": "۰", "1": "۱", "2": "۲", "3": "۳", "4": "۴", "5": "۵",
                "6": "۶", "7": "۷", "8": "۸", "9": "۹"}
    result = ""

    for w in str(ls):
        if shapes.get(w) is not None:
            result += shapes[w]
        else:
            result += w

    return result