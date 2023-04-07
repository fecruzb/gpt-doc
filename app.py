from llama_index import  SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, ServiceContext
from langchain.chat_models import ChatOpenAI
import gradio as gr
import os

os.environ["OPENAI_API_KEY"] = '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' # put your key
folder = "docs" # put your files

def build_index():

    # define LLM
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="text-davinci-003"))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    # build index
    documents = SimpleDirectoryReader(folder).load_data()
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

    # save index
    index.save_to_disk('index.json')

    return index


def chatbot(input_text):
    # load index
    index = GPTSimpleVectorIndex.load_from_disk('index.json')

    ## input query
    response = index.query(input_text)

    return response.response


# Construct index
index = build_index()

# Create web interface
inputs = gr.components.Textbox(lines=10, label="Enter your text")
iface = gr.Interface(fn=chatbot, inputs=inputs, outputs="text", title="Custom-trained AI Chatbot")

# Run at http://127.0.0.1:7860
iface.launch(share=True)
