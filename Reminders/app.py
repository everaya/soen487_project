from flask import Flask, request, render_template, redirect
import pusher
import models
from database import db_session
from datetime import datetime

app = Flask(__name__)


pusher_client = pusher.Pusher(
    app_id="742788",
    key="d0d46422fb3e9456efd6",
    secret="ab03f23cca860b35e5b7",
    cluster="us2",
    ssl=True)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/reminders_page', methods=["POST", "GET"])
def reminders_page():
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        email = request.form["email"]
        start_time = datetime.strptime(request.form['start_time'], '%d-%m-%Y %H:%M %p')
        end_time = datetime.strptime(request.form['end_time'], '%d-%m-%Y %H:%M %p')

        new_reminder = models.Reminders(title, description, end_time, start_time)
        db_session.add(new_reminder)
        db_session.commit()

        data = {
            "id": new_reminder.id,
            "title": title,
            "description": description,
            "email": email,
            "start_time": request.form['start_time'],
            "end_time": request.form['end_time'],
        }
        pusher_client.trigger('table', 'new-record', {'data': data})

        return redirect("/reminders_page", code=302)
    else:
        reminders = models.Reminders.query.all()
        return render_template('reminders_page.html', reminders=reminders)


@app.route('/edit/<int:id>', methods=["POST", "GET"])
def update_record(id):
    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        email = request.form["email"]
        start_time = datetime.strptime(request.form['start_time'], '%d-%m-%Y %H:%M %p')
        end_time = datetime.strptime(request.form['end_time'], '%d-%m-%Y %H:%M %p')

        update_reminders = models.Reminders.query.get(id)
        update_reminders.title = title
        update_reminders.description = description
        update_reminders.email = email
        update_reminders.start_time = start_time
        update_reminders.end_time = end_time

        db_session.commit()

        data = {
            "id": id,
            "title": title,
            "description": description,
            "email": email,
            "start_time": request.form['start_time'],
            "end_time": request.form['end_time'],
        }

        pusher_client.trigger('table', 'update-record', {'data': data })

        return redirect("/reminders_page", code=302)
    else:
        new_reminder = models.Reminders.query.get(id)
        new_reminder.start_time= new_reminder.start_time.strftime("%d-%m-%Y %H:%M %p")
        new_reminder.end_time = new_reminder.end_time.strftime("%d-%m-%Y %H:%M %p")

        return render_template('update_reminders.html', data=new_reminder)


@app.route('/delete/<int:id>', methods={"GET"})
def delete_record(id):
    item = models.Reminders.query.get(id)
    db_session.delete(item)
    db_session.commit()

    return redirect("/reminders_page", code=302)


# run Flask app
if __name__ == "__main__":
    app.run()