from langchain_google_genai import GoogleGenerativeAI
from langgraph.graph import StateGraph, START, END
from typing_extensions import TypedDict
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

class State(TypedDict):
    application: str
    experience : str
    skill_match: str
    response : str

llm = GoogleGenerativeAI(model = 'gemini-2.5-flash', temperature = 0.7)

workflow = StateGraph(State)


def categorized_candidate(state:State) -> State:
  prompt = ChatPromptTemplate.from_template(
      "Based on job application, categorized the candidate reponse in one word only as 'Entry-level', 'Mid-level', 'Senior-level' "
      "application : {application}"
  )
  chain = prompt | llm
  experience_level = chain.invoke({"application": state['application']})
  print(f"\nexperience_level :: {experience_level}\n")
  return {'experience' : experience_level} # type: ignore

def access_skill(state:State) -> State:
  prompt = ChatPromptTemplate.from_template(
      "Based on job application for Python developer, check the candidate skill set"
      "response in one word as either 'Match' or 'No Match'"
      "application : {application}")
  chain = prompt | llm
  skill_match = chain.invoke({"application": state['application']})
  print(f"\nskill_match :: {skill_match}\n")
  return {'skill_match' : skill_match} # type: ignore

def selected(state:State) -> State:
  print(f"Candidate is selected for interview")
  return {'response' : 'Candidate is selected for interview.'} # type: ignore

def escalate(state:State) -> State:
  print(f"Candidate is sent to HR")
  return {'response' : 'Candidate is sent to HR.'} # type: ignore

def reject(state:State) -> State:
  print(f"Candidate is rejected")
  return {'response' : 'Candidate is rejected.'} # type: ignore

def route_action(state:State) -> str :
  if(state['skill_match'] == 'Match'):
    return 'selected_for_interview'
  elif(state['experience'] == 'Senior-level'):
    return 'escalate_to_hr'
  else:
    return 'reject_candidate'

workflow.add_node("categorized_candidate",categorized_candidate)
workflow.add_node("access_candidate_skill",access_skill)
workflow.add_node("selected_for_interview",selected)
workflow.add_node("escalate_to_hr",escalate)
workflow.add_node("reject_candidate",reject)

workflow.add_edge("categorized_candidate","access_candidate_skill")
workflow.add_conditional_edges("access_candidate_skill",route_action)

workflow.add_edge(START,"categorized_candidate")
workflow.add_edge("selected_for_interview",END)
workflow.add_edge("escalate_to_hr",END)
workflow.add_edge("reject_candidate",END)

app = workflow.compile()

application = "I have 3 years of experience in FastAPI backend development"
response = app.invoke({"application":application}) # type: ignore
print(f"""
  application : {response['application']}
  experience_level : {response['experience']}
  skill_match : {response['skill_match']}
  response : {response['response']}
""")