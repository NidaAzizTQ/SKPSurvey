from textwrap import wrap

def wrapit(index):
    labels = list()
    label_ = list(index)
    for l in label_:
        # print(l, "\n")
        labels.append("\n".join(wrap(str(l), 12)))  # for l in label_)]
    return labels