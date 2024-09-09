import os


def createResultDir(dir: str) -> str:
    '''在data文件夹下, 生成conversation1, conversation2, ...等文件夹

    return
    ------
    newDir: str, 新生成的文件夹名称, conversation[X]
    '''
    # 列出data文件夹下所有文件夹
    dataDir = 'data'
    dirs = os.listdir(dataDir)
    conversationDirs = [d for d in dirs if d.startswith('conversation')]
    # 找出最大的conversation文件夹
    maxDir = 'conversation0' if len(conversationDirs) == 0 else \
        max(conversationDirs, key=lambda x: int(x[12:]))
    # 生成新的conversation文件夹
    newDir = f'conversation{int(maxDir[12:]) + 1}'
    dirPath = os.path.join(dataDir, newDir)
    os.mkdir(dirPath)
    return dirPath


def purifyAnswer2Json(answer: str) -> str:
    '''仅保留答案中JSON字符串, 删除其他无效字符'''
    # 找到第一个{和最后一个}的位置
    start = answer.find('{')
    end = answer.rfind('}')
    return answer[start:end + 1]

def purifyChangeLine(answer: str) -> str:
    '''清除回答中的换行符'''
    return answer.replace('/n', '')


def purifyAnswer(answer: str) -> str:
    '''整合多个清洗函数'''
    funcList = [purifyAnswer2Json, purifyChangeLine]
    for func in funcList:
        answer = func(answer)
    return answer
