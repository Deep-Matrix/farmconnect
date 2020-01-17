from .apis import farmer

def create(conn, data):
    return farmer.createFarmerUser(conn, data)