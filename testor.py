'''定义大模型测试器, 使用指定数据集测试指定大模型'''
import pandas as pd
import os
import json
import yaml
from langchain_ollama import OllamaLLM
from utils import purifyAnswer

class LlmTestor():
    '''大模型测试器'''
    def __init__(self, model: str, data: str, save_dir: str = 'data',
                 base_url: str = 'http://localhost:11434',
                 print: bool = True, save_txt: bool = False,
                 save_excel: bool = False):
        '''初始化测试器

        input
        -----
        model: str, 大模型名称
        data: str, 数据集路径
        base_url: str, ollama大模型服务地址

        properties
        ----------
        model: OllamaLLM, 大模型
        data: list, 测试数据集
        '''
        self.modelName = model.replace(':', '_')
        self.model = OllamaLLM(model=model, base_url=base_url)
        # 数据读取
        problemColumn = '问题'
        df = pd.read_excel(data).dropna(subset=[problemColumn])
        self.data = df[problemColumn].tolist()
        # 属性赋值
        self.print = print
        self.save_txt = save_txt
        self.save_excel = save_excel
        self.txtPath = os.path.join(save_dir, self.modelName + '.txt')
        self.excelPath = os.path.join(save_dir, self.modelName + '.xlsx')
        config = yaml.load(open('config.yml', 'r', encoding='utf-8'), Loader=yaml.FullLoader)
        self.promptPrefix = config['promptPrefix']

    def run(self):
        '''测试大模型'''
        # 读取数据
        for i in range(len(self.data)):
            prompt = self.data[i]
            response = ''
            while response == '':       # 防止空回答
                response = self.model.invoke(self.promptPrefix + prompt)  # 调用大模型
                response = purifyAnswer(response)  # 答案清洗
            # 输出对话
            conversation = f'User: {prompt}\n{self.modelName}: {response}\n' \
                + '-' * 40 + '\n'
            if self.print:      # 打印
                print(conversation)
            if self.save_txt:       # 保存到txt文件
                with open(self.txtPath, 'a', encoding='utf-8') as f:
                    f.write(conversation)
            if self.save_excel:     # 保存到excel文件
                if i == 0:
                    df = pd.DataFrame(columns=['User', self.modelName, '答案'])
                try:
                    responseDict = json.loads(response)
                    df.loc[i] = [prompt, response, responseDict.get('答案', '')]
                except:
                    df.loc[i] = [prompt, response, '回答格式不规范']
        if self.save_excel:
            df.to_excel(self.excelPath, index=False)
