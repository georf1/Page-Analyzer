from flask import Flask, render_template, url_for, redirect
from flask import request, flash, get_flashed_messages
from datetime import date
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import psycopg2
import os
import validators
import requests


load_dotenv()

app = Flask(__name__)
app.secret_key = "super_secret_key"

DATABASE_URL = os.getenv('DATABASE_URL')


def make_conn():
    return psycopg2.connect(DATABASE_URL)


def make_check(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, 'html.parser')

    try:
        h1 = soup.h1.text
    except AttributeError:
        h1 = ''

    try:
        title = soup.title.string
    except AttributeError:
        title = ''

    try:
        desc = soup.meta['content']
    except KeyError:
        desc = ''

    return h1, title, desc


@app.get('/')
def get_index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages)


@app.post('/')
def post_index():
    data = request.form.to_dict()
    if validators.url(data['url']):
        conn = make_conn()
        cur = conn.cursor()

        p = urlparse(data['url'])
        url = f'{p.scheme}://{p.hostname}'

        cur.execute("SELECT name FROM urls")
        added_urls = cur.fetchall()
        if (url,) in added_urls:
            cur.execute("SELECT id FROM urls WHERE name=%s", (url,))
            id = cur.fetchone()

            conn.close()

            flash('Страница уже существует', 'info')
            return redirect(url_for('get_url', id=id[0]))

        cur.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s)",
                    (url, date.today()))
        conn.commit()

        cur.execute("SELECT id FROM urls WHERE name=%s", (url,))
        id = cur.fetchone()

        conn.close()

        flash('Страница успешно добавлена', 'success')
        return redirect(url_for('get_url', id=id[0]))
    flash('Некорректный URL', 'error')
    return redirect(url_for('get_index'))


@app.route('/urls')
def get_urls():
    conn = make_conn()
    cur = conn.cursor()

    cur.execute("SELECT DISTINCT ON (urls.id) urls.id, urls.name, "
                "url_checks.created_at, url_checks.status_code FROM urls "
                "LEFT JOIN url_checks ON urls.id = url_checks.url_id "
                "ORDER BY urls.id DESC")
    data = cur.fetchall()

    conn.close()
    return render_template('urls.html', data=data)


@app.route('/urls/<id>')
def get_url(id):
    messages = get_flashed_messages(with_categories=True)
    conn = make_conn()
    cur = conn.cursor()

    cur.execute("SELECT * FROM urls WHERE id=%s", (id[0],))
    data = cur.fetchone()

    cur.execute("SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC",
                (id[0],))
    checks = cur.fetchall()

    conn.close()
    return render_template('url.html', messages=messages, data=data,
                           checks=checks)


@app.post('/urls/<id>/checks')
def post_check(id):
    conn = make_conn()
    cur = conn.cursor()

    cur.execute("SELECT name FROM urls WHERE id=%s", (id,))
    url = cur.fetchone()

    try:
    response = requests.get(url[0])
    response.raise_for_status()
    except requests.exceptions.RequestException:
        conn.close()

        flash('Произошла ошибка при проверке', 'error')
        return redirect(url_for('get_url', id=id))

    h1, title, desc = make_check(url[0])
    cur.execute("INSERT INTO url_checks "
                "(url_id, status_code, h1, title, description, created_at) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (id, resp.status_code, h1, title, desc, date.today()))
    conn.commit()

    conn.close()

    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url', id=id))
