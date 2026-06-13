from synthesis_engine import master_synthesis_node

raw_sql = "Microsoft Market Cap: $3.1T."
raw_faiss = "Satya Nadella considers Alpha AI a critical acquisition."
raw_neo4j = "(Alpha AI)--[COMPETES_WITH]--(NeuralNet Labs)"
query = "Provide an overview of Alpha AI's market position."

print("Running synthesis pipeline test...\n")

prediction = master_synthesis_node(
    sql_math_context=raw_sql,
    faiss_document_context=raw_faiss,
    neo4j_relational_context=raw_neo4j,
    user_query=query,
)

summary = prediction.executive_summary
rationale = prediction.reasoning

print("=" * 60)
print("EXECUTIVE SUMMARY")
print("=" * 60)
print(summary)
print()
print("=" * 60)
print("RATIONALE (AI Reasoning Trace)")
print("=" * 60)
print(rationale)
print()


# Strict pass criteria validation 
checks = {
    "Microsoft $3.1T valuation": any(x in summary for x in ["3.1T", "$3.1", "3.1 trillion", "3.1-trillion"]),
    "Satya Nadella acquisition interest": any(x in summary for x in ["Nadella", "Satya"]),
    "NeuralNet Labs competition": "NeuralNet" in summary,
    "Rationale generated": bool(rationale and rationale.strip()),
}

print("=" * 60)
print("PASS / FAIL CRITERIA")
print("=" * 60)
all_passed = True
for criterion, passed in checks.items():
    status = "PASS" if passed else "FAIL"
    print(f"  [{status}] {criterion}")
    if not passed:
        all_passed = False

print()
if all_passed:
    print("RESULT: ALL CHECKS PASSED - Pipeline is verified.")
else:
    print("RESULT: ONE OR MORE CHECKS FAILED - Review output above.")