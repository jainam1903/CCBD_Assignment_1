from flask import Flask, render_template, request
import csv
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        # Handle the uploaded image
        image = request.files['image']
        # Save the image or process it as needed
        # ...
        save_path = os.path.join(CURRENT_DIR, 'static', image.filename)
        image.save(save_path)
        return 'Image uploaded successfully!'

    return render_template('upload_image.html')




@app.route('/upload_csv', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # File handling code here
        file = request.files['csfile']
        # Process the uploaded file
        # For example, save it to a specific location
        save_path = os.path.join(CURRENT_DIR, 'static', file.filename)
        file.save(save_path)        
        return 'File uploaded successfully'

    return render_template('upload_csv.html')

@app.route("/search", methods=['GET', 'POST'])
def search():
    return render_template('search.html')


@app.route("/searchimage", methods=['GET', 'POST'])
def searchimage():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/people.csv'))
        temp_path = ''
        for r in csv_reader:
            if name == r['Name']:
                temp_path = '../static/' + r['Picture']
        if temp_path != '':
            return render_template('search.html', image_path=temp_path, message="found")
        else:
            return render_template('search.html', error="Picture did not find!")


@app.route("/searchbysal", methods=['GET', 'POST'])
def searchbysal():
    csv_reader = csv.DictReader(open('static/people.csv'))
    temp_path = []

    for r in csv_reader:
        if r['Salary'] == '' or r['Salary'] == ' ':
            r['Salary'] = 99000;
        if int(float(r['Salary'])) < 99000:
            if r['Picture'] != ' ':
                temp_path.append('static/' + r['Picture'])
                print(temp_path)
                print(int(float(r['Salary'])))

    print(len(temp_path))
    if temp_path != '':
        return render_template('searchbysal.html', image_path=temp_path, message="found")
    else:
        return render_template('searchbysal.html', error="Picture did not find!")


@app.route("/edit", methods=['GET', 'POST'])
def edit():
    return render_template('edit.html')


@app.route("/editdetails", methods=['GET', 'POST'])
def editdetails():
    if request.method == 'POST':
        name = request.form['name']
        csv_reader = csv.DictReader(open('static/people.csv'))
        temp_name = ''
        for r in csv_reader:
            if name == r['Name']:
                temp_name = name
        if temp_name != '':
            return render_template('display.html', name=temp_name)
        else:
            return render_template('display.html', error="No Record Found!")


@app.route("/updatedetails", methods=['GET', 'POST'])
def updatedetails():
    if request.method == 'POST':
        name = request.form['name']
        state = request.form['state']
        salary = request.form['salary']
        grade = request.form['grade']
        room = request.form['room']
        pic = request.files['picture']
        keyword = request.form['keyword']
        cnt = 0
        picture = pic.filename

        temp = [name, state, salary, grade, room, picture, keyword]
        line = list()

        with open('static/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                if name == r[0]:
                    line.append(temp)
                    # pic.save('static/' + pic.filename)
                else:
                    line.append(r)
                cnt += 1

            csv_write = open('static/people.csv', 'w')
            for i in line:
                for j in i:
                    csv_write.write(j + ',')
                csv_write.write('\n')

            if cnt != 0:
                return render_template('display.html', update="One Record Updated Successfully.")
            else:
                return render_template('display.html', error="No Record Found!")


@app.route("/remove", methods=['GET', 'POST'])
def remove():
    return render_template('remove.html')

@app.route("/removedetails", methods=['GET', 'POST'])
def removedetails():
    if request.method == 'POST':
        name = request.form['name']
        cnt = 0
        line = list()
        with open('static/people.csv', 'r') as f1:
            csv_reader = csv.reader(f1)
            for r in csv_reader:
                line.append(r)
                if name == r[0]:
                    line.remove(r)
                    cnt+=1


            csv_write = open('static/people.csv', 'w')
            for i in line:
                for j in i:
                    csv_write.write(j + ',')
                csv_write.write('\n')

        if cnt != 0:
            return render_template('removedetails.html', message="Record Remove Successfully.")
        else:
            return render_template('removedetails.html', error="Record Not Found.")


if __name__ == '__main__':
    app.run(debug=True)




