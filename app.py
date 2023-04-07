from llama_index import  SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, ServiceContext
from langchain.chat_models import ChatOpenAI
import gradio as gr
import os

os.environ["OPENAI_API_KEY"] = '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'

def construct_index(directory_path):

    # define LLM
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-4"))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    # build index
    documents = SimpleDirectoryReader(directory_path).load_data()
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
index = construct_index("docs")

## Create web interface
inputs = gr.components.Textbox(lines=10, label="Enter your text")
iface = gr.Interface(fn=chatbot, inputs=inputs, outputs="text", title="Custom-trained AI Chatbot")

iface.launch(share=True)
