import google.generativeai as genai
KEY = "AIzaSyC92XWZEYYG0bAsp5KlfDZrMGdAaKPl9QE"
if __name__ == "__main__":
    genai.configure(api_key=KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content("Explain how AI works")
    print(response.text)