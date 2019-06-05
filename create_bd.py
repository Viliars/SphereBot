import shelve

file = shelve.open("USERS")

file['users'] = {}

file.close()