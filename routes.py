from flask import Blueprint, request, jsonify
from services import equal_split, exact_split, percentage_split
from data import users, groups, balances, equal_expenses, exact_expenses, percentage_expenses,settlements


api = Blueprint("api", __name__)


@api.route("/users", methods=["POST"])
def create_user():
    data = request.json
    users[data["id"]] = data["name"]
    return jsonify({"message": "User created"})


@api.route("/groups", methods=["POST"])
def create_group():
    data = request.json
    groups[data["id"]] = {
        "name": data["name"],
        "members": data["members"]
    }
    return jsonify({"message": "Group created"})


@api.route("/expense/equal", methods=["POST"])
def add_equal_expense():
    data = request.json

    equal_split(data["amount"], data["paid_by"], data["users"])

    equal_expenses.append({
        "amount": data["amount"],
        "paid_by": data["paid_by"],
        "users": data["users"]
    })

    return jsonify({"message": "Equal expense added"})



@api.route("/expense/exact", methods=["POST"])
def add_exact_expense():
    data = request.json

    exact_split(data["paid_by"], data["splits"])

    exact_expenses.append({
        "paid_by": data["paid_by"],
        "splits": data["splits"]
    })

    return jsonify({"message": "Exact expense added"})

@api.route("/expense/percentage", methods=["POST"])
def add_percentage_expense():
    data = request.json

    percentage_split(data["amount"], data["paid_by"], data["percentages"])

    percentage_expenses.append({
        "amount": data["amount"],
        "paid_by": data["paid_by"],
        "percentages": data["percentages"]
    })

    return jsonify({"message": "Percentage expense added"})
@api.route("/settle", methods=["POST"])
def settle_due():
    data = request.json
    from_user = data["from"]
    to_user = data["to"]
    amount = data["amount"]

    key = (from_user, to_user)

    if key not in balances:
        return jsonify({"message": "No dues to settle"}), 400

    if amount >= balances[key]:
        del balances[key]
        settled_amount = balances.get(key, amount)
    else:
        balances[key] -= amount
        settled_amount = amount

    settlements.append({
        "from": from_user,
        "to": to_user,
        "amount": settled_amount
    })

    return jsonify({"message": "Settlement successful"})


@api.route("/expense/equal", methods=["GET"])
def get_equal_expenses():
    return jsonify(equal_expenses)

@api.route("/expense/exact", methods=["GET"])
def get_exact_expenses():
    return jsonify(exact_expenses)

@api.route("/expense/percentage", methods=["GET"])
def get_percentage_expenses():
    return jsonify(percentage_expenses)

@api.route("/settlements", methods=["GET"])
def get_settlements():
    return jsonify(settlements)

@api.route("/who-owes-whom", methods=["GET"])
def who_owes_whom():
    result = []

    for (from_user, to_user), amount in balances.items():
        result.append({
            "debtor": from_user,
            "creditor": to_user,
            "amount": amount,
            "statement": f"{from_user} owes {to_user} amount {amount}"
        })

    return jsonify(result)



@api.route("/balances", methods=["GET"])
def get_balances():
    result = []
    for (u1, u2), amt in balances.items():
        result.append({
            "from": u1,
            "to": u2,
            "amount": amt
        })
    return jsonify(result)
