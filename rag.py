#from transformers import LlamaForCausalLM, LlamaTokenizer
from llama_cpp import Llama

class RAG:

    def __init__(self):
        self.model_name = \
            "J:\\lm-models\\lmstudio-community\\Meta-Llama-3.1-8B-Instruct-GGUF\\Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
        self.model_name = \
            "J:\\lm-models\\DeepSeek-R1-Distill-Qwen-1.5B-Q2_K.gguf"

        self.set_model(self.model_name)

    def set_model(self):
        self.set_model(self.model_name)

    def set_model(self, model_name):
        self.model_name = model_name
        self.llm = Llama(model_path=self.model_name)
        #self.tokenizer = LlamaTokenizer.from_pretrained(self.model_name)
        #self.model = LlamaForCausalLM.from_pretrained(self.model_name)

    def generate_response(self, prompt, max_length=200):
        #inputs = self.tokenizer(prompt, return_tensors="pt")
        #outputs = self.model.generate(**inputs, max_length=max_length)
        #response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = self.llm(prompt, max_tokens=max_length)
        return str(response["choices"][0]["text"])