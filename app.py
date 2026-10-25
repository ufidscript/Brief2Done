import gradio as gr
import json
import urllib.request
import re
import urllib.error



def analyze_assignment(assignment):
    if not assignment.strip():
        return "Please paste an assignment brief."
    # Extract word-count range from the original assignment
    pattern = r"\b([\d,]+)\s*(?:-|–|—|to|and)\s*([\d,]+)\s*words?\b"
    match = re.search(pattern, assignment, re.IGNORECASE)

    if match:
        word_count = f"{match.group(1)}–{match.group(2)} words"
    else:
        word_count = "Not detected"

         # Detect common submission formats
    format_match = re.search(
        r"\b(PDF|DOCX|DOC)\b",
        assignment,
        re.IGNORECASE
    )

    if format_match:
        file_format = format_match.group(1).upper()
    else:
        file_format = "Not detected"

    # Detect common weekday deadlines
    deadline_match = re.search(
        r"\b(?:by|before|due|on)\s+"
        r"(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday)\b",
        assignment,
        re.IGNORECASE
    )

    if deadline_match:
        deadline = deadline_match.group(1)
    else:
        deadline = "Not detected"


   
    prompt = f"""
You are Brief2Done, an assignment instruction extractor.

Analyze the following assignment brief:

{assignment}

Return a JSON object containing exactly three keys:

"main_task": A short sentence describing the main task.


"requirements": A list of objects. Each object must have:

"requirement": A short description of an explicitly stated instruction.
"evidence": An exact quotation copied from the original assignment.

Example:
{{
  "requirement": "Submit the report as a PDF",
  "evidence": "Submit the report as a PDF"
}}

Do not include a requirement unless you can quote supporting
words directly from the original assignment.


"suggestions": A list of up to three optional suggestions
that may help the student complete the assignment.

Rules:
- Never generate the assignment itself.
- Never write a report or essay.
- Never invent deadlines, grading percentages, or word counts.
- Never invent source counts or citation styles.
- Preserve the exact meaning of the original instructions.
- Keep suggestions separate from requirements.
- Return only valid JSON.
"""



    payload = {
        "model": "gemma3:1b",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    request = urllib.request.Request(
        "http://localhost:11434/api/generate",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            result = json.loads(response.read().decode("utf-8"))

        raw_ai_response = result.get("response", "")

        if not raw_ai_response.strip():
            return f"Ollama returned an empty response. Details: {result}"

        try:
            analysis = json.loads(raw_ai_response)
        except json.JSONDecodeError:
            return f"Gemma returned invalid JSON:\n\n{raw_ai_response[:1000]}"
        main_task = analysis.get("main_task", "Not identified")
        requirements = analysis.get("requirements", [])
        suggestions = analysis.get("suggestions", [])

        if isinstance(suggestions, list):
            suggestions = suggestions[:3]
        else:
            suggestions = []
        output = (
    f"## 📋 Extracted from Original Brief\n\n"
    f"**Word-count range:** {word_count}\n\n"
    f"**File format:** {file_format}\n\n"
    f"**Deadline:** {deadline}\n\n"
    f"---\n\n"
    f"## 🤖 AI-Generated Analysis (Unverified)\n\n"
    f"### Main Task\n\n{main_task}\n\n"
    f"### Requirements\n\n"
)



        output += "- Complete the main task described above.\n"

        if word_count != "Not detected":
            output += f"- Follow the word-count range: {word_count}.\n"

        if file_format != "Not detected":
            output += f"- Submit in {file_format} format.\n"

        if deadline != "Not detected":
            output += f"- Submit by {deadline}.\n"

        output += "\n### 📝 Optional Suggestions\n\n"

        if suggestions:
            for suggestion in suggestions:
                output += f"- {suggestion}\n"
        else:
            output += "No optional suggestions generated.\n"


        return output
    except urllib.error.HTTPError as error:
        details = error.read().decode("utf-8", errors="replace")
        return f"Ollama HTTP error {error.code}:\n{details}"

    except Exception as error:
        return f"Unable to analyze assignment: {error}"

demo = gr.Interface(
    fn=analyze_assignment,
    inputs=gr.Textbox(
        label="Assignment Brief",
        lines=6,
        placeholder="Paste your lecturer's instructions here..."
    ),
    outputs=gr.Markdown(
        value="### 📋 Brief2Done Results\n\nYour assignment analysis will appear here."
    ),
    title="Brief2Done",
    description="Turn assignment briefs into clear, actionable steps.",
    flagging_mode="never"
)

demo.launch(inbrowser=True)
