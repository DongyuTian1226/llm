from langchain_ollama import OllamaLLM


model = OllamaLLM(model='llama3.1', base_url='http://localhost:11434')

response = model.invoke("Hello, how are you?")
print(response)
