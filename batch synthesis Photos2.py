import os
import re
import PIL.Image as Image
from PIL import ImageDraw, ImageFont, ImageOps




def resize_by_width(infile, image_size):
    """按照宽度进行所需比例缩放"""
    im = Image.open(infile)
    (x, y) = im.size
    lv = round(x / image_size, 2) + 0.01
    x_s = int(x // lv)
    y_s = int(y // lv)
    print("x_s", x_s, y_s)
    out = im.resize((x_s, y_s), Image.LANCZOS)

    # 创建一个与原始图像大小相同的空白图像
    blank_image = Image.new("RGB", (x, y), (0, 0, 0))

    # 将原始图像粘贴到空白图像上
    blank_image.paste(out, (0, 0))

    # 在图像上方添加一小块黑色
    pad_height = 150  # 黑色块的高度
    pad_width = int(0.8*x)   # 黑色块的宽度与图像宽度相同
    pad_color = (0, 0, 0)  # 将颜色设置为黑色，RGB值为(0, 0, 0)
    out = ImageOps.pad(blank_image, (pad_width, pad_height + y), method=Image.Resampling.NEAREST, color=pad_color)

    return out


def get_new_img_xy(infile, image_size):
    """返回一个图片的宽、高像素"""
    im = Image.open(infile)
    (x, y) = im.size
    y += 200

    lv = round(x / image_size, 2) + 0.01
    x_s = x // lv
    y_s = y // lv
    # print("x_s", x_s, y_s)
    # out = im.resize((x_s, y_s), Image.ANTIALIAS)
    return x_s, y_s


# 定义图像拼接函数
def image_compose(image_colnum, image_size, image_rownum, image_names, image_save_path, x_new, y_new):
    print(image_names)
    to_image = Image.new('RGB', (image_colnum * x_new, image_rownum * y_new))  # 创建一个新图
    draw = ImageDraw.Draw(to_image)
    fnt = ImageFont.truetype(r'C:\Windows\Fonts\simkai.ttf', 80)
    # 循环遍历，把每张图片按顺序粘贴到对应位置上
    total_num = 0
    for y in range(1, image_rownum + 1):
        for x in range(1, image_colnum + 1):
            from_image = resize_by_width(image_names[image_colnum * (y - 1) + x - 1], image_size)
            to_image.paste(from_image, ((x - 1) * x_new, (y - 1) * y_new))
            print(total_num)
            total_num += 1
            title = image_names[total_num - 1].split('\\')[-1]
            print(title)
            first_underscore_index = title.index("_")
            last_underscore_index = title.rindex("_")
            title = title[first_underscore_index + 1:last_underscore_index]
            print(title)
            # split_index = title.index("热") # 自己设定
            # title1 = title[:split_index+1]
            # title2 = title[split_index+1:]
            # draw.text(((x - 1) * x_new, (y - 1) * y_new), title1, fill="white", font=fnt)
            # draw.text(((x - 1) * x_new, (y - 0.9) * y_new), title2, fill="white", font=fnt) # 这个调整一下
            draw.text(((x - 1) * x_new, (y - 0.9) * y_new), title, fill="white", font=fnt)
            if total_num == len(image_names):
                break
    print(image_save_path)
    return to_image.save(image_save_path)  # 保存新图


def get_image_list_fullpath(dir_path):
    file_name_list = os.listdir(dir_path)
    image_fullpath_list = []
    for file_name_one in file_name_list:
        file_one_path = os.path.join(dir_path, file_name_one)
        if os.path.isfile(file_one_path):
            image_fullpath_list.append(file_one_path)
        else:
            img_path_list = get_image_list_fullpath(file_one_path)
            image_fullpath_list.extend(img_path_list)
    return image_fullpath_list


def merge_images(image_dir_path, image_size, image_colnum):
    # 获取图片集地址下的所有图片名称
    image_fullpath_list = get_image_list_fullpath(image_dir_path)
    def to_mg(weight):  
        if 'mg' in weight:  
            s = weight.split('m')[0]
            print(s)
            return int(s.split('_')[-1])
        return 1e-8  
    image_fullpath_list.sort(key=lambda x:to_mg(x))
    print("image_fullpath_list", len(image_fullpath_list), image_fullpath_list)

    image_save_path = r'{}.png'.format(image_dir_path)  # 图片转换后的地址
    # image_rownum = 4  # 图片间隔，也就是合并成一张图后，一共有几行
    image_rownum_yu = len(image_fullpath_list) % image_colnum
    if image_rownum_yu == 0:
        image_rownum = len(image_fullpath_list) // image_colnum
    else:
        image_rownum = len(image_fullpath_list) // image_colnum + 1

    x_list = []
    y_list = []
    for img_file in image_fullpath_list:
        img_x, img_y = get_new_img_xy(img_file, image_size)
        x_list.append(img_x)
        y_list.append(img_y)

    print("x_list", sorted(x_list))
    print("y_list", sorted(y_list))
    x_new = int(x_list[len(x_list) // 5 * 4])
    y_new = int(y_list[len(y_list) // 5 * 4])
    print(" x_new, y_new", x_new, y_new)
    image_compose(image_colnum, image_size, image_rownum, image_fullpath_list, image_save_path, x_new, y_new)  # 调用函数
    # for img_file in image_fullpath_list:
    #     resize_by_width(img_file,image_size)

image_dir_path = input("图片集地址：") # 图片集地址
image_size = 1080  # 每张小图片的大小
image_colnum = int(input("合并成一张图片后，一行有几个小图：") ) # 合并成一张图后，一行有几个小图


merge_images(image_dir_path, image_size, image_colnum)