"""
生成应用图标
"""
from PIL import Image, ImageDraw

def create_icon():
    sizes = [16, 32, 48, 64, 128, 256]

    for size in sizes:
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)

        # 绘制蓝色圆形背景
        margin = int(size * 0.06)
        draw.ellipse([margin, margin, size - margin, size - margin],
                    fill=(0, 120, 212, 255))

        # 绘制白色勾 - 根据大小调整
        line_width = max(2, int(size * 0.09))
        points = [
            (int(size * 0.25), int(size * 0.50)),
            (int(size * 0.42), int(size * 0.67)),
            (int(size * 0.75), int(size * 0.28))
        ]
        draw.line(points, fill=(255, 255, 255, 255), width=line_width)

        # 保存不同尺寸的图标
        if size == 64:
            img.save('d:/Nutstore Sync/win project/todo-app/resources/icons/app_icon.png')
        elif size == 32:
            img.save('d:/Nutstore Sync/win project/todo-app/resources/icons/app_icon_32.png')

    print("Icons created!")

if __name__ == "__main__":
    create_icon()