import datetime
import math
import plotly.graph_objects as go
import img2pdf
from PIL import Image, ImageDraw, ImageFont

def write1to3(member):
    im = Image.open("components/images/1-3_img/1-3_real_base.png")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(
        'components/font/HGRSKP.TTF',
        60)

    draw.text(
        (120, 77),
        member["名前"][0],
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (120, 165),
        member["名前"][1],
        font=font,
        fill='rgb(199, 199, 199)',
        stroke_width=2,
        stroke_fill='white')
    draw.text(
        (120, 253),
        member["名前"][2],
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')


    draw.text(
        (500, 77),
        str(math.floor(member["エントリ数"][0])),
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (500, 165),
        str(math.floor(member["エントリ数"][1])),
        font=font,
        fill='rgb(199, 199, 199)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (500, 253),
        str(math.floor(member["エントリ数"][2])),
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (650, 77),
        str(math.floor(member["1次審査OK"][0])),
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (650, 165),
        str(math.floor(member["1次審査OK"][1])),
        font=font,
        fill='rgb(199, 199, 199)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (650, 253),
        str(math.floor(member["1次審査OK"][2])),
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')


    draw.text(
        (790, 77),
        str(math.floor(member["1次審査不備"][0])),
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (790, 165),
        str(math.floor(member["1次審査不備"][1])),
        font=font,
        fill='rgb(199, 199, 199)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (790, 253),
        str(math.floor(member["1次審査不備"][2])),
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')
    
    draw.text(
        (980, 77),
        str(math.floor(member["2次審査待ち"][0])),
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')
    
    draw.text(
        (980, 165),
        str(math.floor(member["2次審査待ち"][1])),
        font=font,
        fill='rgb(199,199, 199)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (980, 253),
        str(math.floor(member["未着手"][2])),
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')
    
    draw.text(
        (1170, 77),
        str(math.floor(member["未着手"][0])),
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')
    
    draw.text(
        (1170, 165),
        str(math.floor(member["未着手"][1])),
        font=font,
        fill='rgb(199,199, 199)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (1170, 253),
        str(math.floor(member["2次審査待ち"][2])),
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')


    
    im.save('components/images/1-3_img/1-3_real.png')

def get_concat_v_resize(im1, im2, resample=Image.BICUBIC, resize_big_image=True):
    if im1.width == im2.width:
        _im1 = im1
        _im2 = im2
    elif (((im1.width > im2.width) and resize_big_image) or
          ((im1.width < im2.width) and not resize_big_image)):
        _im1 = im1.resize((im2.width, int(im1.height * im2.width / im1.width)), resample=resample)
        _im2 = im2
    else:
        _im1 = im1
        _im2 = im2.resize((im1.width, int(im2.height * im1.width / im2.width)), resample=resample)
    dst = Image.new('RGB', (_im1.width, _im1.height + _im2.height))
    dst.paste(_im1, (0, 0))
    dst.paste(_im2, (0, _im1.height))
    return dst

def title_link_1to3():
    im1 = Image.open('components/images/title_img/title.png')
    im2 = Image.open('components/images/1-3_img/1-3_real.png')
    get_concat_v_resize(im1, im2, resize_big_image=False).save('pillow_concat_v_resize.jpg')

def head_link_4toend():
    im1 = Image.open('pillow_concat_v_resize.jpg')
    im2 = Image.open('4-end.jpg')
    get_concat_v_resize(im1, im2, resize_big_image=False).save('all_real.jpg')

def dfPlt(X):
    X = X.drop("平均値",axis=1)
    X = X.drop("稼働時間",axis=1)
    X = X.drop("index",axis=1)
    X = X.drop("照合なし",axis=1)
    X = X.drop("1次審査OK平均値",axis=1)
    X = X.drop("取消",axis=1)
    X.insert(0,'index',X.reset_index().index)
    X['index'] = X['index'] + 1
    fig = go.Figure(
        data=[
            go.Table(
                # ヘッダーとしてDataframeのcolumnsを渡す。
                columnwidth=[95,360,154,140,160,180,182],
                header=dict(
                    values=X.iloc[3,:],
                    line_color='darkslategray',
                    fill_color='white',
                    height=40,
                    font_size=26
                        ),
                # 全て表示するときは、valuesで取得して転置した方がシンプルかも。
                cells=dict(
                    values=X.iloc[4:].values.T,
                    line_color='darkslategray',
                    fill_color='white',
                    height=30,
                    font=dict(family="components/font/Honoka_Shin_Mincho_L.otf",size=16)
                    )
            )
        ]
         )
    
    fig.update_layout(margin=dict(t=0,b=0,l=0,r=0),font=dict(family='HGSeikaishotaiPRO')),

    fig.write_image("4-end.jpg")
    return fig

def imgtopdf():
    image = Image.open('all_real.jpg')
    pdf_bytes =img2pdf.convert(image.filename)
    file = open('all_real.pdf',"wb")

    file.write(pdf_bytes)
    image.close()
    file.close()

