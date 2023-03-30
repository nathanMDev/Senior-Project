from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.document_loaders import TextLoader
from langchain.document_loaders import TextLoader
import pinecone
import openai
import json

loader = TextLoader('model/prompts/super_prompt.txt')
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=100)
docs = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings()

# Read the API key and environment from file lines 1 and 2
with open('./key_pinecone.txt') as f:
    api_key = f.readline().strip()
    environment = f.readline().strip()

# initialize pinecone
pinecone.init(
    api_key=api_key,  # find at app.pinecone.io
    environment=environment  # next to api key in console
)

index_name = "ai-langchain"

docsearch = Pinecone.from_documents(docs, embeddings, index_name=index_name)

query = "Kyle: Man I'm out here grinding langchain while your ass is sleeping. You are being a bozo."
docs = docsearch.similarity_search(query)

relevant_doc = docs[0].page_content
print(relevant_doc)

#GPT takes a new message + chat history and turns it into 1 message we'll call this the refined message
#Embedding for this message is created with ada
#Embeddings between this message and current vector database are compared and most relevant chunk is extracted
#The relevant chunk and the refined message are combined so that GPT has all the information needed to respond
#This is how most applications use langchain, but we might have to add another layer
with open('model/history/nathan_history.json') as f:
    history = json.load(f)
agent_history = [x for x in history]

agent_prompt = 'model/prompts/nathan_prompt.txt'
msg = [{'role':'system', 'content': f'{agent_prompt}'}, 
       *agent_history, 
       { "role": "user", "content": 
        f"""As Nathan, you are currently in a conversation with Kyle. 
        Maintain your persona and respond appropriately to his query [{query}]. 
        To assist you in the conversation, you are provided with some information that may be relevant. 
        However, you should only use the information that is relevant to the current conversation and keep your response concise. 
        It is advised that you do not use multiple facts from the document.
        Please see the following document for information:\n\n{relevant_doc}""" }]
response = openai.ChatCompletion.create(messages=msg, model="gpt-3.5-turbo", temperature=0.91, top_p=1, n=1, stream=False, stop= "null", max_tokens=350, presence_penalty=0, frequency_penalty=0)
answer = response["choices"][0]["message"]["content"]
print(answer)