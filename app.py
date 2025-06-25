from flask import Flask,render_template,render_template_string,request
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/api/teams', methods=['POST'])
def teams():
    reponse=requests.get('http://127.0.0.1:5000/api/teams')
    teams_list=reponse.json()['teams']
    return render_template('teams.html', teams=teams_list)



@app.route('/api/teamVteam', methods=['POST'])
def teamVteam():
    reponse=requests.get('http://127.0.0.1:5000/api/teams')
    teams_list=reponse.json()['teams']
    return render_template('teamVteam.html', teams=teams_list)
    
    
    
@app.route('/api/teamVteam_response')
def teamVteam_response():
    team1=request.args.get('team1')
    team2=request.args.get('team2')
    response=requests.get('http://127.0.0.1:5000/api/teamVteam?team1={}&team2={}'.format(team1,team2))
    data=response.json()
    return render_template('teamVteam_response.html',data=data)



@app.route('/api/team_winning_record', methods=['POST'])
def team_winning():
    reponse=requests.get('http://127.0.0.1:5000/api/team_winning_record')
    data=reponse.json()
    return render_template('team_winning.html', data=data)




@app.route('/api/point_table',methods=['POST'])
def point_table():
    return render_template('point_table.html')



@app.route('/api/points_table_view', methods=['POST'])
def points_table_view():
    season = request.form.get('season_ka_data')
    
    if not season:
        return "Season parameter is missing.", 400

    # Fetch data from internal API
    try:
        response = requests.get(f'http://127.0.0.1:5000/api/point_table?season={season}')
        response.raise_for_status()
        points_data = response.json()
    except requests.RequestException as e:
        return f"Failed to fetch points table: {e}", 500

    def season_sort_key(team_data):
        order_map = {
            "Winner": 1,
            "Runner Up": 2,
            "3rd Place": 3,
            "4th Place": 4
        }
        pos = team_data.get('SeasonPosition')

        if isinstance(pos, str):
            pos = pos.strip()
            if pos in order_map:
                return order_map[pos]
            try:
                return int(pos)  # "5", "6", etc.
            except ValueError:
                return float('inf')  # Push invalid values to the bottom
        elif isinstance(pos, int):
            return pos
        else:
            return float('inf')

    # Check if SeasonPosition exists in at least one team
    has_season_position = any(team.get('SeasonPosition') for team in points_data)

    if has_season_position:
        try:
            sorted_points = sorted(points_data, key=season_sort_key)
            return render_template(
                'points_result_combined.html',
                season=season,
                points=sorted_points,
                has_position=True
            )
        except Exception as e:
            print(f"Sorting error: {e}")  # Debug log
            return render_template(
                'points_result_combined.html',
                season=season,
                points=points_data,
                has_position=False
            )
    else:
        return render_template(
            'points_result_combined.html',
            season=season,
            points=points_data,
            has_position=False
        )




@app.route('/api/purple_cap', methods=['POST'])
def purple_cap():
    response = requests.get('http://127.0.0.1:5000/api/purple_cap')
    purple_cap_list = response.json()  # This is a dictionary: {season: {details}}

    return render_template('purple_cap.html', purple_data=purple_cap_list)



@app.route('/api/orange_cap', methods=['POST'])
def orange_cap():
    response = requests.get('http://127.0.0.1:5000/api/orange_cap')
    orange_cap_list = response.json()  # This is a dictionary: {season: {details}}

    return render_template('orange_cap.html', orange_data=orange_cap_list)


@app.route('/api/batting_pair',methods=['POST'])
def batting_pair():
    reponse=requests.get('http://127.0.0.1:5000/api/batting_pair')
    batt_pair=reponse.json()
    return render_template('batting_pair.html',  pairs=batt_pair)



@app.route('/api/Player_Of_Match', methods=['POST'])
def pom():
    response = requests.get('http://127.0.0.1:5000/api/Player_Of_Match')
    pom_player = response.json()
    return render_template('pom.html', data=pom_player)


@app.route('/api/bowler_details',methods=['POST'])
def bowler():
    response = requests.get('http://127.0.0.1:5000/api/name_of_bowlers')
    bowlers= response.json()
    return render_template('bowler.html',data=bowlers)


@app.route('/api/specific_bowler', methods=['POST'])
def specific_bowler():
    bowler = request.form.get('bowler_name')  
    response = requests.get(f'http://127.0.0.1:5000/api/bowler_details?bowler={bowler}')
    data = response.json()
    return render_template('bowler_detail.html', data=data)


@app.route('/api/batsman_details', methods=['POST'])
def batsman_details():
    response = requests.get('http://127.0.0.1:5000/api/name_of_batsmens')
    batsmen = response.json()  # Should return {"batsmen": [...]}
    return render_template('batsman.html', data=batsmen)


@app.route('/api/specific_batsman', methods=['POST'])
def specific_batsman():
    batsman = request.form.get('batsman_name')
    response = requests.get(f'http://127.0.0.1:5000/api/batsman_details?batsman={batsman}')
    data = response.json()  # Dict with seasons
    return render_template('batsman_detail.html', data=data)


if __name__ == '__main__':
    app.run(debug=True,port=8888)
