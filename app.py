from flask import Flask,redirect,url_for,render_template,request,redirect,session
import os
from werkzeug.utils import secure_filename
from flask import Flask,render_template,url_for,request
import pandas as pd
import tkinter
from tkinter import messagebox
from tkinter import *
from tkinter import simpledialog
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from tkinter.filedialog import askopenfilename
import numpy as np 
import pandas as pd 
from sklearn import *
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score 
from sklearn.metrics import classification_report 
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

 
UPLOAD_FOLDER = os.path.join('static', 'images')
app=Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'This is your secret key to utilize session in Flask'
@app.route("/")
def main():
    return render_template("main.html")
def logout():
    return redirect(url_for("main"))
@app.route("/passhome")
def passhome():
    
    
    main = tkinter.Tk()
    main.title("Machine Learning Algorithm for detecting and Predicting Fraud in Credit Card Transactions") #designing main screen
    main.geometry("1300x1200")

    global filename
    global cls
    global X, Y, X_train, X_test, y_train, y_test
    global random_acc # all global variables names define in above lines
    global clean
    global attack
    global total
    
    def traintest(train):     #method to generate test and train data from dataset
        X = train.values[:, 0:29] 
        Y = train.values[:, 30]
        print(X)
        print(Y)
        X_train, X_test, y_train, y_test = train_test_split( 
        X, Y, test_size = 0.3, random_state = 0)
        return X, Y, X_train, X_test, y_train, y_test

    def generateModel(): #method to read dataset values which contains all five features data
        global X, Y, X_train, X_test, y_train, y_test
        train = pd.read_csv(filename)
        X, Y, X_train, X_test, y_train, y_test = traintest(train)
        text.insert(END,"Train & Test Model Generated\n\n")
        text.insert(END,"Total Dataset Size : "+str(len(train))+"\n")
        text.insert(END,"Split Training Size : "+str(len(X_train))+"\n")
        text.insert(END,"Split Test Size : "+str(len(X_test))+"\n")



    def upload(): #function to upload tweeter profile
        global filename
        filename = filedialog.askopenfilename(initialdir="dataset")
        text.delete('1.0', END)
        text.insert(END,filename+" loaded\n");



    def prediction(X_test, cls):  #prediction done here
        y_pred = cls.predict(X_test) 
        for i in range(50):
           print("X=%s, Predicted=%s" % (X_test[i], y_pred[i]))
        return y_pred 
	
# Function to calculate accuracy 
    def cal_accuracy(y_test, y_pred, details): 
        accuracy = accuracy_score(y_test,y_pred)*100
        text.insert(END,details+"\n\n")
        text.insert(END,"Accuracy : "+str(accuracy)+"\n\n")
        return accuracy


    def runRandomForest():
        headers = ["Time","V1","V2","V3","V4","V5","V6","V7","V8","V9","V10","V11","V12","V13","V14","V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28","Amount","Class"]
        global random_acc
        global cls
        global X, Y, X_train, X_test, y_train, y_test
        cls = RandomForestClassifier(n_estimators=50,max_depth=2,random_state=0,class_weight='balanced')
        cls.fit(X_train, y_train) 
        text.insert(END,"Prediction Results\n\n") 
        prediction_data = prediction(X_test, cls) 
        random_acc = cal_accuracy(y_test, prediction_data,'Random Forest Accuracy')
    #str_tree = export_graphviz(cls, out_file=None, feature_names=headers,filled=True, special_characters=True, rotate=True, precision=0.6)
    #display.display(str_tree)
    def runKNeighborsClassifier():
        headers = ["Time","V1","V2","V3","V4","V5","V6","V7","V8","V9","V10","V11","V12","V13","V14","V15","V16","V17","V18","V19","V20","V21","V22","V23","V24","V25","V26","V27","V28","Amount","Class"]
        global random_acc
        global cls
        global X, Y, X_train, X_test, y_train, y_test
        cls = KNeighborsClassifier(n_neighbors=50, weights='distance', algorithm='auto', p=2, metric='minkowski')
        cls.fit(X_train, y_train) 
        text.insert(END,"Prediction Results\n\n") 
        prediction_data = prediction(X_test, cls) 
        random_acc = cal_accuracy(y_test, prediction_data,'knn Accuracy')
        #str_tree = export_graphviz(cls, out_file=None, feature_names=headers,filled=True, special_characters=True, rotate=True, precision=0.6)
        #display.display(str_tree)
                


    def predicts():
        global clean
        global attack
        global total
        clean = 0;
        attack = 0;
        text.delete('1.0', END)
        filename = filedialog.askopenfilename(initialdir="dataset")
        test = pd.read_csv(filename)
        test = test.values[:, 0:29]
        total = len(test)
        text.insert(END,filename+" test file loaded\n");
        y_pred = cls.predict(test) 
        for i in range(len(test)):
            if str(y_pred[i]) == '1.0':
               attack = attack + 1
               text.insert(END,"X=%s, Predicted = %s" % (test[i], 'Contains Fraud Transaction Signature')+"\n\n")
            else:
               clean = clean + 1
               text.insert(END,"X=%s, Predicted = %s" % (test[i], 'Transaction Contains Cleaned Signatures')+"\n\n")
     

    def graph():
        height = [total,clean,attack]
        bars = ('Total Transactions','Normal Transaction','Fraud Transaction')
        y_pos = np.arange(len(bars))
        plt.bar(y_pos, height)
        plt.xticks(y_pos, bars)
        plt.show()

    font = ('times', 16, 'bold')
    title = Label(main, text='Machine Learning Algorithm for detecting and Predicting Fraud in Credit Card Transactions')
    title.config(bg='greenyellow', fg='dodger blue')  
    title.config(font=font)           
    title.config(height=3, width=120)       
    title.place(x=0,y=5)

    font1 = ('times', 12, 'bold')
    text=Text(main,height=20,width=150)
    scroll=Scrollbar(text)
    text.configure(yscrollcommand=scroll.set)
    text.place(x=50,y=120)
    text.config(font=font1)


    font1 = ('times', 14, 'bold')
    uploadButton = Button(main, text="Upload Credit Card Dataset", command=upload)
    uploadButton.place(x=50,y=550)
    uploadButton.config(font=font1)  

    modelButton = Button(main, text="Generate Train & Test Model", command=generateModel)
    modelButton.place(x=350,y=550)
    modelButton.config(font=font1) 

    runrandomButton = Button(main, text="Run Random Forest Algorithm", command=runRandomForest)
    runrandomButton.place(x=650,y=550)
    runrandomButton.config(font=font1) 

    runrandomButton = Button(main, text=" Run Knn Algorithm", command=runKNeighborsClassifier)
    runrandomButton.place(x=950,y=550)
    runrandomButton.config(font=font1) 


    predictButton = Button(main, text="Detect Fraud From Test Data", command=predicts)
    predictButton.place(x=50,y=600)
    predictButton.config(font=font1) 

    graphButton = Button(main, text="Clean & Fraud Transaction Detection Graph", command=graph)
    graphButton.place(x=350,y=600)
    graphButton.config(font=font1)

    exitButton = Button(main, text="Exit", command=exit)
    exitButton.place(x=770,y=600)
    exitButton.config(font=font1) 

    main.config(bg='LightSkyBlue')
    main.mainloop()

@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/contact")
def contact():
    return render_template('contact.html')
@app.route("/register",methods=["POST","GET"])
def register():
    
    if request.method=="POST":
        name=request.form["firstname"]
        lname=request.form["lastname"]
        uemail=request.form["email"]
        Password=request.form["password"]
        print(name,lname,uemail,Password)
        import sqlite3
        con=sqlite3.connect("test.db")
        cur=con.cursor()
        table="CREATE TABLE if not exists user (name varchar(255),lastname varchar(255),email varchar(255),password varchar(255))"
        cur.execute(table)
        a=f"select email from user where email='{uemail}'"
        cur.execute(a)
        result=cur.fetchone()
        if result!=None:
            return "email alredy registered"
        else:
        #a="create table emp(name varchar(100),lastname varchar(100),email varchar(100),password varchar(100))"
            cur.execute("INSERT INTO user('name', 'lastname', 'email', 'password') VALUES (?,?,?,?)",(name,lname,uemail,Password))
            con.commit()
            con.close()
            return "successfully registered"
    return render_template("register.html")
 

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        uemail=request.form["email"]
        upassword=request.form["password"]
        print(uemail,upassword)
        import sqlite3
        con=sqlite3.connect("test.db")
        cur=con.cursor()
        a = "SELECT *FROM user WHERE email='"+uemail+"' AND password='"+upassword+"'"
        cur.execute(a)
        result=cur.fetchone()
        print("database",result)
        if result==None:
            return "enter valid details"
        else:
            return redirect(url_for("passhome"))
    return render_template("login.html")
    
@app.route("/logout")
def logout():
    return redirect(url_for("main"))
    
@app.route("/home",methods=["POST","GET"])
def home():
	return render_template('home.html')

 
##########


if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run(debug=True)