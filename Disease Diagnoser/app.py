from flask import Flask,render_template,request,jsonify
from flask_mysqldb import MySQL
import json,pickle,csv

app = Flask(__name__)


 
mysql = MySQL(app)
print(mysql)



@app.route('/')
def get_symp():
    return render_template('index.html')


@app.route('/survey')
def survey():
    return render_template('survey.html')

@app.route('/thanks')
def thanks():
    return render_template('thanks.html')

@app.route('/surveydata',methods=['GET','POST'])
def surveydata():
    if request.method == 'POST':
        data = request.form['checkboxvalue'] 
        data = data.split(',')
       
        with open('datasets\survey.csv', 'a', encoding='UTF8', newline='') as f:
           writer = csv.writer(f)
           writer.writerow(data)
        return jsonify("Successful")


@app.route("/diagnose",methods=["POST","GET"])
def diagnose():  
    
    if request.method == 'POST':
        insert = request.form['checkboxvalue'] 
        
        list = insert.split(',')
        test_list = [int(i) for i in list]
       
        z_list = [0] * 132
        if ((test_list)==z_list):
            msg ="Invalid Data"
        else:
            model = pickle.load(open('model','rb'))
            y_pred = model.predict([test_list])
            print(y_pred)
            msg = y_pred[0]
    else:
        msg = 'Invalid'
    return jsonify(msg)
   
    
    


if __name__ =="__main__":
    app.run(debug=True)