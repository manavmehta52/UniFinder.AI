from flask import Flask, request, render_template
import cohere
import os

app = Flask(__name__)

# Cohere API setup (replace with your actual API key)
co = cohere.Client("hS5QrCpGSyIsUxcKY7pGo4JpLwUaM3wZSaW45B0U")

chat_history = []

@app.route("/", methods=["GET", "POST"])
def index():
    global chat_history

    if request.method == "POST":
        user_input = request.form["user_input"]
        chat_history.append({"sender": "user", "text": user_input})

        # Build full conversation context as prompt
        prompt = (
            "You are an expert educational advisor AI that helps students find the best universities based on their major, GPA, budget, and preferred country. "
            "Provide clear and informative suggestions in natural language.\n"
        )
        for msg in chat_history:
            role = "User" if msg["sender"] == "user" else "Advisor"
            prompt += f"{role}: {msg['text']}\n"
        prompt += "Advisor:"

        try:
            response = co.generate(
                model="command-r-plus",
                prompt=prompt,
                max_tokens=800,  # Increased to prevent cutoff
                temperature=0.7,
            )
            reply = response.generations[0].text.strip()
        except Exception as e:
            print("Cohere API Error:", e)
            reply = "Sorry, something went wrong while fetching suggestions."

        chat_history.append({"sender": "bot", "text": reply})

    return render_template("index.html", messages=chat_history)

if __name__ == "__main__":
    app.run(debug=True)
