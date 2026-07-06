import json
import re

from backend.prompts import analysis_prompt
from backend.llm import llm


def _extract_json(raw_text):
    """
    Llama 3.1 sometimes wraps JSON in ```json fences, stray text,
    or even double-encodes it as a JSON string. This handles all three.
    """
    text = raw_text.strip()

    # Remove markdown code fences if present
    text = re.sub(r"^```(?:json)?", "", text.strip())
    text = re.sub(r"```$", "", text.strip())
    text = text.strip()

    # Grab the outermost {...} if there's stray text around it
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        text = match.group(0)

    parsed = json.loads(text)

    # Handle double-encoded JSON (parsed came back as a string, not dict)
    if isinstance(parsed, str):
        parsed = json.loads(parsed)

    return parsed
  


def analyze_resume(resume_text, job_description):
    """
    Analyze resume against the job description
    using LangChain PromptTemplate + ChatGroq.
    Returns (success: bool, result: dict | error_message: str)
    """

    try:
        chain = analysis_prompt | llm

        response = chain.invoke(
            {
                "resume": resume_text,
                "job_description": job_description
            }
        )

        

        parsed = _extract_json(response.content)
        return True, parsed

    except json.JSONDecodeError:
        return False, "AI response wasn't valid JSON. Try again."

    except Exception as e:
        return False, str(e)
