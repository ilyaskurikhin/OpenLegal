import json
from flask import Flask, render_template

app = Flask(__name__, static_folder='static', static_url_path='')


@app.route("/")
def start_page():
    decisions = [decision_name for decision_name,
                 _ in load_decisions().items()]

    return render_template('start.html', decisions=decisions)


@app.route("/article/<string:id>")
def decision_page(id: str):
    print(id)
    decisions = load_decisions()
    decision = decisions[id]

    # load matching paragraphs:
    paragraphs = decision['paragraphs']
    with open('../comparison_values.json', 'r', encoding='utf-8') as file:
        comparison_data = json.load(file)
    for paragraph in paragraphs:
        hash = __correct_hash(paragraph['hash'])

        if hash in comparison_data:
            matches: dict = comparison_data[hash]
            paragraph['matches'] = []
            paragraph['matches'] = matches
            for match, match_rate in matches.items():
                for decision_name, dec in decisions.items():
                    for par in dec['paragraphs']:
                        if __correct_hash(par['hash']) == match:
                            matches[match] = {
                                'decision': decision_name,
                                'id': decision_name.replace(' ', '-'),
                                'original': par['original'], 
                                'confidence': match_rate}
                pass
            print('gugus!!!!!!!!!')

    return render_template('decision.html', decision=id, decision_object=decision)


def load_decisions() -> dict:
    with open('static/json_data.json', 'r', encoding='utf-8') as file:
        decision = json.load(file)
    return decision


def __correct_hash(hash: str) -> str:
    """Just in case the binary arrays haven't been saved
    correctly as a string"""

    if hash[:2] == "b'" and hash[-1] == "'":
        hash = hash[2:-1]
    return hash


app.run(debug=True)
