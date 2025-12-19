class User:
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name


class Group:
    def __init__(self, group_id, name, members):
        self.group_id = group_id
        self.name = name
        self.members = members


class Expense:
    def __init__(self, amount, paid_by, splits):
        self.amount = amount
        self.paid_by = paid_by
        self.splits = splits
