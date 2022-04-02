from flask import Flask, render_template, url_for, request
import psycopg2
import os
import pandas as pd
from datetime import datetime, timedelta
import json

'''

'''

psql_pass = os.environ.get('PSQL_PASS')

app = Flask(__name__)


# no home route, reminder only
@app.route('/')
def home():
    return render_template('index.html')


@ app.route('/charts/', methods=['GET', 'POST'])
def charts():

    # set defaults for first visit (GET)
    num_rec = 5
    deltacalc = 'first'
    recent = 'rec'

    if request.method == 'POST':
        num_rec = int(request.form['count'])
        deltacalc = request.form['deltacalc']
        recent = request.form['recent']

    days_recent = 180
    min_resp = 4  # must be 2 or more

    now = datetime.now()

    # get data from DB

    connect = psycopg2.connect(
        database='mostimproved',
        user='postgres',
        password=psql_pass
    )
    cursor = connect.cursor()
    cursor.execute("SELECT id, date, loc, first, last, email, ltr, comment FROM responses ORDER BY id")
    data = cursor.fetchall()
    cursor.close()
    connect.close()

    # use pandas df to groupby

    df = pd.DataFrame(data, columns=['id', 'date', 'loc', 'first', 'last', 'email', 'ltr', 'comment'])

    # get earliest date from df for charts--used below (pass to template)
    min_date = min(df['date'])
    min_date_python = min_date.to_pydatetime()
    min_date_string = datetime.strftime(min_date_python, '%Y-%m-%d')

    # convert date to string, with correct format for charts.js
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')

    # group by (unique) email and add grouped values (date, ltr, etc) as lists ( e.g. none@none.com | [10,8,9] )
    df2 = df.groupby("email").agg(list)

    # output to dict with (unique) emails as the keys
    data_dict = df2.to_dict('index')  # to_dict method creating timestamp(), for some reason
    pd.set_option('display.max_columns', None)

    # create new data list from dict

    data = []
    for k, v in data_dict.items():
        # min number of responses
        if len(v['ltr']) >= min_resp:

            temp = {}

            temp['email'] = k
            temp['first'] = v['first'][-1].title().replace('vip', '')  # get last name, etc in the list (possible multiple associated with an email)
            temp['last'] = v['last'][-1].title().replace('vip', '')
            temp['club'] = v['loc'][-1]  # note different key name

            temp['comment'] = v['comment']
            temp['date'] = v['date']
            temp['score'] = v['ltr']

            temp['chartScores'] = []

            for i in range(len(v['ltr'])):  # loop through lists--assuming that len of dates and ltr are the same...
                temp['chartScores'].append({'x': v['date'][i], 'y': v['ltr'][i]})  # convert pandas timestamp to date str

            data.append(temp)

    # add a 'delta' for each record in data
    # too many loops on data... need to optimize...
    for record in data:
        tmp_scores = []

        for i in record['chartScores']:
            score = i['y']
            tmp_scores.append(score)

        if deltacalc == 'avg':
            delta = tmp_scores[0] - (sum(tmp_scores[1:]) / len(tmp_scores[1:]))
            record['delta'] = delta
        else:
            delta = tmp_scores[0] - tmp_scores[-1]
            record['delta'] = delta
            # print(data)

    # sort data (list of dicts), in place by key 'delta'

    data = sorted(data, reverse=True, key=lambda i: i['delta'])

    # get start and end of list, based on recent or not recent visit

    data_start = []
    data_end = []

    # filter for only recent responders
    if recent == 'rec':

        then = now - timedelta(days=days_recent)

        for record in data:
            if len(data_start) < num_rec:
                date = record['chartScores'][0]['x']  # most recent score date
                if datetime.strptime(date, '%Y-%m-%d') > then:
                    data_start.append(record)
            else:
                break

        for record in data[::-1]:  # start at end and go backward
            if len(data_end) < num_rec:
                date = record['chartScores'][0]['x']  # most recent score date
                if datetime.strptime(date, '%Y-%m-%d') > then:
                    data_end.insert(0, record)  # need to add record at beginning of list, or it's reversed
            else:
                break

    # ...or ignore dates and just select top/bottom
    else:
        data_start = data[:num_rec]
        data_end = data[-(num_rec):]

    return render_template('charts.html', data_start=data_start, data_end=data_end, min_date_string=min_date_string)


if __name__ == "__main__":
    app.run(debug=True)
