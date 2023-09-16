# Rainbow-Tables-AliyunOSS
使用阿里云OSS作为存储介质的哈希彩虹表生成工具

---

## 文件说明

**警告：当中的某些程序可能存在BUG异常！**

| 源文件名   | 多线程 | 本地留档 | 逐行读取源文件 | 是否存在BUG |
|--------|-----|------|---------|----|
| rt.py  | 是   | 是    | 否       | 无  |
| rt2.py | 否   | 是    | 否       | 无  |
| rt3.py | 是   | 是    | 是       | 可能 |
| rt4.py | 是   | 是    | 是       | 无  | 

**注意：rt.py和rt2.py运行时会将字典文件整个读取到内存中！**

如果字典较大，建议使用**rt4.py**生成彩虹表。

如果字典较小，则可以使用**rt.py**或**rt2.py**生成彩虹表。

---

## 使用教程

> 运行所需第三方库

**注意：需要Python 3才能运行！不支持Python 2！**

```shell
pip3 install oss2
```

---

> 使用前请先编辑python代码文件中的OSS存储信息！否则数据无法正常存储！

```python
# 定义阿里云OSS的配置信息
access_key_id = "<access_key_id>"
access_key_secret = "<access_key_secret>"
bucket_name = "你的bucket名称"
endpoint = "oss-cn-<你的地域>.aliyuncs.com"
```

然后将要生成彩虹表的字典文件重命名为**source.txt**放置在脚本同目录下，运行脚本。

运行时，当前目录可能多出以下文件：

| 文件名        | 目录 | 用途               |
|------------|----|------------------|
| source.txt | 否  | 字典文件             |
| data/      | 是  | 本地留档产生的彩虹表数据目录   |
| progress.txt | 否  | 用于保存读取字典文件的进度的文件 |

**得益于progress.txt文件，生成彩虹表可以随时中断并保存生成进度**

![OSS](docs\images\objects.png)

生成完成后，可在OSS中查看生成的结果。

例如，字典中包含一个字符串"Hello"，则其SHA256值的数据保存位置：

> SHA256/185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969/data.json

_（185f8db32271fe25f561a6fc938b2e264306ec304eda518007d1764826381969是"Hello"的SHA256值）_

data.json内容：

```json
{"data": 
  [
    "Hello"
  ]
}
```

即使发生碰撞，也能有效记录数据值。