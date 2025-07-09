
from flask import Flask, render_template, request, session, redirect, url_for, flash
from pymongo import MongoClient
from bson import ObjectId
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Flask setup
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "default_secret")

# MongoDB setup
mongo_uri = os.getenv("MONGO_URI")
if not mongo_uri:
    raise RuntimeError("MONGO_URI not set")

try:
    # TLS enabled with invalid certificates only for development (not for production)
    client = MongoClient(os.getenv("MONGO_URI"))

    db = client['medicover']

    # Collections
    users = db['users']
    doctors = db['doctors']
    pform = db['pform']
    appointments = db['appointments']
except Exception as e:
    print("MongoDB connection failed:", e)
    raise



@app.route('/')
def home():
  return render_template("paclogin.html")
@app.route("/signup")
def signup():
  return render_template("signup.html")
@app.route("/doctlogin")
def doctlogin1():
  return render_template("doctlogin.html")
@app.route("/doctsignup")
def doctsignup1():
  return render_template("doctsignup.html")
@app.route("/forgotpassword") 
def forgotpassword():
  return render_template("forgotpassword.html")
@app.route("/homepg")
def homepg():
  return render_template("homepg.html")
@app.route("/pharmacy")
def pharmacy():
  return render_template("pharmacy.html")
@app.route("/Aboutus")
def Aboutus():
  return render_template("Aboutus.html")
@app.route("/Reviews")
def Reviews():
  return render_template("Reviews.html")
@app.route("/Contactus")
def Contactus():
  return render_template("Contactus.html")
@app.route("/patientprof")
def patientprof():
  return render_template("patientprof.html")
@app.route("/docthmpg")
def docthmpg():
  return render_template("docthmpg.html")
@app.route("/appointment")
def appointment():
  return render_template("appointment.html")
@app.route("/generaldoct")
def generaldoct():
  return render_template("generaldoct.html")
@app.route("/entdoct")
def entdoct():
  return render_template("entdoct.html")
@app.route("/cardiologydoct")
def cardiologydoct():
  return render_template("cardiologydoct.html")
@app.route("/pulmonarydoct")
def pulmonarydoct():
  return render_template("pulmonarydoct.html")
@app.route("/orthopedicsdoct")
def orthopedicsdoct():
  return render_template("orthopedicsdoct.html")
@app.route("/gynaecologydoct")
def gynaecologydoct():
  return render_template("gynaecologydoct.html")
@app.route("/diabetologydoct")
def diabetologydoct():
  return render_template("diabetologydoct.html")
@app.route("/pregnancydoct")
def pregnancydoct():
  return render_template("pregnancydoct.html")
@app.route("/paediatricsdoct")
def paediatricsdoct():
  return render_template("paediatricsdoct.html")
@app.route("/dermatologydoct")
def dermatologydoct():
  return render_template("dermatologydoct.html")
# signup
@app.route("/signupuser",methods=['post'])
def signupuser():
  a=request.form.get("name")
  b=request.form.get("email")
  c=request.form.get("mobile")
  d=request.form.get("password")
  # e=request.form.get("cpassword")
  user=users.find_one({"email":b})
  if (user):
    return render_template("signup.html",status="already existing email")
  
  users.insert_one({"name":a,"email":b,"mobile":c,"password":d})
  return render_template("paclogin.html")
  
# loginn
@app.route("/loginuser", methods=['GET', 'POST'])
def loginuser():
    if request.method == 'GET':
        return redirect('/login')  # or render_template('paclogin.html')

    a = request.form.get("email")
    b = request.form.get("password")

    user = users.find_one({"email": a})
    if user and user['password'] == b:
        session['email'] = a
        return render_template('homepg.html')
    
    return render_template('paclogin.html', status='invalid credential')



  # doctsignup
@app.route("/doctsignup", methods=['post'])
def doctsignup():
  a=request.form.get("username")
  b=request.form.get("specialization")
  c=request.form.get("experience")
  d=request.form.get("working")
  e=request.form.get("password")
  g=request.form.get("image")

  doctor=doctors.find_one({"username":a})
  if (doctor):
    return render_template("doctsignup.html",status="already existing user")
  
  doctors.insert_one({"username":a,"specialization":b,"experience":c,"working":d,"password":e,"image_url":g})
  return render_template("doctlogin.html")

# doctlogin

@app.route("/doctlogin", methods=['post'])
def doctlogin():
    a = request.form.get("username")
    b = request.form.get("password")
    doctor = doctors.find_one({"username": a})
    if doctor:
        if doctor['password'] == b:
            session['username'] = a
            u = doctors.find_one({"username": a})

            # Get both pending and accepted appointments
            pending = appointments.find({
                "bookeddoctor": a,
                "status": "pending"
            })

            approved = appointments.find({
                "bookeddoctor": a,
                "status": "Accepted"
            })

            return render_template(
                'docthmpg.html',
                data=u,
                data1=pending,
                approved_appointments=approved
            )

    return render_template('doctlogin.html', status='invalid credential')




@app.route("/patientprof1")
def patientprof1():
    a = users.find_one({"email": session['email']}) 
    return render_template("patientprof.html", data=a)


# doct prof
@app.route("/docthmpg1")
def docthmpg1():
  a=doctors.find_one({"username":session['username']})
  return render_template("docthmpg.html")

#pform    
@app.route("/formofpatient", methods=['POST'])
def formofpatient():
    name = request.form.get("fullName")
    gender = request.form.get("gender")
    age = request.form.get("age")
    
    if name and gender and age:
        age = int(age)  # Ensure age is a valid integer
        
        # Insert patient details into the database
        pform.insert_one({"name": name, "gender": gender, "age": age})
        
        # Retrieve the inserted patient details
        patient_data = pform.find_one({"name": name})
        
        # Pass the retrieved patient data to the template
        return render_template("appointment.html", data=patient_data)
    
    # Handle case where form data is invalid
    return render_template("appointment.html")

    
# @app.route("/doctorsheet",methods=['post'])
# # def doctorsheet():
  
  
@app.route("/filterdoctors")
def filter():
  x=request.args.get("type")
  a=doctors.find({"specialization":x})
  return render_template("filtereddoctors.html",data=a)

@app.route("/bookappointment")
def bookapp():
  x=request.args.get("id")
  session['doctor']=x
  return render_template("bookappointment.html")

@app.route("/bookappointment",methods=['post'])
def bookappoint():
  a=request.form.get("appointment_date")
  b=request.form.get("appointment_time")
  c=request.form.get("reason")
  doctor=doctors.find_one({"_id":ObjectId(session['doctor'])})
  appointments.insert_one({"bookeddoctor":doctor['username'],"bookedby":session['email'],"ad":a,"at":b,"reason":c,"status":"pending"})
  y=appointments.find({"bookedby":session['email']})
  return render_template("myappointments.html",documents=y)

@app.route("/myappointments")
def myappointment():
  y=appointments.find({"bookedby":session['email']})
  return render_template("myappointments.html",documents=y)

@app.route("/deleteappointment")
def deleteappoint():
  x=request.args.get("id")
  appointments.delete_one({"_id":ObjectId(x)})
  y=appointments.find({"bookedby":session['email']})
  return render_template("myappointments.html",documents=y) 

@app.route("/acceptappointment")
def accapp():
  x=request.args.get("id")
  appointments.update_one({"_id":ObjectId(x)},{"$set":{"status":"Accepted"}})
  u=doctors.find_one({"username":session['username']})
  x=appointments.find({"bookeddoctor":session['username'],"status":"pending"})
  return render_template('docthmpg.html',data=u,data1=x)

@app.route("/rejectappointment")
def rejapp():
  x=request.args.get("id")
  appointments.update_one({"_id":ObjectId(x)},{"$set":{"status":"Rejected"}})
  u=doctors.find_one({"username":session['username']})
  x=appointments.find({"bookeddoctor":session['username'],"status":"pending"})
  return render_template('docthmpg.html',data=u,data1=x)
  
# search
@app.route("/search")
def search():
    query = request.args.get("query", "").strip()
    if not query:
        return redirect(url_for("homepg"))
    
    # Case-insensitive search in doctor names or specializations
    search_results = doctors.find({
        "$or": [
            {"username": {"$regex": query, "$options": "i"}},
            {"specialization": {"$regex": query, "$options": "i"}}
        ]
    })

    return render_template("filtereddoctors.html", data=search_results)

# logout

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('home'))







if __name__=="__main__":
  app.run(port=2761,debug=True)
  