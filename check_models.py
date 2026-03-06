import google.genai as genai

API_KEY = input("AIzaSyBBMB2qg1Xnfhl56dJN8dfbagGC12ZptS0").strip()
genai.configure(api_key=API_KEY)

print("\nAvailable models that support generateContent:\n")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(" -", m.name)