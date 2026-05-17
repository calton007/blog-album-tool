# coding: utf-8
import argparse
import subprocess
from PIL import Image
import json
from datetime import datetime
from pathlib import Path

# 定义压缩比，数值越大，压缩越小
SIZE_normal = 1.0
SIZE_small = 1.5
SIZE_more_small = 2.0
SIZE_more_small_small = 3.0
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".gif"}
DEFAULT_SRC_DIR = Path("photos")
DEFAULT_DES_DIR = Path("min_photos")
DEFAULT_JSON_OUT = Path("data.json")


def make_directory(directory):
    """创建目录"""
    Path(directory).mkdir(parents=True, exist_ok=True)

def directory_exists(directory):
    """判断目录是否存在"""
    return Path(directory).exists()

def list_img_file(directory):
    """列出目录下所有文件，并筛选出图片文件列表返回"""
    path = Path(directory)
    if not path.exists():
        raise FileNotFoundError(f"source directory not exist: {path}")
    return sorted(
        item.name
        for item in path.iterdir()
        if item.is_file() and item.suffix.lower() in IMAGE_EXTENSIONS
    )


def print_help():
    print("""
    This program helps compress many image files
    you can choose which scale you want to compress your img(jpg/png/etc)
    1) normal compress(4M to 1M around)
    2) small compress(4M to 500K around)
    3) smaller compress(4M to 300K around)
    """)

def compress(choose, des_dir, src_dir, file_list):
    """压缩算法，img.thumbnail对图片进行压缩，
    
    参数
    -----------
    choose: str
            选择压缩的比例，有4个选项，越大压缩后的图片越小
    """
    scales = {
        "1": SIZE_normal,
        "2": SIZE_small,
        "3": SIZE_more_small,
        "4": SIZE_more_small_small,
    }
    scale = scales[choose]
    src_dir = Path(src_dir)
    des_dir = Path(des_dir)
    des_dir.mkdir(parents=True, exist_ok=True)
    for infile in file_list:
        with Image.open(src_dir / infile) as img:
            w, h = img.size
            img.thumbnail((int(w / scale), int(h / scale)), Image.Resampling.LANCZOS)
            img.save(des_dir / infile)

def compress_photo(src_dir=DEFAULT_SRC_DIR, des_dir=DEFAULT_DES_DIR, choose="4"):
    '''调用压缩图片的函数
    '''
    src_dir = Path(src_dir)
    des_dir = Path(des_dir)
    file_list_src = list_img_file(src_dir)
    des_dir.mkdir(parents=True, exist_ok=True)
    file_list_des = list_img_file(des_dir)

    '''如果已经压缩了，就不再压缩'''
    pending_files = [filename for filename in file_list_src if filename not in file_list_des]
    compress(choose, des_dir, src_dir, pending_files)
    print(f"compressed {len(pending_files)} image(s)")

def handle_photo(src_dir=DEFAULT_SRC_DIR, output=DEFAULT_JSON_OUT):
    '''根据图片的文件名处理成需要的json格式的数据
    
    -----------
    最后将data.json文件存到博客的source/photos文件夹下
    '''
    src_dir = Path(src_dir)
    output = Path(output)
    file_list = list_img_file(src_dir)
    list_info = []
    for i, filename in enumerate(file_list):
        date_str, info = Path(filename).stem.split("_", 1)
        date = datetime.strptime(date_str, "%Y-%m-%d")
        year_month = date_str[0:7]
        if i == 0:  # 处理第一个文件
            new_dict = {"date": year_month, "arr":{'year': date.year,
                                                                   'month': date.month,
                                                                   'link': [filename],
                                                                   'text': [info],
                                                                   'type': ['image']
                                                                   }
                                        } 
            list_info.append(new_dict)
        elif year_month != list_info[-1]['date']:  # 不是最后的一个日期，就新建一个dict
            new_dict = {"date": year_month, "arr":{'year': date.year,
                                                   'month': date.month,
                                                   'link': [filename],
                                                   'text': [info],
                                                   'type': ['image']
                                                   }
                        }
            list_info.append(new_dict)
        else:  # 同一个日期
            list_info[-1]['arr']['link'].append(filename)
            list_info[-1]['arr']['text'].append(info)
            list_info[-1]['arr']['type'].append('image')
    list_info.reverse()  # 翻转
    final_dict = {"list": list_info}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as fp:
        json.dump(final_dict, fp, ensure_ascii=False, indent=2)
    print(f"wrote {output}")

def cut_photo():
    """裁剪算法
    
    ----------
    调用Graphics类中的裁剪算法，将src_dir目录下的文件进行裁剪（裁剪成正方形）
    """
    print("cut_photo is not implemented")



def git_operation():
    '''
    git 命令行函数，将仓库提交
    
    ----------
    需要安装git命令行工具，并且添加到环境变量中
    '''
    subprocess.run(["git", "add", "--all"], check=True)
    subprocess.run(["git", "commit", "-m", "add photos"], check=True)
    subprocess.run(["git", "push", "origin", "master"], check=True)


def parse_args():
    parser = argparse.ArgumentParser(description="Blog album image utility")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compress_parser = subparsers.add_parser("compress", help="compress photos into min_photos")
    compress_parser.add_argument("--src", default=DEFAULT_SRC_DIR)
    compress_parser.add_argument("--dest", default=DEFAULT_DES_DIR)
    compress_parser.add_argument("--scale", choices=["1", "2", "3", "4"], default="4")

    json_parser = subparsers.add_parser("json", help="generate album data json")
    json_parser.add_argument("--src", default=DEFAULT_SRC_DIR)
    json_parser.add_argument("--output", default=DEFAULT_JSON_OUT)

    all_parser = subparsers.add_parser("all", help="compress photos and generate json")
    all_parser.add_argument("--src", default=DEFAULT_SRC_DIR)
    all_parser.add_argument("--dest", default=DEFAULT_DES_DIR)
    all_parser.add_argument("--output", default=DEFAULT_JSON_OUT)
    all_parser.add_argument("--scale", choices=["1", "2", "3", "4"], default="4")

    subparsers.add_parser("publish", help="git add, commit and push")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.command == "compress":
        compress_photo(args.src, args.dest, args.scale)
    elif args.command == "json":
        handle_photo(args.src, args.output)
    elif args.command == "all":
        compress_photo(args.src, args.dest, args.scale)
        handle_photo(args.src, args.output)
    elif args.command == "publish":
        git_operation()

if __name__ == "__main__":
    main()
