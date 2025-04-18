from neo4j import GraphDatabase

# Neo4j connection details
URI = "bolt://localhost:7687"  # Replace with your Neo4j URI
AUTH = ("neo4j", "12345678")  # Replace with your credentials

# Initialize the driver
driver = GraphDatabase.driver(URI, auth=AUTH)

# Test the connection
def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Hello, Neo4j!' AS message")
        print(result.single()["message"])

def query_kb(question):
    query = """
    MATCH p=()-[r:ns0__has_control_method]->() RETURN p LIMIT 25
    """
    with driver.session() as session:
        result = session.run(query, keyword=question)
        return [record for record in result]

# Example usage
question = "Tell me about product X"
results = query_kb(question)
for record in results:
    print(record)

#test_connection()