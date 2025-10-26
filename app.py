from flask import Flask, request, render_template_string
import openai

# Replace this with your actual API key
openai.api_key = "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"

app = Flask(__name__)

# The HTML page (simple and clean)
html_page = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat with ChatGPT</title>
</head>
<body style="font-family: Arial; text-align: center; margin-top: 100px;">
    <h2>Python ChatGPT Web App</h2>
    <form method="POST" action="/">
        <input type="text" name="user_input" placeholder="Type your message" style="width:300px; height:30px;">
        <input type="submit" value="Send" style="height:35px;">
    </form>

    {% if response %}
        <p><strong>Response:</strong> {{ response }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    response = None
    if request.method == "POST":
        user_text = request.form["user_input"]

        try:
            # Correct OpenAI syntax for new versions (>=1.0.0)
            chat_response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_text}
                ]
            )

            response = chat_response.choices[0].message.content
        except Exception as e:
            response = f"Error: {e}"

    return render_template_string(html_page, response=response)

if __name__ == "__main__":
    # Run on all network interfaces (so you can access from your phone)
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)

