import google.generativeai as genai

genai.configure(api_key="AIzaSyC5KjkmEX0KdNPPJo4vd8cdnBW5gjLDMQw")
models = genai.list_models()

models = genai.list_models()
for m in models:
    print(m.name)

response = genai.generate_text(
    model="models/gemini-2.5-flash-lite",
    prompt="Say hello!",
    temperature=0,
    max_output_tokens=50
)

print(response.text)
