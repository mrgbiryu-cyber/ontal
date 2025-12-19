from neo4j import GraphDatabase

# 1. 연결 정보 설정
URI = "bolt://localhost:7687"
AUTH = ("neo4j", "horrorshorts")

def initialize_ontology():
    driver = GraphDatabase.driver(URI, auth=AUTH)
    with driver.session() as session:
        # 초기화 (기존 데이터 삭제 - 깔끔한 시작을 위해)
        session.run("MATCH (n) DETACH DELETE n")
        
        # 2. 핵심 엔티티 및 관계 생성 (I-103)
        # 예시로 '공포 테마'와 '장소' 하나씩만 먼저 넣어봅니다.
        cypher_query = """
        CREATE (c:Character {name: '미지의 존재', type: 'Ghost'})
        CREATE (l:Location {name: '폐교', atmosphere: 'Gloomy'})
        CREATE (p:PlotDevice {name: '낡은 거울', effect: 'Reflection'})
        CREATE (c)-[:LOCATED_AT]->(l)
        CREATE (p)-[:LOCATED_AT]->(l)
        """
        session.run(cypher_query)
        print("Ontology initial data injected successfully!")
    driver.close()

if __name__ == "__main__":
    initialize_ontology()