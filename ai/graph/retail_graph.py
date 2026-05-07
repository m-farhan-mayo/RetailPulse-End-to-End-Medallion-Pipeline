from typing import TypedDict

from langgraph.graph import StateGraph, END

# ---------------- STATE ---------------- #

class GraphState(TypedDict):

    question: str
    context: str
    answer: str

# ---------------- NODES ---------------- #

def classify_question(state):

    print("\nClassifying Question...\n")

    return state

def retrieve_context(state):

    print("\nRetrieving Context...\n")

    return state

def generate_answer(state):

    print("\nGenerating Answer...\n")

    state["answer"] = "AI Answer Generated"

    return state

# ---------------- GRAPH ---------------- #

workflow = StateGraph(GraphState)

workflow.add_node(
    "classify",
    classify_question
)

workflow.add_node(
    "retrieve",
    retrieve_context
)

workflow.add_node(
    "generate",
    generate_answer
)

workflow.set_entry_point("classify")

workflow.add_edge("classify", "retrieve")

workflow.add_edge("retrieve", "generate")

workflow.add_edge("generate", END)

graph = workflow.compile()

# ---------------- TEST ---------------- #

response = graph.invoke({

    "question": "Top products?",
    "context": "",
    "answer": ""

})

print(response)