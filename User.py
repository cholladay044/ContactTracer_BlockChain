class User:
    def __init__(self, first_name, last_name, email, address, phone):
        # Add a method to generate an id
        self.id = 0
        self.firstName = first_name
        self.lastName = last_name
        self.email = email
        # Commenting out the password

        # make sure this is the PhysAddress class, not sure if we can strictly type params
        self.address = address
        self.phone = phone
        # Decide On a Library to implement this with
        self.registrationDate = 0
