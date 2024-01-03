import os
from chromadb import  Documents, Embeddings
from dotenv import load_dotenv
from openai import OpenAI

from .CustomEmbeddingFunction import CustomEmbeddingFunction
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction as OAIEMbFunc


# load the API key from .env
load_dotenv()

class OpenAIEmbeddingFunction(CustomEmbeddingFunction, OAIEMbFunc):
    def __init__(self,
            model_name:str="text-embedding-ada-002",
            max_token_length:int=8191,
            ):
        
        CustomEmbeddingFunction.__init__(self,
            max_token_length=max_token_length
            )
        
        api_key = os.environ.get("OPENAI_API_KEY", None)
        if api_key is None:
            raise ValueError("Please make sure 'OPENAI_API_KEY' is setup as an environment variable")
        OAIEMbFunc.__init__(self,
            api_key=api_key,
            model_name=model_name
            )
        
        self._model_name = model_name

    def encode_sentences(self, input:Documents) -> Embeddings: 
        return OAIEMbFunc.__call__(self, input)