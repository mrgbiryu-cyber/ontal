import streamlit as st
from src.generator.scenario_gen import generate_horror_script

# 페이지 설정
st.set_page_config(page_title="부자 - 공포 쇼츠 AI", page_icon="👻")

st.title("👻 온톨로지 기반 공포 쇼츠 생성기")
st.subheader("형님, 오늘은 어떤 공포를 만들어볼까요?")

# 1. 사이드바 - 설정
with st.sidebar:
    st.header("⚙️ 시스템 설정")
    st.info("Neo4j DB 및 Gemini 2.0/3.0 연동 중")

# 2. 메인 화면 - 생성 버튼
if st.button("🔮 새로운 대본 생성하기", use_container_width=True):
    with st.spinner("Gemini가 지식 그래프를 읽어 대본을 쓰고 있습니다..."):
        try:
            script = generate_horror_script()
            st.session_state['current_script'] = script
        except Exception as e:
            st.error(f"오류 발생: {e}")

# 3. 결과 출력 및 피드백
if 'current_script' in st.session_state:
    st.divider()
    st.markdown("### 📜 생성된 대본")
    st.write(st.session_state['current_script'])
    
    st.divider()
    st.markdown("### 📊 이 대본은 어떠셨나요? (피드백 학습)")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("👍 대박 (성공)", use_container_width=True):
            st.success("피드백 반영 완료: 이 조합의 우선순위를 높입니다!")
            # TODO: L-303 가중치 상승 로직 연결 예정
            
    with col2:
        if st.button("👎 노잼 (실패)", use_container_width=True):
            st.warning("피드백 반영 완료: 이 조합을 당분간 피하도록 학습합니다.")
            # TODO: L-303 Avoid Score 상승 로직 연결 예정