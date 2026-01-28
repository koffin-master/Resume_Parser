from langgraph.graph import StateGraph,START
from typing import TypedDict
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os
import streamlit as st

load_dotenv()

resume_llm = ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key = os.getenv('GROQ_API_KEY'),


)
evaluator_llm = ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key = os.getenv('GROQ_API_KEY'),


)
optimizer_llm = ChatGroq(
    model = "openai/gpt-oss-20b",
    api_key = os.getenv('GROQ_API_KEY'),


)

class Resumestate(TypedDict):
    JD : str
    resume_content : str
    ResumeandJD : str
    descriptionALL : str
    evaluationResume : str
    Clear_Result : str

def resume_checker(state : Resumestate):
    messages = [
        SystemMessage(content= "You are a resume shortlister AI and You see resume based on the given Job description"),
        HumanMessage(content=f"""
                Here is the Job description : {state['JD']}
                Here is the candidate's resume content : {state['resume_content']}
                Find : -
                1. What kind of Resume is this. Which means on what topics the resume is more focused like MLops, AIML etc.
                2. What are the given Job description expect.What level the JD demand from the candidate [junior, mid, senior]
                3. Are the expectation of JD is even realistic.
                4. Extract the Skills from the resume content whether its explicit or implied.
                5. Write all those candidates skills [explicit + implied] distinctively and break down what each skill means.
                6. Extract What kind of skills the JD demand and what are the expectations of the JD
"""
                     )
    ]
    response = resume_llm.invoke(messages).content
    return {'ResumeandJD' : response}

def evaluate_resume(state: Resumestate):
    messages = [
        SystemMessage(
            content=(
                "You are a strict, no-nonsense Resume content evaluator based on the Resume content, description and given JD Info"
                "You judge resume skills like a senior person on that JD role in the company. "
                "You only evaluate and give precise feedback."
            )
        ),
        HumanMessage(
            content=f"""
Evaluate the following Following  Resume content and their skill, confidence and experience level based on the JD info **very strictly**.

Info:
\"\"\"
{state['ResumeandJD']}
\"\"\"

Resume Classification Criteria
	•	Extract and normalize candidate skills (technical, tools, domain).
	•	Identify candidate’s core strengths aligned with role requirements.
	•	Assess experience level (years, role type, project depth).
	•	Evaluate relevance of past work to the JD’s domain and responsibilities.
	•	Detect seniority signals (ownership, scale, impact, leadership).

⸻

JD Expectation Analysis
	•	Identify mandatory, core, and nice-to-have skills from the JD.
	•	Highlight which core JD skills are present in the candidate profile.
	•	Clearly list missing JD skills from the candidate’s perspective.
	•	Compare candidate experience level with JD’s expected seniority.
	•	Judge whether missing skills are critical blockers or easily trainable.
	•	Evaluate overall role fit (Strong Fit / Partial Fit / Weak Fit).

⸻

Output Rules & Constraints
	•	No question–answer format.
	•	Use clear headings and decisive statements.
	•	Stay within 300 words.
	•	Avoid generic comments; provide actionable insight.
	•	Focus on hiring relevance, not academic evaluation.

Decision Rules:
- Give all answer in concise manner
- If ANY red flag you see , add a special note. If not than dont add anything.
- In all cases give 1 paragraph short feedback explaining the strength and weakness
- Dont call any tool

Output Format 

The evaluation output must be divided into two clearly separated sections:
	1.	JDExpectation
	2.	ResumeCriteria
"""
        )
    ]
    response = evaluator_llm.invoke(messages).content



    return {"descriptionALL": response}


def reChecker_info(state: Resumestate):
    messages = [
        SystemMessage(
            content=(
                f"You are the senior most fully skilled person with experience of many years in the given JD {state['JD']} "
                "Your job is to IMPROVE the given info and matching between the JD and the given resume strictly with your knowledge in the field only. "
                "You rewrite intelligently, and concisely. "
                "You keep the original intent, topic, and structure. "
                "You do NOT add fluff, emojis, or hashtags."
            )
        ),
        HumanMessage(
            content=f"""
You are given:
1) A Resume info along with their skill information, what the candidate lacks , what is his strength etc.
2) Also include the JD expectations in terms of skills and experience.

Your task:
- Rewrite the information or review of the resume if it necessary.
- Tell how much the resume match with jd requirement
- Improve clarity, insight, tone, and professionalism
- Make it feel more human, less AI-like
- Preserve the original topic and message
- Clearly tells which gap is critical, which is moderate , and which can achieved easily. [A one word ranking system for each gap skill]
- In result also give score for strength, description and other things where explicit.
- format it correctly


Rules to follow (MANDATORY):
1. Max 300 words
2. NO question–answer format
3. Tone must be intelligent, professional, and confident
4. Humor or sarcasm must be subtle and tasteful (optional, not forced)
5. Use simple, day-to-day English
6. No cringe phrases, no buzzwords, no motivational clichés
7. Do NOT explain what you changed
8. Output ONLY the optimized information text
9. - Dont call any tool

The complete info about the resume and JD is here :
{state['descriptionALL']}

Return only the improved  information and any other info only if it is necessary.
"""
        )
    ]

    response = optimizer_llm.invoke(messages).content

    return {
        "Clear_Result": response
    }


graph = StateGraph(Resumestate)
graph.add_node("generate", resume_checker)
graph.add_node("evaluate", evaluate_resume)
graph.add_node("optimize", reChecker_info)

graph.add_edge(START, "generate")
graph.add_edge("generate", "evaluate")
graph.add_edge("evaluate", "optimize")

workflow = graph.compile()

st.title("Resume Parser")

user_input = st.text_input("Enter The Job description briefly: ")

user_input2 = st.text_input("Enter The Resume description briefly: ")


initial_state = {"JD": user_input, "resume_content" : user_input2 }


if st.button("CHECK"):
    st.subheader("Post : ")
    if user_input:
        output_state = workflow.invoke(initial_state)
        st.write(output_state['Clear_Result'])
    else:
        st.write("Please Enter Something")


