import datetime
import math
import plotly.graph_objects as go
import img2pdf
from PIL import Image, ImageDraw, ImageFont

def makeImage():
    now = datetime.datetime.now()
    im = Image.open("components/images/title_img/base.png")
    # 描画準備
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(
        'components/font/HGRSKP.TTF',
        80)
    text = 'POINT RANKING'
    text2 = 'CIRRUS '+now.strftime("%Y%m")

    draw.text(
        (130, 800),
        text2,
        font=font,
        fill='gray',
        stroke_width=2,
        stroke_fill='white')

    im.save("components/images/title_img/title.png")

def write1to3(member):
    im = Image.open("components/images/1-3_img/1-3_base.png")
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(
        'components/font/HGRSKP.TTF',
        70)

    draw.text(
        (180, 100),
        member["名前"][0],
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (180, 210),
        member["名前"][1],
        font=font,
        fill='rgb(199, 199, 199)',
        stroke_width=2,
        stroke_fill='white')
    draw.text(
        (180, 320),
        member["名前"][2],
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')


    draw.text(
        (800, 100),
        str(math.floor(member["エントリ数"][0])),
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (800, 210),
        str(math.floor(member["エントリ数"][1])),
        font=font,
        fill='rgb(199, 199, 199)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (800, 320),
        str(math.floor(member["エントリ数"][2])),
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')


    draw.text(
        (600, 100),
        str(math.floor(member["稼働時間"][0])),
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (600, 210),
        str(math.floor(member["稼働時間"][1])),
        font=font,
        fill='rgb(199, 199, 199)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (600, 320),
        str(math.floor(member["稼働時間"][2])),
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (980, 100),
        str(math.floor(member["1次審査OK"][0])),
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (980, 210),
        str(math.floor(member["1次審査OK"][1])),
        font=font,
        fill='rgb(199, 199, 199)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (980, 320),
        str(math.floor(member["1次審査OK"][2])),
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')



    draw.text(
        (1380, 100),
        str(round(member["1次審査OK平均値"][0],3)),
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (1380, 210),
        str(round(member["1次審査OK平均値"][1],3)),
        font=font,
        fill='rgb(199, 199, 199)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (1380, 320),
        str(round(member["1次審査OK平均値"][2],3)),
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')
    
    draw.text(
        (1147, 100),
        str(round(member["平均値"][0],3)),
        font=font,
        fill='rgb(252, 198, 3)',
        stroke_width=2,
        stroke_fill='white')
    
    draw.text(
        (1147, 210),
        str(round(member["平均値"][1],3)),
        font=font,
        fill='rgb(199,199, 199)',
        stroke_width=2,
        stroke_fill='white')

    draw.text(
        (1147, 320),
        str(round(member["平均値"][2],3)),
        font=font,
        fill='rgb(158, 46, 38)',
        stroke_width=2,
        stroke_fill='white')

    
    im.save('components/images/1-3_img/1-3.png')

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
    im2 = Image.open('components/images/1-3_img/1-3.png')
    get_concat_v_resize(im1, im2, resize_big_image=False).save('pillow_concat_v_resize.jpg')

def head_link_4toend():
    im1 = Image.open('pillow_concat_v_resize.jpg')
    im2 = Image.open('4-end.jpg')
    get_concat_v_resize(im1, im2, resize_big_image=False).save('all.jpg')

def dfPlt(X):
    X = X.drop("1次審査不備",axis=1)
    X = X.drop("index",axis=1)
    X = X.drop("未着手",axis=1)
    X = X.drop("照合なし",axis=1)
    X = X.drop("2次審査待ち",axis=1)
    X = X.drop("取消",axis=1)
    X.insert(0,'index',X.reset_index().index)
    X['index'] = X['index'] + 1
    X = X.round({'平均値': 3})
    X = X.round({'1次審査OK平均値':3})
    fig = go.Figure(
        data=[
            go.Table(
                # ヘッダーとしてDataframeのcolumnsを渡す。
                columnwidth=[115,445,190,193,177,223,223],
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
    image = Image.open('all.jpg')
    pdf_bytes =img2pdf.convert(image.filename)
    file = open('all.pdf',"wb")

    file.write(pdf_bytes)
    image.close()
    file.close()

