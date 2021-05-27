from  flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
#MYSQL CONEXION
app.config['MYSQL_HOST']= 'localhost'
app.config['MYSQL_USER']= 'root'
app.config['MYSQL_PASSWORD']= ''
app.config['MYSQL_DB']= 'flaskcontacts'
mysql = MySQL(app)
#INICIO SESION
app.secret_key = 'mysecretkey'

@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)
#Ruta de la seccion de contactos para utilizar el metodo POST
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) values (%s,%s,%s)',(fullname,phone,email))
        mysql.connection.commit()
        flash('CONTACTO AGREGADO !')
        return redirect(url_for('index'))

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('select * from contacts where id = %s',(id))
    data = cur.fetchall()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>' , methods = ['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']
    cur = mysql.connection.cursor()
    cur.execute(""" 
    UPDATE contacts SET fullname = %s, email = %s, phone = %s where id = %s
    """, (fullname,email,phone,id))
    mysql.connection.commit()
    flash('Contacto Actualizado Satisfactoriamente ! ')    
    return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
   cur = mysql.connection.cursor()
   cur.execute('delete from contacts where id = {0}'.format(id))
   mysql.connection.commit()
   flash('Contacto Eliminado')
   return redirect(url_for('index'))
if __name__ == '__main__':
 app.run(port = 3000, debug = True)