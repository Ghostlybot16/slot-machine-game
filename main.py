from flask import Flask, render_template, request, redirect, session, url_for

app = Flask(
    __name__,
    template_folder="web_app/templates",
    static_folder="web_app/static"
)
app.secret_key = 'dev'

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        balance = request.form.get("deposit_amount")
        if balance and balance.isdigit() and int(balance) > 0:
            balance = int(balance)
            session["balance"] = balance
            return render_template("home_page.html", message=f"You've deposited ${balance} to play the game!")
        return render_template("home_page.html", error="Please enter a valid deposit amount.")

    return render_template("home_page.html")

@app.route("/play", methods=["GET"])
def play():
    balance = session.get("balance", 0)
    return f"<h2>You're now ready to play! Your starting balance is ${balance}.</h2>"

if __name__ == "__main__":
    app.run(debug=True)