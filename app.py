from flask import Flask, redirect, render_template, request, session,redirect,url_for,g,flash
import random
import subprocess

app = Flask(__name__, static_folder='static')
app.secret_key="123"
class User:
    def __init__(self,id,username,password):
        self.id=id
        self.username=username
        self.password=password

users=[]
users.append(User(id=1,username='syed',password='syed@123'))
users.append(User(id=2,username='raghul',password='raghul@123'))
users.append(User(id=3,username='sasi',password='sasi@123'))

@app.route("/",methods=['GET','POST'])
def login():
    if request.method=='POST':
        uname=request.form['uname']
        upass = request.form['upass']

        for data in users:
            if data.username==uname and data.password==upass:
                session['userid']=data.id
                g.record=1
                return redirect(url_for('index'))
            else:
                g.record=0
        if g.record!=1:
            flash("Username or Password Mismatch...!!!",'danger')
            return redirect(url_for('login'))
    return render_template("login.html")


@app.before_request
def before_request():
    if 'userid' in session:
        for data in users:
            if data.id==session['userid']:
                g.user=data

@app.route('/index')
def index():
    if not g.user:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Function to calculate BMI
def calculate_bmi(weight, height):
    height_meters = height / 100
    bmi = weight / (height_meters ** 2)
    return bmi

def generate_diet_plan(bmi, exercise, weight):
    diet_plan = {}
    if bmi < 18.5:
        diet_plan['level1']='oh no!.. You are Under weight. you have to increase your body weight.'
        diet_plan['breakfast'] = 'High-protein smoothie with spinach, banana, and protein powder.'
        diet_plan['snack'] = 'Greek yogurt with honey and mixed berries.'
        diet_plan['lunch'] = 'Grilled chicken salad with mixed greens, avocado, and olive oil dressing.'
        diet_plan['snack2'] = 'Handful of almonds and an orange.'
        diet_plan['dinner'] = 'Baked fish with quinoa and steamed vegetables.'

         # Generate random exercise counts
        exercise_counts = {}
        min_reps = 5
        max_reps = 8
        exercise_counts['pushup'] = f"4x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['squat'] = f"3x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['Biceps'] = f"3x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['ABS'] = f"3x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['pullup'] = f"2x{random.randint(min_reps, max_reps)} counts"

    elif bmi >= 18.5 and bmi < 25:
        diet_plan['level2']='wow!.. You are fit. You are Normal Weight. you have to maintain your body.'
        diet_plan['breakfast'] = 'Whole grain toast with avocado and poached eggs.'
        diet_plan['snack'] = 'Cottage cheese with pineapple slices.'
        diet_plan['lunch'] = 'Turkey and hummus wrap with whole wheat tortilla.'
        diet_plan['snack2'] = 'Apple slices with peanut butter.'
        diet_plan['dinner'] = 'Grilled tofu with brown rice and stir-fried vegetables.'

         # Generate random exercise counts
        exercise_counts = {}
        min_reps = 8
        max_reps = 10
        exercise_counts['pushup'] = f"3x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['squat'] = f"3x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['Biceps'] = f"3x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['ABS'] = f"3x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['pullup'] = f"1x{random.randint(min_reps, max_reps)} counts"

    else:
        diet_plan['level3']='oh no!.. You are over weight. you have to decrease your body weight.'
        diet_plan['breakfast'] = 'Oatmeal with nuts, seeds, and sliced banana.'
        diet_plan['snack'] = 'Protein shake with almond milk and a banana.'
        diet_plan['lunch'] = 'Lean beef stir-fry with brown rice and broccoli.'
        diet_plan['snack2'] = 'Whole grain crackers with hummus.'
        diet_plan['dinner'] = 'Salmon fillet with quinoa salad and roasted sweet potatoes.'

         # Generate random exercise counts
        exercise_counts = {}
        min_reps = 8
        max_reps = 10
        exercise_counts['pushup'] = f"3x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['squat'] = f"2x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['Biceps'] = f"3x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['ABS'] = f"3x{random.randint(min_reps, max_reps)} counts"
        exercise_counts['pullup'] = f"1x{random.randint(min_reps, max_reps)} counts"

    # Generate random exercise counts
    # exercise_counts = {}
    # min_reps = 8
    # max_reps = 10
    # exercise_counts['pushup'] = f"2x{random.randint(min_reps, max_reps)} repetitions"
    # exercise_counts['squat'] = f"2x{random.randint(min_reps, max_reps)} repetitions"
    # exercise_counts['Biceps'] = f"2x{random.randint(min_reps, max_reps)} repetitions"
    # exercise_counts['ABS'] = f"2x{random.randint(min_reps, max_reps)} repetitions"
    # exercise_counts['pullup'] = f"2x{random.randint(min_reps, max_reps)} repetitions"

    # Map exercise type to video file name
    exercise_videos = {
        'pushup': 'push-up.mp4',
        'squat': 'squat.mp4',
        'pullup': 'pull-up.mp4',
        'Biceps':'BicepsCurl.mp4',
        'ABS':'ABS.mp4'

    }
    video_file = exercise_videos.get(exercise, 'default.mp4')
    
    return diet_plan, exercise_counts, video_file

# Homepage with form to input weight, height, exercise type, and exercise count


# Route to process form submission, calculate BMI, generate diet plan, and display video
@app.route('/generate_plan', methods=['POST'])
def generate_plan():
    weight = float(request.form['weight'])
    height = float(request.form['height'])
    exercise = request.form['exercise']
    exercise_count = {
        'pushup': request.form.get('pushup_count', ''),
        'squat': request.form.get('squat_count', ''),
        'pullup': request.form.get('pullup_count', ''),
        'ABS': request.form.get('ABS_count', ''),
        'Biceps': request.form.get('Biceps_count', '')
    }

    bmi = calculate_bmi(weight, height)
    diet_plan, exercise_counts, video_file = generate_diet_plan(bmi, exercise, exercise_count)

    return render_template('diet_plan.html', bmi=bmi, diet_plan=diet_plan, exercise_counts=exercise_counts, video_file=video_file)
# Route to run the script with provided exercise type and count
@app.route('/run_script', methods=['GET'])
def run_script():
    

    # Run the script with provided command-line arguments
    command = ['python', 'C:\\Users\\Administrator\\Documents\\MEGA\\Python\\fitnesspp\\AI-Fitness-trainer\\main.py', '-t', '-push-up']
    subprocess.run(command)
    
    # Return a message indicating the script has been executed
    return 'Script has been executed successfully.'
if __name__ == '__main__':
    app.run(debug=True)
