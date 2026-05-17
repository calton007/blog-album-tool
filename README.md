# Blog-Albums

这是一个博客相册图片处理工具。

项目主要做两件事：

1. 读取 `photos/` 目录中的原图。
2. 将图片压缩后输出到 `min_photos/`，并根据图片文件名生成相册数据 `data.json`。

## 目录说明

| 路径 | 说明 |
|---|---|
| `photos/` | 原始图片目录 |
| `min_photos/` | 压缩后的图片目录 |
| `tool.py` | 命令行入口 |
| `ImageProcess.py` | 图片处理类 |
| `requirements.txt` | Python 依赖 |

## 图片命名规则

图片文件名需要使用下面格式：

```text
YYYY-MM-DD_图片说明.jpg
```

例如：

```text
2018-03-10_芒果西米露.jpg
```

脚本会从文件名中读取日期和说明文字，用来生成相册数据。

## 运行方式

安装依赖：

```powershell
pip install -r requirements.txt
```

压缩图片：

```powershell
python tool.py compress
```

生成相册数据：

```powershell
python tool.py json
```

压缩图片并生成相册数据：

```powershell
python tool.py all
```

提交并推送到 GitHub：

```powershell
python tool.py publish
```

## 注意事项

`publish` 会执行 `git add`、`git commit` 和 `git push`，会真实提交并推送代码。

`data.json` 是运行生成文件，不提交到仓库。
