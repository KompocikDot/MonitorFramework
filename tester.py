processes = ["1", '2', '3']
csv = ["2", "4", "5"]

print(list(set(csv) - set(processes)))