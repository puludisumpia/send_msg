import requests

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config["SECRET_KEY"] = "secret_key"
bootstrap = Bootstrap(app)

class SMSForm(FlaskForm):
    name = StringField(label="Nom", validators=[DataRequired()])
    email = EmailField(label="Email", validators=[DataRequired(), Email()])
    message = TextAreaField(label="Message", validators=[DataRequired()])
    submit = SubmitField(label="Envoyer")

# ------- CONFIGURATION FREEMOBILE-------
# Il faut d'abord activer l'api de Notifications par SMS dans 
# votre espace free
# user_id -> votre identifiant de connexion freemobile
# api_key -> votre clé d'identification


def send_sms(msg):
    user_id = "a completer"
    api_key = "a completer"
    url = f"https://smsapi.free-mobile.fr/sendmsg?user={user_id}&pass={api_key}&msg={msg}"
    req = requests.post(url)
    if req.status_code == 200:
        return f"Message envoyé avec succès, {req.status_code}"
    else:
        return f"Une erreur s'est produite, {req.status_code}"


@app.route("/", methods=("GET", "POST"))
def index():
    form = SMSForm()
    if request.method == "POST":
        name = form.name.data
        email = form.email.data
        message = form.message.data

        msg = f"""
            Bonjour, 
            Vous avez un nouveau message de la part de {name}. Voici un extrait: {message}.
            Son mail est: {email}
        """
        # Envoi sms
        send_sms(msg)

        flash("Message envoyé avec succès", "success")

        return redirect(url_for("index"))
    else:
        form = SMSForm()
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)