from langchain_core.prompts import PromptTemplate

analysis_prompt = PromptTemplate.from_template(
"""
You are an expert AI Interview Preparation Assistant.

Your task is to compare the candidate's resume with the job description
and return a structured match analysis.

Resume:
{resume}

Job Description:
{job_description}

Respond with ONLY a valid JSON object — no markdown fences, no preamble, no explanation, no extra text before or after.
Use exactly this structure:

{{
  "overall_match_score": <integer 0-100>,
  "summary": "<3-5 line resume summary and overall fit assessment>",
  "categories": {{
    "technical_skills": {{
      "score": <integer 0-100>,
      "matched": ["skill1", "skill2"],
      "missing": ["skill3"]
    }},
    "soft_skills": {{
      "score": <integer 0-100>,
      "matched": ["skill1"],
      "missing": ["skill2"]
    }},
    "experience_level": {{
      "score": <integer 0-100>,
      "notes": "<short note on whether experience level fits the JD>"
    }},
    "tools_frameworks": {{
      "score": <integer 0-100>,
      "matched": ["tool1"],
      "missing": ["tool2"]
    }}
  }}
}}

Rules:
- overall_match_score should be a weighted overall fit, not a simple average of category scores.
- Only include skills/tools that are actually mentioned or clearly implied in the job description.
- Keep each list concise (max 8 items).
- Be professional and concise in all text fields.
- Return ONLY the JSON object. Nothing else.
"""
)
