from flask import Flask, render_template, request, redirect, url_for, session,flash
from flaskext.mysql import MySQL
import pymysql
from flask import redirect
import re
  
app = Flask(__name__)
  
  
app.secret_key = 'your secret key'
  

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'etudiants_bd'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''


    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT * FROM accounts WHERE username = % s AND password = % s", (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email']=account['email']
            fct=account['fonction']
            msg = 'conexion est bien établit !'
            if fct=='Admin':
                return render_template('index1.html', msg = msg)
            elif fct=='Etudiant' :
                return render_template('index_etudiant.html', msg = msg)
            #return """<a href="app.py">Retour à la page d'accueil</a>"""
            #url_for("http://127.0.0.1:5000/app.py")
        else:
            msg = 'Incorrect nom utilisateur / password !'
    return render_template('login.html', msg = msg)
  
@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/interface1')
def interface1():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT DISTINCT niveau FROM classe')
    data = cur.fetchall()
    cur.close()
    return render_template('interface1.html', classe = data)

@app.route('/Index')
def Index():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT DISTINCT niveau FROM classe')
    data = cur.fetchall()
    cur.close()
    cur2 = connection.cursor(pymysql.cursors.DictCursor)
    cur2.execute('SELECT DISTINCT spécialité FROM classe')
    data2 = cur2.fetchall()
    cur2.close()
    return render_template('index.html', classe = data, classe2=data2)
 
@app.route('/Index/add_etudiants', methods=['POST'])
def add_etudiants():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        cinnumber = request.form['cinnumber']
        phone = request.form['phone']
        adresse = request.form['adresse']
        email = request.form['email']
        niveau = request.form['niveau']
        classe = request.form['classe']
        cur.execute("INSERT INTO etudiants (nom,prénom,cin,num_tlf,adresse,email, niveau, classe) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)", (firstname,lastname,cinnumber,phone,adresse, email,niveau, classe))
        connection.commit()
        flash('Etudiant est bien ajouté')
        return redirect(url_for('Index'))

@app.route('/Index5')
def Index5():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM classe')
    data = cur.fetchall()
    cur.close()
    return render_template('ajouter_classe.html', classe = data)

@app.route('/ajouter_classe', methods=['POST', 'GET'])
def ajouter_classe():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        niveau = request.form['niveau']
        spécialité = request.form['spécialité']
        salle = request.form['salle']
        cur.execute("INSERT INTO classe (niveau, spécialité, salle) VALUES (%s,%s,%s)", (niveau, spécialité,salle))
        connection.commit()
        flash('La nouvelle classe est créée')
        #return render_template('ajouter_matière.html', matière = data)
        return redirect(url_for('Index5'))
      #njareb nrod formulaire get w hedhom lkol get
        #matiere.html hiya elli bech nafficher feha les matieres lkol notes par etudiants 

@app.route('/Index2')
def Index2():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
 
    cur.execute('SELECT * FROM etudiants')
    data = cur.fetchall()
  
    cur.close()
    return render_template('index2.html', etudiants = data)

@app.route('/Index2/edit/<id>', methods = ['POST', 'GET'])
def get_etudiants(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM etudiants WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    cur1 = connection.cursor(pymysql.cursors.DictCursor)
    cur1.execute('SELECT DISTINCT niveau FROM classe')
    data1 = cur1.fetchall()
    cur.close()
    cur2 = connection.cursor(pymysql.cursors.DictCursor)
    cur2.execute('SELECT DISTINCT spécialité FROM classe')
    data2 = cur2.fetchall()
    cur2.close()
    return render_template('edit.html', etudiants = data[0], classe1 = data1, classe2 = data2)
 
@app.route('/Index2/update/<id>', methods=['POST'])
def update_etudiants(id):
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        cinnumber = request.form['cinnumber']
        phone = request.form['phone']
        adresse = request.form['adresse']
        email = request.form['email']
        niveau = request.form['niveau']
        classe = request.form['classe']
        connection = mysql.connect()
        cur = connection.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE etudiants
            SET nom = %s,
                prénom = %s,
                cin = %s,
                num_tlf = %s,
                adresse = %s,
                email = %s,
                niveau = %s,
                classe = %s
                
            WHERE id = %s
        """, (firstname,lastname,cinnumber,phone,adresse, email,niveau,classe, id))
        flash('Etudiant est bien modifié')
        connection.commit()
       # msg = 'Etudiant modifié avec succès'
        return redirect(url_for('interface1')) 
        #nwali lena selon ye na3mel update w delete lkol classe wa7dou 
        #ye ntester selon l valeur de niveau et classe naamel redirect spécialité
        #madem kol wehed aandou spécialité hiya nafsha index2 bensba liya donc naamel kol delete w update lkol spécialité elli houma barcha :( 
 
@app.route('/Index2/delete/<string:id>', methods = ['POST','GET'])
def delete_etudiants(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE FROM etudiants WHERE id = {0}'.format(id))
    flash('Etudiant supprimé avec succès')
    connection.commit()
    #msg='Etudiant supprimé avec succès'
    return redirect(url_for('interface1'))

  
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form and 'fonction' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        fonction = request.form['fonction']
        connection = mysql.connect()
        cursor = connection.cursor(pymysql.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Compte déja existe '
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'E-mail non valide !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Nom utilisateur doit contenir uniquement des lettres et des chiffres !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, % s, % s, % s, % s)', (username, password, email,fonction, ))
            connection.commit()
            msg = 'Votre compte est créé avec succès !'
    elif request.method == 'POST':
        msg = 'Veuiller remplir tous les champs !'
    return render_template('register.html', msg = msg)

@app.route('/Index3')
def Index3():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM matière')
    data = cur.fetchall()
    cur.close()
    return render_template('ajouter_matière.html', matière = data)

@app.route('/IndexMat/<cin>')
def IndexMat(cin):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT DISTINCT cin_etudiant FROM matière where cin_etudiant=%s',(cin))
    data = cur.fetchall()
    cur.close()
    cur1 = connection.cursor(pymysql.cursors.DictCursor)
    cur1.execute('SELECT DISTINCT titre FROM etudiants e , module m WHERE e.niveau=m.cycle AND e.cin=%s',(cin))
    data1 = cur1.fetchall()
    cur1.close()
    cur2 = connection.cursor(pymysql.cursors.DictCursor)
    cur2.execute('SELECT DISTINCT titre_mat FROM etudiants e , module m , matièreparmodule mat WHERE e.niveau=m.cycle AND m.titre=mat.module AND m.cycle=e.niveau AND e.cin=%s',(cin))
    data2 = cur2.fetchall()
    cur2.close()
    return render_template('ajouter_matière.html', matière1 = data,mod=data1, mat=data2)

@app.route('/ajouter_matière', methods=['POST', 'GET'])
def ajouter_matière():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        m_module = request.form['m_module']
        nom_m = request.form['nom_m']
        note_EXAM = float (request.form['note_EXAM'])
        coeff_EXAM = float(request.form['coeff_EXAM'])
        note_DS = float (request.form['note_DS'])
        coeff_DS = float(request.form['coeff_DS'])
        note_TP = float (request.form['note_TP'])
        coeff_TP = float(request.form['coeff_TP'])
        coeff_matière= int(request.form['coeff_matière'])
        Moy=float((note_EXAM*coeff_EXAM)+(note_DS*coeff_DS)+(note_TP*coeff_TP))
        MoyMultCoeff=float(Moy*float (coeff_matière))
        CIN=request.form['cin']
        cur.execute("INSERT INTO matière (module, nom, examen, coeff_EXAM, DS, coeff_DS, TP, coeff_TP, coeff_matière, moyenne, cin_etudiant,MoyMultCoeff) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (m_module, nom_m,note_EXAM,coeff_EXAM,note_DS,coeff_DS,note_TP,coeff_TP,coeff_matière, Moy, CIN,MoyMultCoeff))
        connection.commit()
        flash('La matière et les notes correspandantes sont bien ajoutées')
        #return render_template('ajouter_matière.html', matière = data)
        return redirect(url_for('interface1'))
      #njareb nrod formulaire get w hedhom lkol get
        #matiere.html hiya elli bech nafficher feha les matieres lkol notes par etudiants 
@app.route('/Index4')
def Index4():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM matière')
    data = cur.fetchall()
    cur.close()
    return render_template('ajouter_matière_sans_TP.html', matière = data)

@app.route('/IndexMatSTP/<cin>')
def IndexMatSTP(cin):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT DISTINCT cin_etudiant FROM matière where cin_etudiant=%s',(cin))
    data = cur.fetchall()
    cur.close()
    cur1 = connection.cursor(pymysql.cursors.DictCursor)
    cur1.execute('SELECT DISTINCT titre FROM etudiants e , module m WHERE e.niveau=m.cycle AND e.cin=%s',(cin))
    data1 = cur1.fetchall()
    cur1.close()
    cur2 = connection.cursor(pymysql.cursors.DictCursor)
    cur2.execute('SELECT DISTINCT titre_mat FROM etudiants e , module m , matièreparmodule mat WHERE e.niveau=m.cycle AND m.titre=mat.module AND m.cycle=e.niveau AND e.cin=%s',(cin))
    data2 = cur2.fetchall()
    cur2.close()
    return render_template('ajouter_matière_sans_TP.html', matière2 = data,mod=data1, mat=data2)

@app.route('/ajouter_matière_sans_TP', methods=['POST', 'GET'])
def ajouter_matière_sans_TP():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        m_module = request.form['m_module']
        nom_m = request.form['nom_m']
        note_EXAM = float (request.form['note_EXAM'])
        coeff_EXAM = float(request.form['coeff_EXAM'])
        note_DS = float (request.form['note_DS'])
        coeff_DS = float(request.form['coeff_DS'])
        note_TP = '--'
        coeff_TP = '--'
        coeff_matière= int(request.form['coeff_matière'])
        Moy=float((note_EXAM*coeff_EXAM)+(note_DS*coeff_DS))
        MoyMultCoeff=float(Moy*float (coeff_matière))
        CIN=request.form['cin']
        cur.execute("INSERT INTO matière (module, nom, examen, coeff_EXAM, DS, coeff_DS, TP, coeff_TP, coeff_matière, moyenne, cin_etudiant,MoyMultCoeff) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (m_module,nom_m,note_EXAM,coeff_EXAM,note_DS,coeff_DS,note_TP,coeff_TP,coeff_matière, Moy, CIN,MoyMultCoeff))
        connection.commit()
        flash('La matière et les notes correspandantes sont bien ajoutées')
        #return render_template('ajouter_matière.html', matière = data)
        return redirect(url_for('Index4'))
      #njareb nrod formulaire get w hedhom lkol get
        #matiere.html hiya elli bech nafficher feha les matieres lkol notes par etudiants 

@app.route('/index2/affiche_matière/<cin>',methods = ['POST', 'GET'])
def affiche_matière(cin):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    #print("You said: " + request.args.get('cin', ''))
    cur.execute('SELECT * FROM matière where cin_etudiant=%s',(cin))
    data = cur.fetchall()
    cur.close()
    cur2 = connection.cursor(pymysql.cursors.DictCursor)
    cur2.execute('SELECT DISTINCT cin_etudiant FROM matière where cin_etudiant=%s',(cin))
    data2 = cur2.fetchall()
    cur2.close()
    return render_template('matiére.html', matière = data, matièrePE=data2)

@app.route('/classes/<niveau>')
def classes(niveau):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    #print("You said: " + request.args.get('cin', ''))
    cur.execute('SELECT * FROM classe where niveau=%s',(niveau))
    data = cur.fetchall()
    cur.close()
    cur1= connection.cursor(pymysql.cursors.DictCursor)
    cur1.execute('SELECT DISTINCT niveau FROM classe where niveau=%s',(niveau))
    data1 = cur1.fetchall()
    cur1.close()
    return render_template('classes.html', classes = data, classes1 = data1)

@app.route('/filiere/<sp>')
def filiere(sp):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM etudiants where classe=%s',(sp))
    data = cur.fetchall()
    cur.close()
    return render_template('spécialité.html', filiere = data)

@app.route('/interface_etudiant/<mail>')
def interface_etudiant(mail):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT distinct cin FROM etudiants where email=%s',(mail))
    data = cur.fetchall()
    cur.close()
    return render_template('interface_etudiant.html', interf_etud = data)

@app.route('/espace_etudiant/<cin>')
def espace_etudiant(cin):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM matière where cin_etudiant=%s',(cin))
    data = cur.fetchall()
    cur.close()
    cur2 = connection.cursor(pymysql.cursors.DictCursor)
    cur2.execute('SELECT SUM(coeff_matière)AS sumy1 FROM matière where cin_etudiant=%s',(cin))
    total1 = cur2.fetchone()
    total1 = total1["sumy1"]
    cur2.close()
    cur3 = connection.cursor(pymysql.cursors.DictCursor)
    cur3.execute('SELECT SUM(MoyMultCoeff)AS sumy FROM matière where cin_etudiant=%s',(cin))
    total = cur3.fetchone()
    total = total["sumy"]
    cur3.close()
    moy_général=float(total)/float(total1)
    return render_template('consulter_notes.html', esp_etud = data, moy_général=moy_général)

@app.route('/Index3/delete/<string:id>', methods = ['POST','GET'])
def delete_matière(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
  
    cur.execute('DELETE FROM matière WHERE id = {0}'.format(id))
    flash('La matière supprimé avec succès')
    connection.commit()
    return redirect(url_for('interface1'))

@app.route('/Index3/edit/<id>', methods = ['POST', 'GET'])
def get_matière(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM matière WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_matière.html', matière = data[0])
 
@app.route('/Index3/update/<id>', methods=['POST'])
def update_matière(id):
    if request.method == 'POST':
        nom_m = request.form['nom_m']
        note_EXAM = float (request.form['note_EXAM'])
        coeff_EXAM = float(request.form['coeff_EXAM'])
        note_DS = float (request.form['note_DS'])
        coeff_DS = float(request.form['coeff_DS'])
        note_TP = request.form['note_TP']
        coeff_TP = request.form['coeff_TP']
        coeff_matière= int(request.form['coeff_matière'])
        cin_etudiant = request.form['cin_etudiant']
    if (note_TP=='--' and coeff_TP=='--'):
        Moy=float((note_EXAM*coeff_EXAM)+(note_DS*coeff_DS))
        MoyMultCoeff=float(Moy*float (coeff_matière))
        connection = mysql.connect()
        cur = connection.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE matière
            SET nom = %s,
                examen = %s,
                coeff_EXAM = %s,
                DS = %s,
                coeff_DS = %s,
                TP = %s,
                coeff_TP = %s,
                coeff_matière = %s,
                moyenne = %s,
                cin_etudiant = %s,
                MoyMultCoeff=%s
                
            WHERE id = %s
        """, (nom_m,note_EXAM,coeff_EXAM,note_DS,coeff_DS,note_TP,coeff_TP,coeff_matière,Moy,cin_etudiant,MoyMultCoeff, id))
        flash('matière est bien modifié')
        connection.commit()
       # msg = 'Etudiant modifié avec succès'
        return redirect(url_for('interface1')) 
        #modifi mat sans tp wa7dha
    else :  
        Moy=float((note_EXAM*coeff_EXAM)+(note_DS*coeff_DS)+(float(note_TP)*float(coeff_TP)))
        MoyMultCoeff=float(Moy*float (coeff_matière))
        connection = mysql.connect()
        cur = connection.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE matière
            SET nom = %s,
                examen = %s,
                coeff_EXAM = %s,
                DS = %s,
                coeff_DS = %s,
                TP = %s,
                coeff_TP = %s,
                coeff_matière = %s,
                moyenne = %s,
                cin_etudiant = %s,
                MoyMultCoeff=%s
                
            WHERE id = %s
        """, (nom_m,note_EXAM,coeff_EXAM,note_DS,coeff_DS,note_TP,coeff_TP,coeff_matière,Moy,cin_etudiant,MoyMultCoeff, id))
        flash('matière est bien modifié')
        connection.commit()
        return redirect(url_for('interface1')) 

@app.route('/index2/bulltein/<cin>',methods = ['POST', 'GET'])
def bulltein(cin):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM matière where cin_etudiant=%s',(cin))
    data = cur.fetchall()
    cur.close()
    cur2 = connection.cursor(pymysql.cursors.DictCursor)
    cur2.execute('SELECT SUM(coeff_matière)AS sumy1 FROM matière where cin_etudiant=%s',(cin))
    total1 = cur2.fetchone()
    total1 = total1["sumy1"]
    cur2.close()
    cur3 = connection.cursor(pymysql.cursors.DictCursor)
    cur3.execute('SELECT SUM(MoyMultCoeff)AS sumy FROM matière where cin_etudiant=%s',(cin))
    total = cur3.fetchone()
    total = total["sumy"]
    cur3.close()
    moy_général=float(total)/float(total1)
    return render_template('bulltein.html', matière = data , moy_général=moy_général)

@app.route('/IndexModule')
def IndexModule():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM module')
    data = cur.fetchall()
    cur.close()
    cur1 = connection.cursor(pymysql.cursors.DictCursor)
    cur1.execute('SELECT DISTINCT niveau FROM classe')
    data1 = cur1.fetchall()
    cur1.close()
    return render_template('index_module.html', module = data, cycle_module=data1)

@app.route('/ajouter_module', methods=['POST', 'GET'])
def ajouter_module():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        titre = request.form['titre']
        cycle = request.form['cycle']
        cur.execute("INSERT INTO module (titre,cycle) VALUES (%s,%s)", (titre, cycle))
        connection.commit()
        flash('Le nouveau module est créée')
        return redirect(url_for('interface1'))

@app.route('/interface_module/<niveau>')
def interface_module(niveau):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT DISTINCT titre FROM module where cycle=%s',(niveau))
    data = cur.fetchall()
    cur.close()
    cur1 = connection.cursor(pymysql.cursors.DictCursor)
    cur1.execute('SELECT DISTINCT cycle FROM module where cycle=%s',(niveau))
    data1 = cur1.fetchall()
    cur.close()
    return render_template('interface_module.html', module = data, module2 = data1)

@app.route('/module/<nom_module>')
def module(nom_module):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM matièreparmodule where module=%s',(nom_module))
    data = cur.fetchall()
    cur.close()
    return render_template('module_matière.html', module_matière = data)

@app.route('/gérer_modules')
def gérer_modules():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM module')
    data = cur.fetchall()
    cur.close()
    return render_template('gérer_modules.html', gérer_module = data)

@app.route('/gérer_modules/delete/<string:id>', methods = ['POST','GET'])
def delete_module(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM module WHERE id = {0}'.format(id))
    flash('Lae module supprimé avec succès')
    connection.commit()
    return redirect(url_for('gérer_modules'))

@app.route('/gérer_modules/edit/<id>', methods = ['POST', 'GET'])
def get_module(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM module WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_module.html', module = data[0])
 
@app.route('/gérer_modules/update/<id>', methods=['POST'])
def update_module(id):
    if request.method == 'POST':
        titre = request.form['titre']
        cycle= request.form['cycle']
        connection = mysql.connect()
        cur = connection.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE module
            SET titre = %s,
                cycle = %s                
            WHERE id = %s
        """, (titre,cycle,id))
        flash('module est bien modifié')
        connection.commit()
        return redirect(url_for('gérer_modules')) 


@app.route('/gérer_classes')
def gérer_classes():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM classe')
    data = cur.fetchall()
    cur.close()
    return render_template('gérer_classes.html', gérer_classes = data)

@app.route('/gérer_classes/delete/<string:id>', methods = ['POST','GET'])
def delete_classe(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM classe WHERE id = {0}'.format(id))
    flash('Lae module supprimé avec succès')
    connection.commit()
    return redirect(url_for('gérer_modules'))

@app.route('/gérer_classes/edit/<id>', methods = ['POST', 'GET'])
def get_classe(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM classe WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_classe.html', classe = data[0])
 
@app.route('/gérer_classes/update/<id>', methods=['POST'])
def update_classe(id):
    if request.method == 'POST':
        niveau = request.form['niveau']
        spécialité = request.form['spécialité']
        salle= request.form['csalle']
        connection = mysql.connect()
        cur = connection.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE classe
            SET niveau = %s,
                spécialité = %s,
                salle=%s                
            WHERE id = %s
        """, (niveau,spécialité,salle,id))
        flash('module est bien modifié')
        connection.commit()
        return redirect(url_for('gérer_classes')) 


@app.route('/Index6/<cycle>')
def Index6(cycle):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM matièreParModule')
    data = cur.fetchall()
    cur.close()
    cur1 = connection.cursor(pymysql.cursors.DictCursor)
    cur1.execute('SELECT DISTINCT titre FROM module WHERE cycle=%s',(cycle))
    data1 = cur1.fetchall()
    cur1.close()
    return render_template('ajouter_matière_module.html', matière = data, module=data1)



@app.route('/ajouter_matière_module', methods=['POST', 'GET'])
def ajouter_matière_module():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)

    if request.method == 'POST':
        nom_m = request.form['nom_m']
        coeff_EXAM = request.form['coeff_EXAM']
        coeff_DS = request.form['coeff_DS']
        coeff_TP = request.form['coeff_TP']
        module= request.form['module']
        coeff_matière= request.form['coeff_matière']
        cur.execute("INSERT INTO matièreParModule (titre_mat,  coeff_EXAM,  coeff_DS,  coeff_TP,module, coeff_matière) VALUES (%s,%s,%s,%s,%s,%s)", (nom_m,coeff_EXAM,coeff_DS,coeff_TP,module,coeff_matière))
        connection.commit()
        flash('La matière est bien ajoutée')
        return redirect(url_for('interface1'))
 

@app.route('/Index6/delete/<string:id>', methods = ['POST','GET'])
def delete_matière_module(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM matièreParModule WHERE id = {0}'.format(id))
    flash('La matière supprimé avec succès')
    connection.commit()
    return redirect(url_for('interface1'))

@app.route('/Index6/edit/<id>', methods = ['POST', 'GET'])
def get_matière_module(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM matièreparmodule WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    cur1 = connection.cursor(pymysql.cursors.DictCursor)
    cur1.execute('SELECT DISTINCT titre FROM module')
    data1 = cur1.fetchall()
    cur1.close()
    print(data[0])
    return render_template('edit_matière_module.html', matièreparmodule = data[0], module=data1)
 
@app.route('/Index6/update/<id>', methods=['POST'])
def update_matière_module(id):
    if request.method == 'POST':
        nom_m = request.form['nom_m']
        coeff_EXAM = request.form['coeff_EXAM']
        coeff_DS = request.form['coeff_DS']
        coeff_TP = request.form['coeff_TP']
        module= request.form['module']
        coeff_matière= request.form['coeff_matière']
        connection = mysql.connect()
        cur = connection.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE matièreparmodule
            SET titre_mat = %s,
                coeff_EXAM = %s,
                coeff_DS = %s,
                coeff_TP = %s,
                module=%s,
                coeff_matière = %s
                
            WHERE id = %s
        """, (nom_m,coeff_EXAM,coeff_DS,coeff_TP,module, coeff_matière,id))
        flash('matière est bien modifié')
        connection.commit()
        return redirect(url_for('interface1')) 


@app.route('/liste_utilisateur')
def liste_utilisateur():
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM accounts')
    data = cur.fetchall()
    cur.close()
    return render_template('liste_utilisateur.html', utilisateur = data)

@app.route('/liste_utilisateur/delete/<string:id>', methods = ['POST','GET'])
def delete_utilisateur(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('DELETE FROM accounts WHERE id = {0}'.format(id))
    flash('Utilisateur supprimé avec succès')
    connection.commit()
    return redirect(url_for('liste_utilisateur'))

@app.route('/liste_utilisateur/edit/<id>', methods = ['POST', 'GET'])
def get_utilisateur(id):
    connection = mysql.connect()
    cur = connection.cursor(pymysql.cursors.DictCursor)
    cur.execute('SELECT * FROM accounts WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit_utilisateur.html', utilisateur = data[0])
 
@app.route('/liste_utilisateur/update/<id>', methods=['POST'])
def update_utilisateur(id):
    if request.method == 'POST':
        username = request.form['username']
        password= request.form['password']
        email= request.form['email']
        connection = mysql.connect()
        cur = connection.cursor(pymysql.cursors.DictCursor)
        cur.execute("""
            UPDATE accounts
            SET username = %s,
                password = %s,
                email=%s               
            WHERE id = %s
        """, (username,password,email,id))
        flash('utilisateur est bien modifié')
        connection.commit()
        return redirect(url_for('liste_utilisateur')) 
