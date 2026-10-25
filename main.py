
import re
import json
import urllib.request

url = "http://localhost:11434/api/generate"

assignment = input("Paste your assignment brief: ")
print("\n--- Original Assignment ---")
print(assignment)


prompt = f"""
You are Brief2Done, an assignment requirement extractor.

Your job is to extract instructions from the assignment brief,
not to add new academic requirements.

ASSIGNMENT BRIEF:
{assignment}

Return exactly these sections:

1. MAIN TASK
State the main assignment task in one sentence.

2. EXPLICIT REQUIREMENTS
List only requirements directly stated in the brief.
Include the required topics, sections, file format,
word count, and deadline when provided.

3. ACTION CHECKLIST
Create a short checklist covering every explicit requirement.
Do not introduce new mandatory topics.

4. DEADLINE
Copy the deadline exactly as written.
If absent, write "Not specified".
Never guess a calendar date.

5. WORD COUNT
Copy the word count exactly as written.
If absent, write "Not specified".
Treat a stated range as a requirement, not a suggestion.

6. MISSING INFORMATION
Mention only important information not provided.
Do not invent answers to missing information.

STRICT RULES:
- Never invent requirements.
- Never present suggestions as lecturer instructions.
- Never invent dates, citation styles, or reference counts.
- Do not add unrelated academic explanations.
- Do not ask follow-up questions.
- Keep the output concise.
"""


data = {
    "model": "gemma3:1b",
    "prompt": prompt,
    "stream": False
}

request_data = json.dumps(data).encode("utf-8")

request = urllib.request.Request(
    url,
    data=request_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)

with urllib.request.urlopen(request) as response:
    result = json.loads(response.read().decode("utf-8"))

print("\n--- Brief2Done Analysis ---\n")
print(result["response"])

analysis = result["response"]


pattern = r"([\d,]+)\s*(?:-|–|to)\s*([\d,]+)\s*words?"

match = re.search(pattern, assignment, re.IGNORECASE)


if match:
    minimum = match.group(1)
    maximum = match.group(2)
    word_count = (minimum, maximum)
else:
    word_count = None

if match:
    minimum = match.group(1)
    maximum = match.group(2)
    word_count = (minimum, maximum)
else:
    word_count = None

if word_count is not None:
    verified_word_count = f"{word_count[0]}–{word_count[1]} words"
else:
    verified_word_count = "Not detected"

print("\n--- Verified Assignment Details ---")
print(f"Word count: {verified_word_count}")