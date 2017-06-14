from flask import Flask
from flask import render_template
from flask import request
import pandas as pd


df = pd.read_excel('one_data.xls')
df = df.drop('Index', 1)




def brain(first, second):

        wait_tm = .6

        frm = first
        to = second

        if frm == to:
            diff = "Both stations cannot be the same"

        else:


            subset = df[frm+1:to+1]

            local_total = subset["Local_Tm_Frm_Last"].sum(axis=0)

            num_of_wait_stations = len(subset.index) - 1

            wait_time =  num_of_wait_stations * wait_tm

            local_total = local_total + wait_time

            last_row = subset.tail(1)


            if last_row.iloc[0]['Express'] == 1:
                last_exp = 1

            else:
                last_exp = 0

            num_of_exp_waits = subset["Express"].sum(axis=0) - last_exp

            ex_wait_time = num_of_exp_waits * wait_tm

            express_total = subset["Express_Tm_Frm_Last"].sum(axis=0) + ex_wait_time

            diff = local_total - express_total

            return {'diff':diff, 'express_total':express_total ,'local_total':local_total }



app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def calculation():
    result = 0
    express = 0
    local = 0
    error = ''
    # you may want to customize your GET... in this case not applicable
    if request.method=='POST':
        # get the form data
        first = int(request.form['first'])
        second = int(request.form['second'])

        res = brain(first,second)

        result = res['diff']
        express = res['express_total']
        local = res['local_total']

    # you render the template and pass the context result & error
    return render_template('result.html', result = result, express = express, local = local);



if __name__ == "__main__":
    app.run()
