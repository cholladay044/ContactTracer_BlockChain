from Processing import LocationProcessor, RiskFinder
from Blockchain import Blockchain
from TripLoader import TripLoader
import SaveManager


def main():
    # create instances of classes we need
    print("Initializing...")

    # Loads trip data from trips.json
    print("Loading Mock Data")
    loader = TripLoader("datasets/trips.2.100.2d.1563227630000.csv")

    # Creates LocationProcessor instance with loaded data
    print("Initializing Location Processor")
    processor = LocationProcessor(loader.data())

    # Creates empty blockchain
    print("Creating Empty Blockchain")
    blockchain = Blockchain()

    # create the genesis block
    print("Generating Genesis Block")
    blockchain.create_genesis_block(timestamp=1563123230)

    # blockchain state before data processing
    print("Printing Blockchain")
    print(blockchain)

    # Process the pool for direct contacts
    print("Processing Location Updates...")
    processor.find_direct_contacts()

    # Get direct contacts as a List of Transactions
    print("Building Transactions")
    transactions = processor.build_transactions()

    # Package the transactions into a block and append it to the blockchain
    print("Building Block")
    blockchain.build_block(transactions, timestamp=1563227630)
    print("Block Inserted to Blockchain")

    # Blockchain after data processing
    print(blockchain)

    # Serialization Test
    # bc = blockchain.get_chain()
    pth = "/SaveData/blockchain.json"
    # for x in bc:
    #    SaveManager.
    #    SaveManager.saveBlockchainJSON(json.loads(x.toJSON()), pth)

    print("Saving Blockchain...")
    SaveManager.init_file(pth)
    for x in blockchain.get_chain():
        SaveManager.save_file(pth, x)




main()
