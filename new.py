import pandas as pd
import codecs


def another_read_all_data() -> pd:
    '''
    С использованием класса итератора из предыдущей работы записывает обзоры в датафрейм.
    '''
    counter = 0
    rev_types = []
    rev_text = []
    word_num = []
    left = 0
    right = 1658
    mid = 849
    while left < right:
        fl = codecs.open(u'' + "dataset2/new" + str(left).zfill(4) + ".txt", "r", "utf-8")
        txt = fl.read()
        word_num.append(len(txt.split()))
        rev_text.append(txt)
        if left <= 849:
            rev_types.append(1)
        else:
            rev_types.append(0)     
        print()
        left += 1
        fl = codecs.open(u'' + "dataset2/new" + str(right).zfill(4) + ".txt", "r", encoding="utf-8")
        txt = fl.read()
        word_num.append(len(txt.split()))
        rev_text.append(txt)
        if right > 849:
            rev_types.append(0)
        else:
            rev_types.append(1)
        fl.close()
        right -= 1
    dt = pd.DataFrame({"rev_type": rev_types,"rev_text": rev_text, "word_num": word_num})
    return dt