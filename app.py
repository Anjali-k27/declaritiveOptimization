
import streamlit as st
from synthesis_engine import master_synthesis_node

st.set_page_config(layout="wide", page_title="Newton SkillUP AlphaFund OS")
st.title("Newton SkillUP AlphaFund OS")

user_query = st.text_input("Strategic Query:")

if st.button("Execute Trinity Pipeline"):
    if not user_query.strip():
        st.warning("Please enter a strategic query before executing.")
    else:
        with st.spinner("Running Trinity Pipeline — SQL · FAISS · Neo4j ..."):
            raw_sql = "Microsoft Market Cap: $3.1T."
            raw_faiss = "Satya Nadella considers Alpha AI a critical acquisition."
            raw_neo4j = "(Alpha AI)--[COMPETES_WITH]--(NeuralNet Labs)"

            prediction = master_synthesis_node(
                sql_math_context=raw_sql,
                faiss_document_context=raw_faiss,
                neo4j_relational_context=raw_neo4j,
                user_query=user_query,
            )

        st.markdown("### Executive Summary")
        st.info(prediction.executive_summary)

        with st.expander("🔍 View AI Reasoning Trace (Audit Log)"):
            st.text(prediction.reasoning)