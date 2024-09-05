from __future__ import annotations

from flask import render_template

from src import app, services


@app.route("/frontend-developer")
def frontend_developer():
    return render_template("profile-tab.html", services=services)


@app.route("/backend-developer")
def backend_developer():
    return render_template("profile-tab.html", services=services)


@app.route("/devops-engineer")
def devops_engineer():
    return render_template("profile-tab.html", services=services)


@app.route("/full-stack-developer")
def full_stack_developer():
    return render_template("profile-tab.html", services=services)


@app.route("/ai-data-scientist")
def ai_data_scientist():
    return render_template("profile-tab.html", services=services)


@app.route("/data-analyst")
def data_analyst():
    return render_template("profile-tab.html", services=services)


@app.route("/android-developer")
def android_developer():
    return render_template("profile-tab.html", services=services)


@app.route("/ios-developer")
def ios_developer():
    return render_template("profile-tab.html", services=services)


@app.route("/postgresql")
def postgresql():
    return render_template("profile-tab.html", services=services)


@app.route("/blockchain-developer")
def blockchain_developer():
    return render_template("profile-tab.html", services=services)


@app.route("/qa-engineer")
def qa_engineer():
    return render_template("profile-tab.html", services=services)


@app.route("/software-architect")
def software_architect():
    return render_template("profile-tab.html", services=services)


@app.route("/cyber-security-specialist")
def cyber_security_specialist():
    return render_template("profile-tab.html", services=services)


@app.route("/ux-ui-designer")
def ux_ui_designer():
    return render_template("profile-tab.html", services=services)


@app.route("/game-developer")
def game_developer():
    return render_template("profile-tab.html", services=services)


@app.route("/technical-writer")
def technical_writer():
    return render_template("profile-tab.html", services=services)


@app.route("/mlops-engineer")
def mlops_engineer():
    return render_template("profile-tab.html", services=services)


@app.route("/product-manager")
def product_manager():
    return render_template("profile-tab.html", services=services)
