from flask import Flask,redirect,url_for,render_template,request
import IMP_orphan_finder
from IMP_orphan_finder import final_call

app = Flask(__name__)

@app.route('/done')
def success():
    return "<html><body><h1>DONE</h1></body></html>"

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/submit',methods=['POST','GET'])
def submit():
    if request.method=='POST':
        save_data_path=str(request.form['save_data_path'])
        path_main_folder=str(request.form['path_main_folder'])
        start_file_path=str(request.form['start_file_path'])
        start_file=str(request.form['start_file'])
        
        
        IMP_orphan_finder.final_call(save_data_path, path_main_folder, start_file_path, start_file)
        
        
        
        
    return redirect("/done")        
        
    


if __name__=="__main__":
    app.run()