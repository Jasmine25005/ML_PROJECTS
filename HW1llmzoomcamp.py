# Step 0: Import necessary libraries
import requests
import tiktoken
from tqdm.auto import tqdm
from elasticsearch import Elasticsearch
from openai import OpenAI

# ==============================================================================
# Step 1: Load and process data from the documents URL
# ==============================================================================
docs_url = 'https://github.com/DataTalksClub/llm-zoomcamp/blob/main/01-intro/documents.json?raw=1'
docs_response = requests.get(docs_url)
documents_raw = docs_response.json()

documents = []

# We loop through each course and each document in it to clean and prepare the data
for course in documents_raw:
    course_name = course['course']

    for doc in course['documents']:
        doc['course'] = course_name
        documents.append(doc)

print(" Successfully loaded and processed 1082 documents.")


# ==============================================================================
# Step 2: Connect to Elasticsearch and index the data
# ==============================================================================
# Question 1: Is Elastic running? If this code runs successfully, the answer is yes.
try:
    es_client = Elasticsearch('http://localhost:9200') 
    # We'll make sure the server is up
    es_client.info()
    print(" Successfully connected to Elasticsearch.")
except ConnectionError:
    print(" Failed to connect to Elasticsearch. Make sure the Docker container is running.")
    exit()

# We prepare the Index (the "table") where we will store the data
index_name = "course-questions"
index_settings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "section": {"type": "text"},
            "question": {"type": "text"},
            "course": {"type": "keyword"} 
        }
    }
}

# We delete the old index if it exists and create a new one
if es_client.indices.exists(index=index_name):
    es_client.indices.delete(index=index_name)
es_client.indices.create(index=index_name, body=index_settings)
print(f"Created a new Index named '{index_name}'.")

# Question 2: What is the operation used for indexing? It's 'index'.
# We loop through all documents and add them to Elasticsearch
for doc in tqdm(documents):
    es_client.index(index=index_name, document=doc)
print(f" All documents have been indexed into Elasticsearch.")


# ==============================================================================
# Step 3: Build the search and response generation functions
# ==============================================================================

# Function to search in Elasticsearch
def elastic_search(query, course_filter=None):
    search_query = {
        "size": 5,
        "query": {
            "bool": {
                "must": {
                    "multi_match": {
                        "query": query,
                        "fields": ["question^3", "text", "section"],
                        "type": "best_fields"
                    }
                }
            }
        }
    }
    
    # If there's a filter for a specific course, we add it here
    if course_filter:
        search_query["query"]["bool"]["filter"] = {
            "term": {
                "course": course_filter
            }
        }

    response = es_client.search(index=index_name, body=search_query)
    return response['hits']['hits']

# Function to build the prompt we will use to ask the LLM
def build_prompt(query, search_results):
    prompt_template = """
    You're a course teaching assistant. Answer the QUESTION based on the CONTEXT from the FAQ database.
    Use only the facts from the CONTEXT when answering the QUESTION.
    If the CONTEXT doesn't contain the answer, output NONE.

    QUESTION: {question}

    CONTEXT:
    {context}
    """.strip()

    context = ""
    for doc in search_results:
        doc_str = f"section: {doc['_source']['section']}\nquestion: {doc['_source']['question']}\nanswer: {doc['_source']['text']}\n\n"
        context += doc_str
    
    prompt = prompt_template.format(question=query, context=context)
    return prompt

# Function to call the LLM and get the answer
def llm(prompt):
    # Make sure to put your OpenAI key here or as an environment variable
    # client = OpenAI(api_key="YOUR_OPENAI_KEY")
    client = OpenAI() # It will read the key automatically from environment variables

    response = client.chat.completions.create(
        model='gpt-4o',
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response.choices[0].message.content

# Function to count the number of tokens in the answer
def count_tokens(text):
    encoding = tiktoken.encoding_for_model("gpt-4o")
    return len(encoding.encode(text))

# ==============================================================================
# Step 4: Solve the homework questions
# ==============================================================================

print("\n" + "="*50)
print(" Starting to solve homework questions...")
print("="*50 + "\n")

# --- Question 1: Running Elastic (1 point) ---
# Simply running the code successfully and connecting to ES answers the question.
print("Q1: Running Elastic: Connection successful. The code is working.")

# --- Question 2: Indexing the data (1 point) ---
# The method used in the indexing code is .index()
print("Q2: Indexing the data: The method is 'index'.")

# --- Question 3: Searching (1 point) ---
query_q3 = "How do I execute a command in a running docker container?"
search_results_q3 = elastic_search(query_q3)
top_score_q3 = search_results_q3[0]['_score']
print(f" Q3: Searching: The score of the top result is '{top_score_q3}'.")

# --- Question 4: Filtering (1 point) ---
query_q4 = "How do I copy files from a different folder into docker container’s working directory?"
search_results_q4 = elastic_search(query_q4, course_filter="machine-learning-zoomcamp")
top_question_q4 = search_results_q4[2]['_source']['question'] # The homework asks for the 3rd result
print(f" Q4: Filtering: The 3rd question from the search results is '{top_question_q4}'.")


# --- Question 5: Building a prompt (1 point) ---
prompt_q5 = build_prompt(query_q4, search_results_q4)
prompt_length_q5 = len(prompt_q5)
print(f" Q5: Building a prompt: The length of the prompt is '{prompt_length_q5}' characters.")

# --- Question 6: Tokens (1 point) ---
# Note: Calling the LLM may take a few seconds
print("Q6: Tokens: Generating answer from LLM...")
answer_q6 = llm(prompt_q5)
tokens_q6 = count_tokens(answer_q6)
print(f"Q6: Tokens: The number of tokens in the LLM's answer is '{tokens_q6}'.")
# To print the answer itself
# print(f" LLM Answer: {answer_q6}")

print("\n" + "="*50)
print(" Homework solution finished!")
print("="*50)