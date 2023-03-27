from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# VOTER ROUTES


@app.route('/voters/', methods=['POST'])
def register_voter():
    if not request.data:
        return jsonify({"ok": False,
                        "message": "no data provided"}), 400
    # get payload
    payload = json.loads(request.data)

    # validate payload
    fields = ["id", "firstName", "lastName", "email", "yearGroup", "major"]
    for field in fields:
        if not payload.get(field):
            message = "{} is required".format(field)
            return jsonify({"ok": False,
                            "message": message}), 400

    # add data to database
        # fetch all the voters from voters.txt
        # check if the voter already exists
        # if voter doesn't exist, add the voter to the voters.txt
        # if voter exists, return an error message

    try:
        with open("./database/voters.txt", "r") as voters_file:
            voters = json.load(voters_file)

            for voter in voters:
                if voter["id"] == payload["id"]:
                    return jsonify({"ok": False,
                                    "message": "voter already exists"}), 400

            voters.append(payload)

        with open("./database/voters.txt", "w") as voters_file:
            json.dump(voters, voters_file)
            return jsonify({"ok": True,
                            "message": "voter successfully registered",
                            "id": payload["id"]}), 201
    except FileNotFoundError:
        with open("./database/voters.txt", "w") as voters_file:
            json.dump([payload], voters_file)
            return jsonify({"ok": True,
                            "message": "voter successfully registered",
                            "id": payload["id"]}), 201


@app.route('/voters/<string:id>/', methods=['DELETE'])
def de_register_voter(id):
    try:
        with open("./database/voters.txt", "r") as voters_file:
            voters = json.load(voters_file)
            voter_was_found = False

            for voter in voters:
                if voter["id"] == id:
                    voter_was_found = True
                    voters.remove(voter)
                    break

            if voter_was_found:
                with open("./database/voters.txt", "w") as voters_file:
                    json.dump(voters, voters_file)
                return jsonify({"ok": True,
                                "message": "voter successfully de-registered",
                                "id": id}), 200

            return jsonify({"ok": False,
                            "message": "voter not found"}), 404
    except FileNotFoundError:
        return jsonify({"ok": False,
                        "message": "voter not found"}), 404


@app.route('/voters/<string:id>/', methods=['PATCH'])
def update_voter(id):
    if not request.data:
        return jsonify({"ok": False,
                        "message": "no data provided"}), 400

    payload = json.loads(request.data)

    try:
        with open("./database/voters.txt", "r") as voters_file:
            voters = json.load(voters_file)

            target_voter = None

            for voter in voters:
                if voter["id"] == id:
                    target_voter = voter
                    voters.remove(voter)
                    break

            if not target_voter:
                return jsonify({"ok": False,
                                "message": "voter not found"}), 404

            for key in payload:
                target_voter[key] = payload[key]
                print(key, payload[key])

            voters.append(target_voter)
    except FileNotFoundError:
        return jsonify({"ok": False,
                        "message": "voter not found"}), 404

    with open("./database/voters.txt", "w") as voters_file:
        json.dump(voters, voters_file)

    return jsonify({"ok": True,
                    "message": "voter details successfully updated",
                    "id": id})


@app.route('/voters/<string:id>/', methods=['GET'])
def get_voter(id):
    try:
        with open("./database/voters.txt", "r") as voters_file:
            voters = json.load(voters_file)

            for voter in voters:
                if voter["id"] == id:
                    return jsonify(voter), 200

            return jsonify({"ok": False,
                            "message": "voter not found"}), 404
    except FileNotFoundError:
        return jsonify({"ok": False,
                        "message": "voter not found"}), 404

# ELECTION ROUTES


@app.route('/elections/', methods=['POST'])
def create_election():
    if not request.data:
        return jsonify({"ok": False,
                        "message": "no election data provided"}), 400

    payload = json.loads(request.data)

    fields = ["electionId", "ballot"]
    for field in fields:
        if not payload.get(field):
            message = "{} is required".format(field)
            return jsonify({"ok": False,
                            "message": message}), 400

    try:
        with open("./database/elections.txt", "r") as elections_file:
            elections = json.load(elections_file)

            for election in elections:
                if election["electionId"] == payload["electionId"]:
                    return jsonify({"ok": False,
                                    "message": "election already exists"}), 400

            elections.append(payload)

        with open("./database/elections.txt", "w") as elections_file:
            json.dump(elections, elections_file)
            return jsonify({"ok": True,
                            "message": "election successfully created",
                            "id": payload["electionId"]}), 201
    except FileNotFoundError:
        with open("./database/elections.txt", "w") as elections_file:
            json.dump([payload], elections_file)
            return jsonify({"ok": True,
                            "message": "election successfully created",
                            "id": payload["electionId"]}), 201


@app.route('/elections/<string:id>/', methods=['GET'])
def get_one_election(id):
    try:
        with open("./database/elections.txt", "r") as elections_file:
            elections = json.load(elections_file)

            for election in elections:
                if election["electionId"] == id:
                    return jsonify(election), 200

            return jsonify({"ok": False,
                            "message": "election not found"}), 404
    except FileNotFoundError:
        return jsonify({"ok": False,
                        "message": "election not found"}), 404


@app.route('/elections/<string:id>/', methods=['DELETE'])
def delete_election(id):
    try:
        with open("./database/elections.txt", "r") as elections_file:
            elections = json.load(elections_file)
            election_was_found = False

            for election in elections:
                if election["electionId"] == id:
                    election_was_found = True
                    elections.remove(election)
                    break

            if election_was_found:
                with open("./database/elections.txt", "w") as elections_file:
                    json.dump(elections, elections_file)
                return jsonify({"ok": True,
                                "message": "election successfully deleted",
                                "id": id}), 200

            return jsonify({"ok": False,
                            "message": "election not found"}), 404
    except FileNotFoundError:
        return jsonify({"ok": False,
                        "message": "election not found"}), 404


# VOTE ROUTES
@app.route('/vote/', methods=['POST'])
def cast_vote():
    # check if request data is present
    if not request.data:
        return jsonify({"ok": False,
                        "message": "no vote data provided"}), 400

    payload = json.loads(request.data)

    # check if all required fields are present
    fields = ["voterId", "electionId", "candidateId"]
    for field in fields:
        if not payload.get(field):
            message = "{} is required".format(field)
            return jsonify({"ok": False,
                            "message": message}), 400

    # check if voter exists
    try:
        with open("./database/voters.txt", "r") as voters_file:
            voters = json.load(voters_file)

            voter_exists = False

            for voter in voters:
                if voter["id"] == payload["voterId"]:
                    voter_exists = True
                    break

            if not voter_exists:
                return jsonify({"ok": False,
                                "message": "voter not found"}), 404
    except FileNotFoundError:
        return jsonify({"ok": False,
                        "message": "voter not found"}), 404

    # validate user's vote status
    try:
        with open("./database/votes.txt", "r") as votes_file:
            votes = json.load(votes_file)

            # has voter already voted?
            for vote in votes:
                if vote["voterId"] == payload["voterId"]:
                    return jsonify({"ok": False,
                                    "message": "voter has already voted"}), 400

            votes.append(payload)

        # update voter's vote status
        with open("./database/voters.txt", "r") as voters_file:
            voters = json.load(voters_file)

            for voter in voters:
                if voter["id"] == payload["voterId"]:
                    voters.remove(voter)
                    voter["hasVoted"] = True
                    voters.append(voter)
                    break

        # write updated voter data to file
        with open("./database/voters.txt", "w") as voters_file:
            json.dump(voters, voters_file)

        # update election's vote count
        with open("./database/elections.txt", "r") as elections_file:
            elections = json.load(elections_file)

            for election in elections:
                if election["electionId"] == payload["electionId"]:
                    elections.remove(election)
                    for candidate in election["ballot"]:
                        if candidate["candidateId"] == payload["candidateId"]:
                            candidate["voteCount"] += 1
                    elections.append(election)
                    break

        # write updated election data to file
        with open("./database/elections.txt", "w") as elections_file:
            json.dump(elections, elections_file)

        # write vote data to file
        with open("./database/votes.txt", "w") as votes_file:
            json.dump(votes, votes_file)
            return jsonify({"ok": True,
                            "message": "vote successfully cast",
                            "id": payload["voterId"]}), 201
    except FileNotFoundError:
        # update voter's vote status
        with open("./database/voters.txt", "r") as voters_file:
            voters = json.load(voters_file)

            for voter in voters:
                if voter["id"] == payload["voterId"]:
                    voters.remove(voter)
                    voter["hasVoted"] = True
                    voters.append(voter)
                    break

        # write updated voter data to file
        with open("./database/voters.txt", "w") as voters_file:
            json.dump(voters, voters_file)

        # update election's vote count
        with open("./database/elections.txt", "r") as elections_file:
            elections = json.load(elections_file)

            for election in elections:
                if election["electionId"] == payload["electionId"]:
                    elections.remove(election)
                    for candidate in election["ballot"]:
                        if candidate["candidateId"] == payload["candidateId"]:
                            candidate["voteCount"] += 1
                    elections.append(election)
                    break

        # write updated election data to file
        with open("./database/elections.txt", "w") as elections_file:
            json.dump(elections, elections_file)

        with open("./database/votes.txt", "w") as votes_file:
            json.dump([payload], votes_file)
            return jsonify({"ok": True,
                            "message": "vote successfully cast",
                            "id": payload["voterId"]}), 201


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=105, debug=True)
