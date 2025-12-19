from data import balances


def add_balance(from_user, to_user, amount):
    if from_user == to_user:
        return

    key = (from_user, to_user)
    reverse_key = (to_user, from_user)

    if reverse_key in balances:
        if balances[reverse_key] > amount:
            balances[reverse_key] -= amount
        else:
            balances[key] = amount - balances[reverse_key]
            del balances[reverse_key]
    else:
        balances[key] = balances.get(key, 0) + amount


def equal_split(amount, paid_by, users):
    split_amount = amount / len(users)
    for user in users:
        if user != paid_by:
            add_balance(user, paid_by, split_amount)


def exact_split(paid_by, splits):
    for user, amount in splits.items():
        if user != paid_by:
            add_balance(user, paid_by, amount)


def percentage_split(amount, paid_by, percentages):
    for user, percent in percentages.items():
        share = (amount * percent) / 100
        if user != paid_by:
            add_balance(user, paid_by, share)
