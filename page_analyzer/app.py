from flask import Flask, render_template, url_for, redirect, request, flash, get_flashed_messages
from datetime import date
from urllib.parse import urlparse
import psycopg2, os, validators


app = Flask(__name__)
app.secret_key = "super_secret_key"

DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


@app.get('/')
def get_index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/')
def post_index():
    data = request.form.to_dict()
    if validators.url(data['url']):
        p = urlparse(data['url'])
        url = f'{p.scheme}://{p.hostname}'

        cur.execute("SELECT name FROM urls")
        added_urls = cur.fetchall()
        print(added_urls)
        if (url,) in added_urls:
            flash('Страница уже существует', 'info')
            return redirect(url_for('get_index'))

        cur.execute(f"INSERT INTO urls (name, created_at) VALUES ('{url}', '{date.today()}')")
        conn.commit()

        cur.execute(f"SELECT id FROM urls WHERE name = '{url}'")
        id = cur.fetchone()

        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url', id=id[0]))
    flash('Некорректный URL', 'error')
    return redirect(url_for('get_index'))


@app.route('/urls')
def all_urls():
    cur.execute("SELECT * FROM urls ORDER BY id DESC")
    data = cur.fetchall()
    return render_template('urls.html', data=data)


@app.route('/urls/<id>')
def get_url(id):
    messages = get_flashed_messages(with_categories=True)
    cur.execute(f"SELECT * FROM urls WHERE id = {id[0]}")
    data = cur.fetchone()
    return render_template('url.html', messages=messages, data=data)