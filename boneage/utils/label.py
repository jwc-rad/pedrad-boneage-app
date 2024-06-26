import re

class BoneAgeLabelText(object):
    dict_male = {
        0: "Standard bone age : 3 Months.\nNormal range : -6M",
        1: "Standard bone age : 6 Months.\nNormal range : 2-17M",
        2: "Standard bone age : 9 Months.\nNormal range : 2-17M",
        3: "Standard bone age : 11.5 Months.\nNormal range : 5-18M",
        4: "Standard bone age : 15 Months.\nNormal range : 8-19M",
        5: "Standard bone age : 18 Months.\nNormal range : 9-20M",
        6: "Standard bone age : 21 Months.\nNormal range : 11-27M",
        7: "Standard bone age : 23 Months.\nNormal range : 22-32M",
        8: "Standard bone age : 27 Months.\nNormal range : 22-32M",
        9: "Standard bone age : 30 Months.\nNormal range : 23-38M",
        10: "Standard bone age : 36 Months.\nNormal range : 26-42M",
        11: "Standard bone age : 41 Months.\nNormal range : 38-56M",
        12: "Standard bone age : 48 Months.\nNormal range : 39-60M",
        13: "Standard bone age : 53 Months.\nNormal range : 40-66M",
        14: "Standard bone age : 59 Months.\nNormal range : 44-70M",
        15: "Standard bone age : 66 Months.\nNormal range : 57-75M",
        16: "Standard bone age : 73 Months.\nNormal range : 66-88M",
        17: "Standard bone age : 85 Months.\nNormal range : 75-96M",
        18: "Standard bone age : 96 Months.\nNormal range : 79-115M",
        19: "Standard bone age : 109 Months.\nNormal range : 103-122M",
        20: "Standard bone age : 120 Months.\nNormal range : 106-137M",
        21: "Standard bone age : 131 Months.\nNormal range : 115-143M",
        22: "Standard bone age : 142 Months.\nNormal range : 138-150M",
        23: "Standard bone age : 157 Months.\nNormal range : 151-180M",
        24: "Standard bone age : 170 Months.\nNormal range : 153-186M",
        25: "Standard bone age : 180 Months.\nNormal range : 153M-",
        26: "Standard bone age : 192 Months.\nNormal range : 167M-",
    }

    dict_female = {
        0: "Standard bone age : 2 Months.\nNormal range : -4M",
        1: "Standard bone age : 6 Months.\nNormal range : 2-10M",
        2: "Standard bone age : 9 Months.\nNormal range : 2-10M",
        3: "Standard bone age : 12 Months.\nNormal range : 10-15M",
        4: "Standard bone age : 15 Months.\nNormal range : 11-17M",
        5: "Standard bone age : 18 Months.\nNormal range : 15-27M",
        6: "Standard bone age : 21 Months.\nNormal range : 15-27M",
        7: "Standard bone age : 24 Months.\nNormal range : 15-28M",
        8: "Standard bone age : 27 Months.\nNormal range : 18-35M",
        9: "Standard bone age : 30 Months.\nNormal range : 28-43M",
        10: "Standard bone age : 36 Months.\nNormal range : 29-45M",
        11: "Standard bone age : 41 Months.\nNormal range : 32-49M",
        12: "Standard bone age : 48 Months.\nNormal range : 33-50M",
        13: "Standard bone age : 53 Months.\nNormal range : 40-65M",
        14: "Standard bone age : 60 Months.\nNormal range : 51-75M",
        15: "Standard bone age : 65.5 Months.\nNormal range : 55-77M",
        16: "Standard bone age : 72.5 Months.\nNormal range : 63-87M",
        17: "Standard bone age : 86 Months.\nNormal range : 66-89M",
        18: "Standard bone age : 95 Months.\nNormal range : 81-102M",
        19: "Standard bone age : 108 Months.\nNormal range : 103-124M",
        20: "Standard bone age : 122.5 Months.\nNormal range : 105-126M",
        21: "Standard bone age : 132 Months.\nNormal range : 127-145M",
        22: "Standard bone age : 144 Months.\nNormal range : 139-155M",
        23: "Standard bone age : 157 Months.\nNormal range : 144-169M",
        24: "Standard bone age : 169 Months.\nNormal range : 146-187M",
        25: "Standard bone age : 180 Months.\nNormal range : 161M-",
        26: "Standard bone age : 192 Months.\nNormal range : 161M-",
    }
    
    boneage_male = [float(re.findall(r"\d+[.,]?\d*", x)[0]) for x in dict_male.values()]
    boneage_female = [float(re.findall(r"\d+[.,]?\d*", x)[0]) for x in dict_female.values()]

    def get_labeltext(self, x: int, female: bool, text: bool=True):
        if female:
            if text:
                return self.dict_female[x]
            else:
                return self.boneage_female[x]
        else:
            if text:
                return self.dict_male[x]
            else:
                return self.boneage_male[x]
    
def get_boneage_labeltext(x: int, female: bool, text: bool=True):    
    if female:
        if text:
            return BoneAgeLabelText.dict_female[x]
        else:
            return BoneAgeLabelText.boneage_female[x]
    else:
        if text:
            return BoneAgeLabelText.dict_male[x]
        else:
            return BoneAgeLabelText.boneage_male[x]