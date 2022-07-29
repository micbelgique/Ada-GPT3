from distutils.command.config import config
import os
import openai
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
openai.api_key = os.getenv("OPENAI_API_KEY")


# speech_config.speech_recognition_language = "en-US"
conversation = """The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.
        Human: Hello, who are you?
        AI: I am Ada created by the MIC. How can I help you today?
        Human: Can you only speak french after please
        AI: Of course! I would be happy to speak French with you. Let me know if you need any help translating something.
        Human: No just talking with me in french please
        AI: Je suis ravie de pouvoir parler avec vous en français. Faites-moi savoir si vous avez besoin d'aide pour traduire quelque chose.
        Human: C'est quoi le MIC
        AI:Le MIC est une asbl supportée par le privé (Microsoft et Proximus) et le public (Digital Wallonia). Sa mission est de booster l’économie numérique wallonne en aidant les entreprises à se digitaliser et d’animer la communauté des développeurs wallons
    """

@app.route("/", methods=("GET", "POST"))
def text():
    result=""
    global conversation
    if request.method == "POST":  
        human = request.form["human"]
        conversation += "\nHuman:" + human +  "\nAI:"
        response = openai.Completion.create(
                model="text-davinci-002",
                prompt=conversation,
                temperature = 0.1,
                max_tokens = 150,
                top_p = 1,
                frequency_penalty = 0,
                presence_penalty = 0.6, 
                stop = ["\n", " Human:", " AI:"]
            )   
       
        return redirect(url_for("text", result=response.choices[0].text))
        
    result = request.args.get("result")
    conversation+=str(result)
    return render_template("index.html", result=result)
