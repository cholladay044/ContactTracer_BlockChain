from PositiveCase import PositiveCase
from Blockchain import Transaction
import pandas as pd
from random import randrange
from math import radians, cos, sin, asin, sqrt
import time
from treelib import Tree


class RiskFinder:

    def __init__(self, start_date, end_date, blockchain, test_results):
        self.end_date = end_date
        self.start_date = start_date
        self.blockchain = blockchain
        self.test_results = test_results
        self.trees = []

    def get_user_contacts(self, user):
        transactions = self.blockchain.get_user_transactions(user, self.start_date, self.end_date)
        direct_contacts = []
        for t in transactions:
            if t.user_a_id == user:
                direct_contacts.append(t.user_b_id)
            else:
                direct_contacts.append(t.user_a_id)

        return direct_contacts

    def make_contact_trees(self):
        trees = []
        for positive_case in self.test_results:
            if positive_case.status == 1 and self.start_date <= positive_case.timestamp <= self.end_date:
                trees.append(self.get_contact_tree(positive_case.user))

        self.trees = trees

    def get_contact_trees(self):
        return self.trees

    def get_risk_level_users(self, level=1):
        users = set()
        for tree in self.get_contact_trees():
            for user in tree.get_risk_level(level):
                users.add(user)
        return list(users)

    def get_risk_levels(self):
        risk1 = set(self.get_risk_level_users(1))
        risk2 = set([x for x in self.get_risk_level_users(2) if x not in risk1])
        risk3 = set([x for x in self.get_risk_level_users(3) if x not in risk1 and x not in risk2])
        risk4 = set([x for x in self.get_risk_level_users(4) if x not in risk1 and x not in risk2 and x not in risk3])

        return list(risk1), list(risk2), list(risk3), list(risk4)

    def print_risk_levels(self):
        r1, r2, r3, r4 = self.get_risk_levels()
        total = len(r1) + len(r2) + len(r3) + len(r4)
        print("\nTotals for all risk levels")
        print("Risk Level 1: (#:" + str(len(r1)) + " - " + str(round(len(r1) * 100 / total, 2)) + "%)")
        print(r1)
        print()
        print("Risk Level 2: (#:" + str(len(r2)) + " - " + str(round(len(r2) * 100 / total, 2)) + "%)")
        print(r2)
        print()
        print("Risk Level 3: (#:" + str(len(r3)) + " - " + str(round(len(r3) * 100 / total, 2)) + "%)")
        print(r3)
        print()
        print("Risk Level 4: (#:" + str(len(r4)) + " - " + str(round(len(r4) * 100 / total, 2)) + "%)")
        print(r4)
        print()

    def get_average_risk_level(self):
        r1, r2, r3, r4 = self.get_risk_levels()
        total = 0
        for t in r1:
            total += 1

        for t in r2:
            total += 2

        for t in r3:
            total += 3

        for t in r4:
            total += 4

        return total / (len(r1) + len(r2) + len(r3) + len(r4))

    def get_user_result(self, user):
        result = None
        for r in self.test_results:
            if r.user == user:
                result = r
        return result

    def get_ignorable_users(self, user):
        ignore = []
        result = self.get_user_result(user)
        contacts = self.get_user_contacts(user)

        if result is None:
            return ignore

        for contact in contacts:
            test = self.get_user_result(contact)
            if test is not None:
                if test.status == 0 and test.timestamp >= result.timestamp:
                    ignore.append(contact)

        return ignore

    def get_contact_tree(self, user):
        tree = ContactTree(user)
        seen = {user}

        contacts = self.get_user_contacts(user)
        ignore = self.get_ignorable_users(user)

        contacts = list(set(contacts) - set(ignore))
        tree.set_children(user, contacts)
        [seen.add(x) for x in contacts]
        [seen.add(x) for x in ignore]

        for contact in contacts:
            ignore = self.get_ignorable_users(contact)
            contacts2 = list(set([x for x in self.get_user_contacts(contact) if x not in seen]) - set(ignore))
            tree.set_children(contact, contacts2)
            [seen.add(x) for x in contacts2]

            for contact2 in contacts2:
                ignore = self.get_ignorable_users(contact2)
                contacts3 = list(set([x for x in self.get_user_contacts(contact2) if x not in seen]) - set(ignore))
                tree.set_children(contact2, contacts3)
                [seen.add(x) for x in contacts3]

                for contact3 in contacts3:
                    ignore = self.get_ignorable_users(contact3)
                    contacts4 = list(set([x for x in self.get_user_contacts(contact3) if x not in seen]) - set(ignore))
                    tree.set_children(contact3, contacts4)
                    [seen.add(x) for x in contacts4]

                    for contact4 in contacts4:
                        tree.set_children(contact4, [])

        return tree


class Case:

    def __init__(self, user, status, timestamp):
        self.user = user
        self.status = status
        self.timestamp = timestamp

    def __str__(self):
        return str(self.user) + " " + str(self.status) + " " + str(self.timestamp)

    __repr__ = __str__


class ContactTree:

    def __init__(self, user, node_map=None):
        if node_map is None:
            node_map = {}

        self.user = user
        self.node_map = node_map
        self.tree = Tree()
        self.tree.create_node(user, user)

    def set_children(self, user, children):
        self.node_map[user] = children

    def get_tree(self):
        agenda, seen = [self.user], {self.user}

        while agenda:
            nxt = agenda.pop()
            for child in self.node_map[nxt]:
                self.tree.create_node(child, child, parent=nxt)
                if child not in seen:
                    agenda.append(child)
                    seen.add(child)
        return self.tree

    def get_risk_level(self, level=1):
        nodes = list(self.tree.filter_nodes(lambda x: self.tree.depth(x) == level))
        return [x.identifier for x in nodes]

    def get_risk_one(self):
        return self.get_risk_level(1)

    def get_risk_two(self):
        return self.get_risk_level(2)

    def get_risk_three(self):
        return self.get_risk_level(3)

    def get_risk_four(self):
        return self.get_risk_level(4)

    def __str__(self):
        return "ROOT: " + str(self.user) \
               + "\nLevel 1: " + str(self.get_risk_one()) \
               + "\nLevel 2: " + str(self.get_risk_two()) \
               + "\nLevel 3: " + str(self.get_risk_three()) \
               + "\nLevel 4: " + str(self.get_risk_four())

    def __contains__(self, item):
        for user, children in self.tree.items():
            if user == item or item in children or item == self.user:
                return True
        return False

    __repr__ = __str__


class LocationProcessor:

    def __init__(self, data=None):
        self.location_update_columns = ["user_id", "latitude", "longitude", "timestamp"]
        self.contact_columns = ["user_a_id", "user_b_id", "user_a_location", "user_b_location", "time_of_contact"]
        if data is None:
            self.location_updates = pd.DataFrame(columns=self.location_update_columns)
        else:
            self.location_updates = data
            self.location_updates.columns = self.location_update_columns
        self.direct_contact_instances = pd.DataFrame(columns=self.contact_columns)

    def add_location_update(self, user_id, latitude, longitude, timestamp):
        temp = pd.DataFrame([[user_id, latitude, longitude, timestamp]],
                            columns=["user_id", "latitude", "longitude", "timestamp"])
        self.location_updates = pd.concat([self.location_updates, temp])

    def add_direct_contact(self, user_a_id, user_b_id, user_a_location, user_b_location, timestamp):
        if not self.get_duplicate(user_a_id, user_b_id, user_a_location, user_b_location, timestamp):
            temp = pd.DataFrame([[int(user_a_id), int(user_b_id), user_a_location, user_b_location, int(timestamp)]],
                                columns=self.contact_columns)
            self.direct_contact_instances = pd.concat([self.direct_contact_instances, temp])

    def build_transactions(self):
        transactions = []
        for index, contact in self.direct_contact_instances.iterrows():
            transaction = Transaction(contact['user_a_id'],
                                      contact['user_b_id'],
                                      contact['user_a_location'],
                                      contact['user_b_location'],
                                      contact['time_of_contact'])
            good = True

            for t in transactions:
                if t.user_a_id == transaction.user_b_id and t.user_b_id == transaction.user_a_id and t.user_a_location == transaction.user_b_location and t.user_b_location == transaction.user_a_location and t.time_of_contact == transaction.time_of_contact:
                    good = False
            if good:
                transactions.append(transaction)
        return transactions

    def get_duplicate(self, user_a_id, user_b_id, user_a_location, user_b_location, timestamp):
        return (((self.direct_contact_instances['user_a_id'] == user_a_id)
                 & (self.direct_contact_instances['user_b_id'] == user_b_id))
                | ((self.direct_contact_instances['user_b_id'] == user_a_id)
                   & (self.direct_contact_instances['user_a_id'] == user_b_id))
                & ((self.direct_contact_instances['user_a_location'] == user_a_location)
                   & (self.direct_contact_instances['user_b_location'] == user_b_location))
                | ((self.direct_contact_instances['user_b_location'] == user_a_location)
                   & (self.direct_contact_instances['user_a_location'] == user_b_location))
                & (((self.direct_contact_instances['time_of_contact'] <= timestamp + 4)
                    & (self.direct_contact_instances['time_of_contact'] >= timestamp + 4))
                   | (self.direct_contact_instances['time_of_contact'] == timestamp + 4))
                ).any()

    def find_direct_contacts(self):
        tic = time.perf_counter()

        self.location_updates.sort_values(by=['latitude', 'longitude'], inplace=True)
        self.location_updates.reset_index(inplace=True)

        count = 0
        last = -1

        for index, row in self.location_updates.iterrows():
            inner = 0
            count += 1

            if count % 1000 == 0: print(count)
            mask = (row['timestamp'] - 5.0 <= self.location_updates['timestamp']) & (
                    self.location_updates['timestamp'] <= row['timestamp'] + 5.0)
            small = self.location_updates[mask]
            for check, row_check in small.iterrows():
                inner += 1
                if row['user_id'] != row_check['user_id']:
                    distance, time_delta = dist(row['latitude'], row['longitude'], row_check['latitude'],
                                                row_check['longitude'], row['timestamp'], row_check['timestamp'])
                    if distance <= 10 and time_delta <= 5:
                        self.add_direct_contact(row['user_id'],
                                                row_check['user_id'],
                                                (row['latitude'], row['longitude']),
                                                (row_check['latitude'], row_check['longitude']),
                                                int((row['timestamp'] + row_check['timestamp']) / 2))
        last += 1
        self.direct_contact_instances.sort_values(by=['time_of_contact'], inplace=True)
        self.direct_contact_instances.reset_index(drop=True, inplace=True)

        toc = time.perf_counter()
        print(f"Location updates processed in {toc - tic:0.4f} seconds")


def dist(lat1, long1, lat2, long2, timestamp1, timestamp2):
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    km = 6371 * c
    return km * 1000, abs(timestamp1 - timestamp2)
