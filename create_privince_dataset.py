import csv

csv_txt_path = "/Users/wangrui/Desktop/全国省市区地址库含邮编.csv"

img_h = 32
img_w = 280
f = open(csv_txt_path, "r")
reader = csv.reader(f)

result = {}
max_text_len = img_w * 2 // img_h

tmp_text = ""
tmp_len = 0
for item in reader:
    # 忽略第一行
    if reader.line_num == 1:
        continue
    text_list = ""

    for ch in str(item[0]).replace("\t", ""):
        text_list += ch
        if ch.isdigit() or ch.isalpha():
            tmp_len += 1
        else:
            tmp_len += 2
        if tmp_len>=max_text_len-2:
            tmp_len = 0
            text_list+=ch
            print(text_list)
            text_list=""




f.close()