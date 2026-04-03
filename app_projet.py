from flask import Flask, render_template, request, redirect, session, url_for
from database import EmergencyDB


app = Flask(__name__)
app.secret_key = 'concombre'
db = EmergencyDB()

#page d'accueuil---------------------------------------------
@app.route('/')
def index():
    return render_template('index.html')



#page d'authentification-------------------------------------
@app.route('/login')
def login_form():
    return render_template('login.html')

@app.route('/do-login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = db.get_user(username)
    
    if user and user['password'] == password:
        session['user_id'] = user['id']
        session['username'] = user['username']
        return redirect('/profile')
    return "Erreur d'authentification", 401


#vue d'urgence (publique)-----------------------------------
@app.route('/emergency/<username>')
def emergency_view(username):
    # Comme movies_db.read(id), on lit le profil par le username
    profile = db.get_profile_by_username(username)
    if profile:
        instructions = db.get_instructions(profile['id'])
        return render_template('emergency_view.html', profile=profile, instructions=instructions)
    return "Profil non trouvé", 404


#espace personnel-------------------------------------------
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    
    profile_data = db.get_profile_by_username(session['username'])
    instructions = db.get_instructions(profile_data['id'])
    return render_template('own_profile.html', profile=profile_data, instructions=instructions)




#ajout instructions-----------------------------------------
@app.route('/add-instruction', methods=['POST'])
def add_instruction():
    if 'user_id' not in session:
        return redirect('/login')
    
    profile_id = request.form.get('profile_id')
    symptom = request.form.get('symptom')
    action = request.form.get('action')
    
    db.add_instruction(int(profile_id), symptom, action)
    return redirect('/profile')


#supprimer instructions-------------------------------------
@app.route('/delete-instruction/<id>')
def delete_instruction(id):
    if 'user_id' not in session:
        return redirect('/login')
    
    db.delete_instruction(int(id))
    return redirect('/profile')

@app.route('/logout')
def logout():
    session.clear()
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)