from config import llm

def candidate_screening_tool(user_input, job_role):
    """AI-based candidate screening with dynamic questions & evaluation."""
    
    # ✅ Step 1: Generate a dynamic interview question based on the role
    interview_prompt = f"""
    Tum ek AI interviewer ho jo {job_role} role ke liye interview le raha hai.
    Tumhe candidate se ek accha interview question puchna hai jo is role se relevant ho.
    Ek question likho aur bas wahi return karo bina kisi explanation ke.
    """
    response = llm.invoke(interview_prompt)
    question = response.content.strip() if hasattr(response, "content") else str(response).strip()
    
    # ✅ Step 2: Analyze user response (Evaluation hidden from user)
    evaluation_prompt = f"""
    Tum ek experienced interviewer ho. 
    Candidate ne role "{job_role}" ke liye yeh jawab diya: "{user_input}".
    Tumhe is answer ka analysis dena hai.
    """
    evaluation_response = llm.invoke(evaluation_prompt)
    evaluation = evaluation_response.content.strip() if hasattr(evaluation_response, "content") else str(evaluation_response).strip()
    
    # ✅ Print evaluation in the terminal instead of showing to the user
    print("\n🔍 Candidate Answer Evaluation:")
    print(evaluation)
    print("\n-----------------------------\n")
    
    # ✅ Step 3: Return only the next question to the user
    return f"Agla sawaal: {question}"
