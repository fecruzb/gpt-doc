from llama_index import  SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, ServiceContext, PromptHelper, download_loader
from langchain.chat_models import ChatOpenAI
from util.scrapper import url_to_nodes
import gradio as gr
from dotenv import load_dotenv
import os

load_dotenv()

def build_url_index(url, filename = "docs.url.json"):

    # scrap and fetch ALL sub-urls from the main one
    nodes = url_to_nodes(url)

    # define prompt
    prompt = PromptHelper(max_input_size=4096, num_output=256, max_chunk_overlap=20)

    # define LLM
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt)

    # build index
    index = GPTSimpleVectorIndex(nodes, service_context=service_context)

    # save index
    index.save_to_disk(filename)

    return index

def build_folder_index(folder, filename = "docs.index.json"):

    # read documents
    documents = SimpleDirectoryReader(folder).load_data()

    # define prompt
    prompt = PromptHelper(max_input_size=4096, num_output=256, max_chunk_overlap=20)

    # define LLM
    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo"))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, prompt_helper=prompt)

    # build index
    index = GPTSimpleVectorIndex.from_documents(documents, service_context=service_context)

    # save index
    index.save_to_disk(filename)

    return index


def chatbot(input_text, filename):
    # load index
    index = GPTSimpleVectorIndex.load_from_disk(filename)

    ## input query
    response = index.query(input_text)

    return response.response


def start(filename):
    # Create web interface
    inputs = gr.components.Textbox(lines=10, label="Enter your text")
    interface = gr.Interface(fn=lambda input_text: chatbot(input_text, filename), inputs=inputs, outputs="text", title="Custom-trained AI Chatbot")

    # Run at http://127.0.0.1:7860
    interface.launch(share=True)


# Train
# index = build_url_index("https://gpt-index.readthedocs.io/en/latest/index.html", 'index.gptindex.json')

# Run
start('index.gptindex.json')
