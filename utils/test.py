import uuid

id = uuid.uuid1()

# Representations of uuid1()
# cette manière inclut l’utilisation de l’adresse MAC de l’ordinateur et peut donc compromettre la confidentialité,
#  même si elle fournit des éléments uniques.

print("int Representation : ", end="")
print(id.int)

print("hex Representation : ", end="")
print(id.hex)


id2 = uuid.uuid4()

# Id generated using uuid4()
print("The id generated using uuid4() : ", end="")
print(str(id2))

print("int Representation : ", end="")
print(id2.int)

print("hex Representation : ", end="")
print(id2.hex)
