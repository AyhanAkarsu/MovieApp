from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_mysqldb import MySQL
app = Flask(__name__)
app.secret_key = 'anahtar'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'registerdb'

mysql = MySQL(app)

@app.route("/")
def Anasayfa():
    return render_template("movieapp.html")

@app.route("/login")
def Login():
    return render_template("login.html")

@app.route("/uyelik")
def Uyelik():
    return render_template("register.html")

@app.route("/hakkımda.html")
def Hakkımda():
    return render_template("hakkımda.html")

@app.route("/iletisim.html")
def İletisim():
    return render_template("iletisim.html")


@app.route("/kayit", methods=["POST"])
def kayit():
    if request.method == "POST":
        isim = request.form["isim"]
        soyisim = request.form["soyisim"]
        email = request.form["email"]
        sifre = request.form["sifre"]
        cinsiyet = request.form["cinsiyet"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO uyeler(isim, soyisim, email, sifre, cinsiyet) VALUES (%s, %s, %s, %s, %s)", (isim, soyisim, email, sifre, cinsiyet))
        mysql.connection.commit()
        cur.close()
        return "Kayıt başarılı bir şekilde eklendi."

@app.route("/giris", methods=["GET", "POST"])
def giris():
    if request.method == "POST":
        isim = request.form["isim"]
        sifre = request.form["sifre"]

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM uyeler WHERE isim = %s AND sifre = %s", (isim, sifre))
        kullanıcı = cur.fetchone()
        cur.close()

        if kullanıcı:
            session["user_id"] = kullanıcı[0]
            return "Hoşgeldiniz: " + session["user_id"]
        else:
            flash("E-posta veya şifre yanlış. Lütfen tekrar deneyin.", "danger")
            return render_template("Login.html")



if __name__ == "__main__":
    app.run(debug=True, port = 3306)