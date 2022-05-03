from app import app
import qrcode
import random
import string
from app import db
from handlers.handlers import check_url
from flask import flash, render_template, request, redirect, url_for,abort
from threading import Thread

@app.get("/")
def main_page():
    return render_template("index.html")
@app.route("/create", methods=['GET', 'POST'])
def create_page():
    if request.method == 'GET':
        return render_template("create_url.html")
    elif request.method == 'POST':
        from models import URL
        url = request.form['url']
        access_token = random.randrange(10000000, 99999999)
        endpoint_token = str(''.join([random.choice(string.ascii_letters + string.digits  ) for n in range(5)]))
        if check_url(url):
            add_url = URL(
                access_token=access_token,
                url=url,
                endpoint_token = endpoint_token
            )
            db.session.add(add_url)
            db.session.commit()

            img = qrcode.make(url_for("redirect_endpoint",endpoint_token=endpoint_token, _external=True))
            type(img)
            img.save(f'static/src/qr_codes/{access_token}.png')

            return redirect(url_for('panel_dashboard', access_token=access_token))
        else:
            flash("Incorrect format of URL!")
            return redirect(url_for('create_page'))
            
@app.get("/panel/<access_token>")
def panel_dashboard(access_token: int):
    from models import URL
    url = URL.query.filter_by(access_token=access_token).first()
    if url:
        return render_template('panel.html', 
            id = url.id,
            url=url.url, 
            endpoint_token=url.endpoint_token,
            access_token= url.access_token,
            full_info=url.info,
            len_info=len(url.info)
            )
    else:
        return abort(404)


@app.get("/r/<endpoint_token>")
def redirect_endpoint(endpoint_token):
    from models import URL

    url = URL.query.filter_by(endpoint_token=endpoint_token).first()

    if url:
        ip_address = request.remote_addr 
        user_agent = request.headers.get('User-Agent')
        Thread(target = db_insert, args=(ip_address,user_agent, url.id)).start()
        # return redirect(url.url)
        return f"<html><body><p>You will be redirected</p><script>var timer = setTimeout(function() {{window.location='{url.url}'}}, 2);</script></body></html>"
    return abort(404)

def db_insert(ip_address,user_agent, id):
        from models import Target
        info = Target(ip_address, user_agent, id)
        db.session.add(info)
        db.session.commit()
        return 
    
@app.get("/privacy")
def privacy_policy():
    return render_template("privacy.html")

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    platform= request.headers.get('User-Agent')
    return render_template('404.html', platform=platform), 404