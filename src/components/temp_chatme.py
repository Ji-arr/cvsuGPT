# import os
# import sys

# import openai
# import constant
# from langchain.document_loaders import TextLoader
# from langchain.indexes import VectorstoreIndexCreator

# os.environ["OPENAI_API_KEY"] = constant.APIKEY

# query = sys.argv[1]
# print(query)

# loader = TextLoader('data.txt')
# index = VectorstoreIndexCreator().from_loaders([loader])

# print(index.query(query))

# import requests

# url = "https://api.openai.com/v1/chat/completions"
# headers = {
#     "Content-Type": "application/json",
#     "Authorization": f"Bearer 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"
# }

# data = {
#     "model": "gpt-3.5-turbo",
#     "messages": [{"role": "user", "content": "Say this is a test!"}],
#     "temperature": 0.7
# }

# response = requests.post(url, headers=headers, json=data)

# # Print the response
# print(response.json())


import os
import sys

import openai
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma

import constant

os.environ["OPENAI_API_KEY"] = constant.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

query = None
if len(sys.argv) > 1:
  query = sys.argv[1]

if PERSIST and os.path.exists("persist"):
  print("Reusing index...\n")
  vectorstore = Chroma(persist_directory="persist", embedding_function=OpenAIEmbeddings())
  index = VectorStoreIndexWrapper(vectorstore=vectorstore)
else:
  loader = TextLoader("data/data2.txt", encoding = 'UTF-8') # Use this line if you only need data.txt
  #loader = DirectoryLoader("data/")
  if PERSIST:
    index = VectorstoreIndexCreator(vectorstore_kwargs={"persist_directory":"persist"}).from_loaders([loader])
  else:
    index = VectorstoreIndexCreator().from_loaders([loader])

chain = ConversationalRetrievalChain.from_llm(
  llm=ChatOpenAI(model="gpt-3.5-turbo"),
  retriever=index.vectorstore.as_retriever(search_kwargs={"k": 1}),
)

chat_history = []
while True:
  if not query:
    query = input("Prompt: ")
  if query in ['quit', 'q', 'exit']:
    sys.exit()
  result = chain({"question": query, "chat_history": chat_history})
  print(result['answer'])

  chat_history.append((query, result['answer']))
  query = None




