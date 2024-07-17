from flask import Flask, render_template, request

app = Flask(__name__)



datalist=[]
@app.route('/',methods=['GET','POST'])
def form():
    if request.method == "POST":
        FullName = request.form['fname']
        Email =request.form['email']
        Phone_Number = request.form['pnumber']
        Gender = request.form['gender']
        Username = request.form['uname']
        Password = request.form['pas']
        Con_Password = request.form['cpass']
        infolist=[FullName,Email,Phone_Number,Username,Gender]
        if Password == Con_Password:
            if datalist:
                for user in datalist:
                    if user[1] == Email or user[2]==Phone_Number:
                        msg="Data Already Used"
                        return render_template('fail.html',msg=msg)
                    else:
                        datalist.append(infolist)
                        return render_template('info.html',datalist=datalist)
            else:
                 datalist.append(infolist)
                 return render_template('info.html',datalist=datalist)

        else:
            msg="Resgistrtion Failed"
            return render_template('fail.html',msg=msg)
    else:
        return render_template('index.html')





app.run(debug=True)