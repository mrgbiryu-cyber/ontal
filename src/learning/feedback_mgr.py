import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

load_dotenv()

class FeedbackManager:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"),
            auth=(os.getenv("NEO4J_USER"), os.getenv("NEO4J_PASSWORD"))
        )

    def update_relationship_weight(self, source_name, rel_type, target_name, score_change):
        """
        피드백 결과에 따라 관계의 가중치를 업데이트합니다.
        score_change: 양수면 추천 강화, 음수면 회피 강화
        """
        with self.driver.session() as session:
            # 관계를 찾아서 weight 속성을 수정하는 Cypher 쿼리
            query = f"""
            MATCH (s {{name: $s_name}})-[r:{rel_type}]->(o {{name: $o_name}})
            SET r.weight = coalesce(r.weight, 0) + $change
            SET r.avoid_score = CASE WHEN $change < 0 THEN coalesce(r.avoid_score, 0) + abs($change) ELSE r.avoid_score END
            RETURN r.weight, r.avoid_score
            """
            session.run(query, s_name=source_name, o_name=target_name, change=score_change)
            print(f"✅ {source_name}-{rel_type}->{target_name} 지식 가중치 업데이트 완료")

    def close(self):
        self.driver.close()