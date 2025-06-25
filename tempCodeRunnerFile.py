@app.route('/api/teamVteam', methods=['POST'])
def teamVteam():
    reponse=requests.get('http://127.0.0.1:5000/api/teams')
    teams_list=reponse.json()['teams']
    return render_template('teamVteam.html', teams=teams_list)
    