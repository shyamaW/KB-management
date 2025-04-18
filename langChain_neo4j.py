from dotenv import load_dotenv
import os
from langchain.graphs import Neo4jGraph
from langchain.chains import GraphCypherQAChain
#from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI

# Load environment variables from .env file
load_dotenv()

# Neo4j connection details
URI = "bolt://localhost:7687"  # Replace with your Neo4j URI
USERNAME = "neo4j"  # Replace with your username
PASSWORD = "12345678"  # Replace with your password

# Connect to Neo4j
graph = Neo4jGraph(url=URI, username=USERNAME, password=PASSWORD)

# Initialize the LLM (e.g., OpenAI GPT)
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=os.getenv("OPENAI_API_KEY")  # Get the API key from .env
)

# Create the QA chain with `allow_dangerous_requests=True`
chain = GraphCypherQAChain.from_llm(
    llm=llm,
    graph=graph,
    allow_dangerous_requests=True,  # Acknowledge the risks
    verbose=True
)

# Example query
#question = "what are the variety of rice? "
question = "Do not use the SUM function in cypher query, retrieve uri value which is a description, if crop node connects with two node, assign different variable g,g1.Now find: What is the total global planted area for rice, and how much rice is produced worldwide?"
response = chain.run(question)
#print(response["query"])  # Check the generated Cypher query
#print(response["result"])  # Check the response
print(response)

''' 
#corrected Cypher can run
corrected_cypher_query = """
MATCH (gpe:ns0__Growing_Problem_Event)-[:ns0__has_growing_problem]->(pest:Resource {uri: 'http://www.semanticweb.org/22085197/ontologies/2025/0/rice_general#Stalked-eyed_flies'}),
      (gpe)-[:ns0__has_symptom]->(symptom:Resource)
WHERE (gpe)-[:ns0__related_to]->(:ns0__Crop)
RETURN symptom.uri
"""

# Run the corrected query
response = graph.query(corrected_cypher_query)
print(response)'''