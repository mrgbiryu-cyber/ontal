import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"), 
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        self.driver.close()

    def get_knowledge_triples(self):
        with self.driver.session() as session:
            # DB에 있는 모든 연결 관계를 가져옵니다.
            result = session.run("MATCH (s)-[r]->(o) RETURN s.name, type(r), o.name")
            return [f"{record[0]} - {record[1]} -> {record[2]}" for record in result]