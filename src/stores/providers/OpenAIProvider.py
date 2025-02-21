from llm.LLMInterface import LLMInterface
from llm.LLMEnums import OpneAIEnums
from openai import OpenAI
import logging

class OpenAIProvider(LLMInterface):
    """
    
    
    """
    def __init__(self, 
                 apit_key: str, api_url: str=None,
                 default_input_max_characters: int=1024,
                 default_generation_max_output_tokens: int=1024,
                 default_generation_teperature: float=0.1):
        """
        
        
        """
        self.apit_key = apit_key
        self.api_url = api_url

        self.default_input_max_characters = default_input_max_characters
        self.default_generation_max_output_tokens = default_generation_max_output_tokens
        self.default_generation_teperature = default_generation_teperature
        
        self.generation_model_id = None

        self.embedding_model_id = None
        self.embedding_size = None

        self.client = OpenAI(
            api_key=self.apit_key,
            api_url=self.api_url
        )

        self.logger = logging.getLogger(__name__)

    def set_generation_model(self, model_id):
        """
        
        
        """
        self.generation_model_id = model_id

    def set_embedding_model(self, model_id: str, embedding_size: int):
        """
        
        """
        self.embedding_model_id = model_id
        self.embedding_size = embedding_size

    def process_text(self, text: str):
        return text[:self.default_input_max_characters].strip()
    


    def generate_text(self, prompt: str, 
                      chat_history: list=[], 
                      max_output_token: int= None, 
                      temperature: float = None):

        if not self.client:
            self.logger.error("OpenAI was not set")
            return None
        
        if not self.generation_model_id:
            self.logger.error("Geneation model for OpenAI was not set")
            return None
        
        max_output_token = max_output_token if max_output_token  else self.default_generation_max_output_tokens
        temperature = temperature if temperature else self.default_generation_teperature

        chat_history.append(self.construct_prompt(prompt=prompt, role=OpneAIEnums.USER.value))

        response = self.client.chat.completions.create(
            model = self.generation_model_id,
            messages= chat_history,
            max_tokens= max_output_token,
            temperature= temperature
        )

        if response or response.choices or len(response.choices) == 0 or response.choices[0].message:
            self.logger.error("Error while generating text with OpenAI")
            return None
        
        return response.choices[0].message


    def embed_text(self, text: str, document_type: str=None):
        
        if not self.client:
            self.logger.error("OpenAI was not set")
            return None
        
        if not self.embedding_model_id:
            self.logger.error("Embedding model for OpenAI was not set")

        response = self.client.embeddings.create(
            model = self.embedding_model_id,
            input = text
        )

        if not response or not response.data or len(response.data) == 0 or not response.data[0].embedding:
            self.logger.error("Error with embedding text with OpenAI")
            return None
        
        return response.data[0].embedding
    
    def construct_prompt(self, prompt: str, role: str):

        return {
            "role": role,
            "content": self.process_text(text=prompt) 
        }