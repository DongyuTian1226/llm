from testor import LlmTestor
from utils import createResultDir

def testDemo(savePath: str):
    dataPath = 'data/prompts.xlsx'
    model = 'llama3.1'
    testor = LlmTestor(model=model, data=dataPath, save_dir=savePath,
                       print=True, save_txt=True, save_excel=True)
    testor.run()
    print('结果保存在', savePath)


def testAll(savePath: str):
    dataPath = 'data/prompts.xlsx'
    modelList = ['phi3:14b', 'glm4:latest', 'phi3.5:latest',
                 'llama3-chatqa:latest', 'llama2-chinese:latest',
                 'phi3:latest', 'llava:latest', 'yi:latest',
                 'mistral:latest', 'gemma2:latest',
                 'llama3.1:latest', 'qwen2:latest']     # 
    for model in modelList:
        testor = LlmTestor(model=model, data=dataPath, save_dir=savePath,
                        print=True, save_txt=True, save_excel=True)
        testor.run()
    print('结果保存在', savePath)


if __name__ == '__main__':
    resultDir = createResultDir('data')
    # testDemo(resultDir)
    testAll(resultDir)
