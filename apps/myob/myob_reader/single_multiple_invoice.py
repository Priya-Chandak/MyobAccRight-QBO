import json

path1 = input("path1 :")

with open("{}/item_invoice.json".format(path1), "r") as f:
    data1 = json.load(f)

Q1 = data1

multiple = []
single = []

for i in range(0, len(Q1)):
    if len(Q1[i]["Item"]) == 1:
        single.append(Q1[i])

    elif len(Q1[i]["Item"]) > 1:
        multiple.append(Q1[i])

with open("{}/multiple_item_invoice.json".format(path1), "w") as jsonFile:
    jsonString = json.dumps(multiple)
    jsonFile.write(jsonString)
    jsonFile.close()

with open("{}/single_item_invoice.json".format(path1), "w") as jsonFile:
    jsonString = json.dumps(single)
    jsonFile.write(jsonString)
    jsonFile.close()
