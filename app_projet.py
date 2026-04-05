from flask import Flask, render_template, request, redirect, session, url_for
from database import EmergencyDB
import uuid


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
        session['role'] = user['role']
        
        if session['role'] == 'helper':
            return redirect('/helper_dashboard')
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





@app.route('/new_user', methods=['GET', 'POST'])
def new_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('role') 
        
        user_id = db.create_user(username, password, role)
        
        if role == 'patient':
            
            secret_key = str(uuid.uuid4())[:6].upper()
            db.create_profile(user_id, "À remplir", "À remplir", secret_key)
            
        return redirect('/login') 
    return render_template('new_user.html')






#espace personnel-------------------------------------------
@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/login')
    

    profile_data = db.get_profile_by_username(session['username'])
    instructions = db.get_instructions(profile_data['id'])
    
    
    return render_template('own_profile.html', profile=profile_data, instructions=instructions)


@app.route('/update-profile', methods=['POST'])
def update_profile():
    # On récupère les données du formulaire
    p_id = request.form.get('profile_id')
    cond = request.form.get('condition_name')
    cont = request.form.get('emergency_contact')
    
    # On appelle la fonction de database.py
    db.update_profile(p_id, cond, cont)
    
    # On recharge la page du profil pour voir les changements
    return redirect('/profile')

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
    return redirect('/')
    


@app.route('/helper_dashboard')
def helper_dashboard():
    if 'user_id' not in session or session.get('role') != 'helper':
        return redirect('/login')
    
    # On récupère la liste des patients liés à cet accompagnant
    patients = db.get_followed_patients(session['user_id'])
    
    return render_template('helper_dashboard.html', patients=patients)

# Route pour lier un patient à l'accompagnant
@app.route('/link-patient', methods=['POST'])
def link_patient():
    if 'user_id' not in session or session.get('role') != 'helper':
        return redirect('/login')
    
    patient_username = request.form.get('patient_username')
    secret_key = request.form.get('secret_key') 
    
    success = db.link_helper_to_patient(patient_username, secret_key, session['user_id'])
    
    if not success:
        return "Pseudo ou code secret incorrect", 403
    return redirect('/helper_dashboard')

if __name__ == '__main__':
    app.run(debug=True, port=5000)