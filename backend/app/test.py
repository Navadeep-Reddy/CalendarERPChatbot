import os

import google.generativeai as genai



# 2️⃣ Configure the Google GenAI library
genai.configure(api_key="")
gemini = genai.GenerativeModel("gemini-2.5-flash")


# # # 5️⃣ Generate text
prompt_text = "Hello, how are you?"
try:
    response = gemini.generate_content(prompt_text)
    answer_text = response.text.strip()
except Exception as e:
    answer_text = f"Error generating answer via Gemini: {e}"


print(response.text)

# from google import genai

# client = genai.Client()

# response = client.models.generate_content(
#     model="gemini-2.5-flash",
#     contents="How does AI work?"
# )
# print(response.text)



# import os
# import google.generativeai as genai



# # -------------------------
# # CONFIG
# # -------------------------
# GEMINI_API_KEY = "AIzaSyAonXIAPFobv-uWy3A1fIhQU_HjkSvFmpg"


# # -------------------------
# # 1. Configure Gemini (LLM for final answer)
# # -------------------------
# genai.configure(api_key=GEMINI_API_KEY)
# gemini = genai.GenerativeModel("gemini-2.5-flash")





# prompt = f"""
# You are a retrieval-based assistant.

# Your ONLY source of truth is the content provided in <context>. 
# Do NOT use outside knowledge, assumptions, or reasoning beyond this context.

# Your task:
# - Derive the answer ONLY from the context.
# - If the context has partial information, explain only that part clearly and briefly.
# - If the context does not contain the answer, say: "The available data does not contain information about this query."
# - Write the answer in natural, clear, and concise English.
# - Do NOT include any sentence not supported by the context.

# Answer:
# """

# try:
#     response = gemini.generate_content(prompt)
#     answer_text = response.text.strip()
# except Exception as e:
#     answer_text = f"Error generating answer via Gemini: {e}"


# print(response.text)


