data = "227 Entering Passive Mode (91,189,88,142,100,244)."

data_split = data.split(" ")
data_split = data_split[len(data_split)-1].split(",")
data_split[0] = data_split[0].replace("(","")
data_split[len(data_split)-1] = data_split[len(data_split)-1].replace(")","")
data_split[len(data_split)-1] = data_split[len(data_split)-1].replace(".","")

values = []
for ele in data_split:
    values.append(int(ele))

print(values)