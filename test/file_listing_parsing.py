import pickle

input = open("output.pickle", "rb")
data = pickle.load(input)
data = data.decode("utf-8")

data_split = data.split("\n")

file_dir = []
dir = []
for ele in data_split:
    dir.append(ele.split(" ")[-1].replace("\r", ""))
    file_dir.append(ele.split(" ")[0][:1])
    print(dir[-1])
dir.pop()
file_dir.pop()

result = []
for i in range(0,len(dir)-1):
    result.append((
        file_dir[i],
        dir[i]
    ))

print(result)

