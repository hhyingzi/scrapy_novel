##### 多线程
import threading

datas = []

def process_data(data):
    # 处理单条数据的函数
    pass


def process_data_concurrently(datas):
    threads = []

    # 创建并启动线程
    for data in datas:
        thread = threading.Thread(target=process_data, args=(data,))
        thread.start()
        threads.append(thread)

    # 等待所有线程执行完成
    for thread in threads:
        thread.join()

# 调用函数处理数据
process_data_concurrently(datas)

##### 多进程
import multiprocessing


def process_data_concurrently(datas):
    processes = []

    # 创建并启动进程
    for data in datas:
        process = multiprocessing.Process(target=process_data, args=(data,))
        process.start()
        processes.append(process)

    # 等待所有进程执行完成
    for process in processes:
        process.join()

# 调用函数处理数据
process_data_concurrently(datas)
