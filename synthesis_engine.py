
import os
from dotenv import load_dotenv
import dspy

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.environ.get("GEMINI_API_KEY", "")

# Initialize the dspy signature  
class AlphaFundExecutiveSynthesizer(dspy.Signature):
    """You are a senior investment analyst writing formal strategic intelligence reports.
    Given quantitative financial data, qualitative intelligence from documents, and
    relational graph data about competitive positioning, produce a 2-3 paragraph formal
    strategic executive summary that precisely weaves together all three data sources.
    You MUST explicitly reference the financial valuation figures, the named executive's
    strategic interest, and the specific competitive relationship from the graph data.
    Write in a precise, authoritative tone suitable for a fund manager briefing."""

    sql_math_context: str = dspy.InputField(desc="Quantitative financial data from SQL analytics, including market caps, valuations, and financial metrics")
    faiss_document_context: str = dspy.InputField(desc="Qualitative intelligence retrieved from document store, including executive statements, strategic assessments, and analyst opinions")
    neo4j_relational_context: str = dspy.InputField(desc="Relational graph data showing competitive landscape, partnerships, and entity relationships")
    user_query: str = dspy.InputField(desc="The strategic question or analytical objective posed by the fund analyst")

    executive_summary: str = dspy.OutputField(desc="A 2-3 paragraph formal strategic executive summary that explicitly incorporates the financial valuation from sql_math_context, the named executive's strategic view from faiss_document_context, and the competitive relationship from neo4j_relational_context")

class DashboardPipeline(dspy.Module):
    def __init__(self):
        super().__init__()
        self.synthesize = dspy.ChainOfThought(AlphaFundExecutiveSynthesizer)

    def forward(self, sql_math_context, faiss_document_context, neo4j_relational_context, user_query):
        return self.synthesize(
            sql_math_context=sql_math_context,
            faiss_document_context=faiss_document_context,
            neo4j_relational_context=neo4j_relational_context,
            user_query=user_query,
        )
    
lm = dspy.LM(model="gemini/gemini-2.5-flash", temperature=0.0)
dspy.configure(lm=lm)

master_synthesis_node = DashboardPipeline()