from flask import Flask, request, jsonify
from langchain.llms import OpenAI
import constant
from flask_cors import CORS


import os
from langchain.chains import ConversationalRetrievalChain, RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import DirectoryLoader, TextLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.indexes import VectorstoreIndexCreator
from langchain.indexes.vectorstore import VectorStoreIndexWrapper
from langchain.llms import OpenAI
from langchain.vectorstores import Chroma
from werkzeug.utils import secure_filename


app = Flask(__name__)
CORS(app)

os.environ["OPENAI_API_KEY"] = constant.APIKEY

# Enable to save to disk & reuse the model (for repeated queries on the same data)
PERSIST = False

query = None

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
@app.route('/get-result', methods=["POST"])
def getResult():
    data = request.get_json()
    input1 = data.get('input1', 0)

    result = chain({"question": input1, "chat_history": chat_history})

    answer = result['answer']
    print(answer)
    return jsonify({'result': answer})

@app.route('/upload-file', methods=["POST"])
def uploadFile():
# Check if the request contains a file
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400

    file = request.files['file']

    # Check if the file is not empty
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400

    # Check if the file is a PDF
    if file.mimetype != 'application/pdf':
        return jsonify({'error': 'Invalid file format. Please upload a PDF file.'}), 400

    # Save the file to the current folder
    filename = secure_filename(file.filename)
    file.save(filename)

    # Example set data
    example_set = {1, 2, 3, 4, 5}

    # Convert set to list before JSON serialization
    example_list = list(example_set)

    # Example JSON response with a list
    response_data = {'message': 'File uploaded successfully', 'example_list': example_list}

    return jsonify(response_data), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


