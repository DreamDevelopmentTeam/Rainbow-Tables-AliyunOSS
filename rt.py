# 导入所需的模块
import hashlib
import json
import os
import oss2
import threading

# 定义散列函数列表
hash_functions = ["MD5", "SHA1", "SHA256", "SHA384", "SHA512", "SHA3-256", "SHA3-384", "SHA3-512"]

# 定义阿里云OSS的配置信息
access_key_id = "<access_key_id>"
access_key_secret = "<access_key_secret>"
bucket_name = "你的bucket名称"
endpoint = "oss-cn-<你的地域>.aliyuncs.com"

# 创建阿里云OSS的客户端对象
client = oss2.Auth(access_key_id, access_key_secret)
bucket = oss2.Bucket(client, endpoint, bucket_name)

# 定义彩虹表的数据源，可以是任意的字符串列表
# data_source = ["Hello", "World", "Bing", "Python", "Rainbow"]
data_source = []

source_file = "source.txt"
# 检查source.txt文件是否存在，如果不存在则创建
if not os.path.exists(source_file):
    # 使用open函数，以写入模式打开source.txt文件，如果文件不存在，则会自动创建
    with open(source_file, "w") as f:
        # 写入一些初始内容，可以根据需要修改
        f.write("")
# 打开source.txt文件，以只读模式
with open(source_file, "r", encoding="utf-8") as f:
    # 读取文件中的所有内容，并按换行符分割成一个列表
    lines = f.read().split("\n")
    # 遍历列表中的每个字符串
    for line in lines:
        # 如果字符串不为空，也不在data_source中，就将其添加到data_source中
        if line and line not in data_source:
            data_source.append(line)

# 定义彩虹表的保存路径
save_path = "data/"

# 定义彩虹表的生成进度文件名
progress_file = "progress.txt"


# 定义一个函数，用于计算数据的哈希值
def hash_data(data, hash_function):
    # 根据散列函数的名称，选择对应的模块和方法
    if hash_function == "MD5":
        module = hashlib.md5()
    elif hash_function == "SHA1":
        module = hashlib.sha1()
    elif hash_function == "SHA256":
        module = hashlib.sha256()
    elif hash_function == "SHA384":
        module = hashlib.sha384()
    elif hash_function == "SHA512":
        module = hashlib.sha512()
    elif hash_function == "SHA3-256":
        module = hashlib.sha3_256()
    elif hash_function == "SHA3-384":
        module = hashlib.sha3_384()
    elif hash_function == "SHA3-512":
        module = hashlib.sha3_512()
    else:
        return None

    # 将数据编码为字节，并计算哈希值
    data_bytes = data.encode("utf-8")
    module.update(data_bytes)
    hash_value = module.hexdigest()

    return hash_value


# 定义一个函数，用于保存数据和哈希值到本地文件和阿里云OSS中
def save_data(data, hash_value, hash_function):
    # 构造本地文件和阿里云OSS中的路径和文件名
    local_path = save_path + hash_function + "/" + hash_value + "/"
    local_file = local_path + "data.json"
    oss_path = local_path[5:]  # 去掉"data/"前缀
    oss_file = oss_path + "data.json"

    # 创建本地文件夹，如果不存在的话
    if not os.path.exists(local_path):
        os.makedirs(local_path)

    # 读取本地文件中已有的数据列表，如果存在的话
    data_list = []
    if os.path.exists(local_file):
        with open(local_file, "r") as f:
            data_list = json.load(f)["data"]

    # 将新的数据添加到数据列表中，如果不存在重复的话
    if data not in data_list:
        data_list.append(data)

    # 将数据列表转换为JSON格式，并写入本地文件中
    data_json = json.dumps({"data": data_list})
    with open(local_file, "w") as f:
        f.write(data_json)

    # 检查阿里云OSS中是否已经存在相同的哈希值文件，如果不存在，则上传本地文件到阿里云OSS中，覆盖已有的文件，如果存在的话
    if not bucket.object_exists(oss_file):
        bucket.put_object_from_file(oss_file, local_file)


# 定义一个函数，用于读取彩虹表的生成进度，如果存在的话
def read_progress():
    # 初始化进度为0
    progress = 0

    # 如果进度文件存在，则读取其中的数字
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            progress = int(f.read())

    return progress


# 定义一个函数，用于保存彩虹表的生成进度
def save_progress(progress):
    # 将进度转换为字符串，并写入进度文件中
    progress_str = str(progress)
    with open(progress_file, "w") as f:
        f.write(progress_str)


# 定义一个函数，用于处理单个数据和散列函数的组合
def process_data_hash(data, hash_function):
    print("正在处理数据：", data, "和散列函数：", hash_function)

    # 计算数据的哈希值
    hash_value = hash_data(data, hash_function)
    print("哈希值为：", hash_value)

    # 保存数据和哈希值到本地文件和阿里云OSS中
    save_data(data, hash_value, hash_function)
    print("保存成功")


# 开始生成彩虹表
print("开始生成彩虹表...")

# 读取当前的进度
progress = read_progress()

# 遍历数据源中的每个数据
for i in range(progress, len(data_source)):
    data = data_source[i]

    # 创建一个线程列表，用于存储每个散列函数的线程对象
    threads = []

    # 遍历散列函数列表中的每个散列函数
    for hash_function in hash_functions:
        # 创建一个线程对象，传入处理单个数据和散列函数的组合的函数和参数
        thread = threading.Thread(target=process_data_hash, args=(data, hash_function))
        # 将线程对象添加到线程列表中
        threads.append(thread)
        # 启动线程
        thread.start()

    # 等待所有线程结束
    for thread in threads:
        thread.join()

    # 更新进度，并保存到进度文件中
    progress = i + 1
    save_progress(progress)
    print("当前进度为：", progress)

# 完成彩虹表的生成
print("完成彩虹表的生成！")
