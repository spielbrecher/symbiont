#from transformers import LlamaForCausalLM, LlamaTokenizer
from llama_cpp import Llama

class RAG:

    def __init__(self):
        self.model_name = \
            "J:\\lm-models\\lmstudio-community\\Meta-Llama-3.1-8B-Instruct-GGUF\\Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"

        self.set_model(self.model_name)

    def set_model(self):
        self.set_model(self.model_name)

    def set_model2(self, model_name):
        self.model_name = model_name
        self.llm = Llama(model_path=self.model_name)
        #self.tokenizer = LlamaTokenizer.from_pretrained(self.model_name)
        #self.model = LlamaForCausalLM.from_pretrained(self.model_name)

    def set_model(self, model_name):
        self.model_name = model_name
        try:
            self.llm = Llama(
                model_path=self.model_name,
                n_gpu_layers=32,  # Загрузить все слои на GPU
                n_ctx=2048,
                n_batch=512
            )
            print("Model loaded successfully with GPU support.")
        except Exception as e:
            print(f"Failed to load model with GPU support: {e}")
            self.llm = Llama(model_path=self.model_name)  # Попробовать загрузить на CPU

    def generate_response(self, prompt, max_length=200):
        #inputs = self.tokenizer(prompt, return_tensors="pt")
        #outputs = self.model.generate(**inputs, max_length=max_length)
        #response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        response = self.llm(prompt, max_tokens=max_length)
        return str(response["choices"][0]["text"])