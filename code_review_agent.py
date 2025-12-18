from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, START , END 
from typing import TypedDict
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import interrupt , Command

# Subgraph 
subgraph_llm = ChatOllama(model = "llama3.2:1b")

# subgraph state
class AnalysisState(TypedDict, total=False):

    code : str 
    language : str 
    syntax_issues : str 
    best_practice_issues: str 
    security_issues : str 
    performance_issues : str 

# Syntax validator node
def syntax_check_node(state: AnalysisState ):
    """Check for syntax issues"""

    prompt = f"""Analyze this give {state['language']} for syntax issues:
                code : {state['code']}

                List any syntax errors or warning. be specific
            """ 
    
    response = subgraph_llm.invoke(prompt)

    return {'syntax_issues': response.content}
    
# Best practices Checker
def best_practices_node(state: AnalysisState):
    """Check for best practices"""
    
    prompt = f"""Review this code {state['language']} for best practices violations:
                code : {state['code']}

                Check for: naming conventions, code organization, documentation, etc.
                
            """
    
    response = subgraph_llm.invoke(prompt)

    return {"best_practice_issues": response.content}
    

# Security and vulnerabilities review
def security_check_node(state: AnalysisState):
    """Check for security issues"""

    prompt = f"""Check and Analyze the code {state['language']} for security vulneralibities
            code : {state['code']}

            Review and look for : SQL injection ,XSS, hardcoded secrets , unsafe opeartions, etc.
            """
    
    response = subgraph_llm.invoke(prompt)

    return {'security_issues': response.content}
    
# Performance issue identification
def performance_review_node(state: AnalysisState):
    """Check for performance issues"""

    prompt = f"""Review this code {state['language']} for any performace related issues:
                code : {state['code']}

                Check for: memory issues , inefficient loop, unnecessary operations or 
                time or space complexicity issue.
                
            """
    
    response = subgraph_llm.invoke(prompt)

    return {'performance_issues':response.content}

# Build Subgraph Workflow
subgraph = StateGraph(AnalysisState)

subgraph.add_node("syntax_check_node", syntax_check_node)
subgraph.add_node("best_practices_node", best_practices_node)
subgraph.add_node("security_check_node", security_check_node)
subgraph.add_node("performance_review_node", performance_review_node)

subgraph.set_entry_point("syntax_check_node")
subgraph.add_edge("syntax_check_node","best_practices_node")
subgraph.add_edge("best_practices_node","security_check_node")
subgraph.add_edge("security_check_node","performance_review_node")
subgraph.add_edge("performance_review_node",END)

analysis_graph = subgraph.compile()


# main workflow
main_model = ChatOllama(model = "llama3.2:1b")

class CodeState(TypedDict, total=False):

    code : str 
    language : str 
    syntax_issues : str 
    best_practice_issues: str 
    security_issues : str 
    performance_issues : str 
    human_feedback : str 
    final_report : str 

# Code Validation node
def code_input_node(state : CodeState):
    """Validate and check the code"""

    if not state["code"].strip():
        raise ValueError("Code cannot be empty")
    
    return state 

# Code analysis node using subgraph
def Analyze_code_node(state : CodeState):
    """Run analysis subgraph"""

    subgraph_input = {
        'code': state['code'],
        'language' : state['language'],
        'syntax_issues': '',
        'best_practice_issues': '' ,
        'security_issues' : '', 
        'performance_issues' : ''
    }

    result = analysis_graph.invoke(subgraph_input)

    state["syntax_issues"] = result["syntax_issues"]
    state["best_practice_issues"] = result["best_practice_issues"]
    state["security_issues"] = result["security_issues"]
    state["performance_issues"] = result["performance_issues"]

    return state

# simple Human in the loop for demo purpose
def human_feedback_node(state: CodeState):
    """Display result and get human approval"""
    
    print("\n" + "="*60)
    print("CODE REVIEW RESULTS")
    print("="*60)
    print(f"\n🔍 Syntax Issues:\n{state['syntax_issues']}\n")
    print(f"📋 Best Practices:\n{state['best_practice_issues']}\n")
    print(f"🔒 Security Issues:\n{state['security_issues']}\n")
    print(f"⚡ Performance Issues:\n{state['performance_issues']}\n")
    print("="*60)
    
    # Get actual user input from terminal
    approval = input("\nDo you approve these findings? (yes/no): ").strip().lower()
    
    if approval == "yes":
        state["human_feedback"] = "approved"
    else:
        state["human_feedback"] = "need_improvements"
    
    return state


# Human in the loop with interrupt
#def human_feedback_node(state : CodeState):
#    """Display result and get human approval"""

#    decision = interrupt({
#        "type" : "code review approval",
#        "reason": "code review is completeted, need human approval",
#        "findings": {
#            'syntax' : state["syntax_issues"],
#            'best_practice': state["best_practice_issues"],
#           'security': state["security_issues"],
#            'performance' : state["performance_issues"]
#        },
#        "instructions": "Review the findings and respond with {'approved' : 'yes'} or {'approved' : 'no'}"
#    })

#    if decision.get('approved') == 'yes':
#        state["human_feedback"] = "approved"

#    else:
#        state["human_feedback"] = "need_improvements"

#    return state


def final_report_node(state : CodeState):
    """Generate final comprehensive report"""

    prompt = f"""Generate a comprehensive code review report based on these findings:

            language : {state['language']}

            syntax issues: {state['syntax_issues']}
            best practices: {state['best_practice_issues']}
            security issues: {state['security_issues']}
            performance issues: {state['performance_issues']}

        Create a professional, structured report with:
        - Executive Summary
        - Detailed summary
        - Recommendation
        - Priority levels 
        - Tips for improvement in code
        """
    
    response = main_model.invoke(prompt)

    return {'final_report' : response.content}


# Routing based on human condition
def human_routing_condition(state : CodeState):
    """Route based on feedback"""
    if state.get('human_feedback') == "approved":
        return "approved"

    else:
        return "need_improvements"

graph = StateGraph(CodeState)

checkpointer = InMemorySaver()

graph.add_node("code_input_node", code_input_node)
graph.add_node("Analyze_code_node",Analyze_code_node)
graph.add_node("human_feedback_node",human_feedback_node)
graph.add_node("final_report_node", final_report_node)

graph.add_edge(START, "code_input_node")
graph.add_edge("code_input_node", "Analyze_code_node")
graph.add_edge("Analyze_code_node","human_feedback_node")
graph.add_conditional_edges("human_feedback_node",human_routing_condition,{ "approved": "final_report_node" , "need_improvements":"Analyze_code_node"})
graph.add_edge("final_report_node", END)

main_graph = graph.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "1"}}

# Test the agent
test_code = """
def add_numbers(a, b):
    result = a + b
    return result
"""

print("Starting code review...")

result = main_graph.invoke({
    "code": test_code,
    "language": "python"
}, config=config)

print("\n" + "="*60)
print("FINAL REPORT:")
print("="*60)
print(result.get('final_report'))


"""# First invoke : runs until it hits the interrupt
try:
    result = main_graph.invoke({
        "code": test_code,
        "language": "python"
    }, config=config)
    
    print("\n=== GRAPH INTERRUPTED ===")
    print("The graph is waiting for your approval.")
    print("Current state:", result)
    
except Exception as e:
    print(f"Interrupted as expected: {e}")

# Now you provide feedback and resume
print("\nProviding approval...")
final_result = main_graph.invoke(
    Command(resume={"approved": "yes"}),  # or "no" to reject
    config=config
)

print("\n" + "="*60)
print("FINAL REPORT:")
print("="*60)
print(final_result.get('final_report'))
"""
