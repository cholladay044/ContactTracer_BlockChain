from Processing import RiskFinder, Case
from Blockchain import Block, Blockchain
import random
import SaveManager

start_date = 1563123230
end_date = 1563296030
pth = "/SaveData/blockchain-old.json"

bc = SaveManager.load_blockchain(pth)
tempChain = []

# generate blocks here and then add to blockchain after stepping out
for x in bc:
    tempBlock = Block(x["index"], SaveManager.parse_transactions(x['transactions']), x["timestamp"], x["previous_hash"],
                      x["nonce"], x['hash'])
    tempChain.append(tempBlock)

blockchain = Blockchain(tempChain)

print(blockchain)

# generate random positive cases with infection ratio

infection_rate = 0.2
negative_rate = 0.4
users = list(set(
    [transaction.user_a_id
     for block in blockchain.chain
     for transaction in block.transactions] + [transaction.user_b_id
                                               for block in
                                               blockchain.chain for
                                               transaction in
                                               block.transactions]))
num_infected = int(infection_rate * len(users))
num_negative = int(negative_rate * len(users))

infected = random.sample(users, num_infected)
users = list(set(users) - set(infected))
clean_users = random.sample(users, num_negative)

test_results = []

for user in clean_users:
    tested_time = random.randint(start_date, end_date)
    case = Case(user, 0, tested_time)
    test_results.append(case)

for i in infected:
    start = random.randint(start_date, end_date)
    case = Case(i, 1, start)
    test_results.append(case)

print("Initializing RiskFinder from", start_date, "to", end_date)
risk_finder = RiskFinder(start_date, end_date, blockchain, test_results)
risk_finder.make_contact_trees()
trees = risk_finder.get_contact_trees()

for tree in trees:
    print("Generating Contact Tree for user", tree.user)
    print(tree.get_tree())
    print(tree)
    print()

risk_finder.print_risk_levels()