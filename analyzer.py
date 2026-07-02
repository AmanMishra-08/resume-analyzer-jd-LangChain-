from backend.prompts import analysis_prompt
from backend.llm import llm


def analyze_resume(resume_text, job_description):
    """
    Analyze resume against the job description
    using LangChain PromptTemplate + ChatGroq.
    """

    try:

        # Create LangChain Chain
        chain = analysis_prompt | llm

        # Invoke the chain
        response = chain.invoke(
            {
                "resume": resume_text,
                "job_description": job_description
            }
        )

        return True,response.content

    except Exception as e:
        return False, str(e)