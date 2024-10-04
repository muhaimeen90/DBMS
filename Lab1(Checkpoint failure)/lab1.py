content=[]
with open('input.txt', 'r') as file:
    for line in file:
        content.append(line.strip())

data_dict = {}
value_dict = {}
for entry in content:
    if entry.startswith('<T'):
        tx_id = entry.split()[0][1:]
        data_dict[tx_id] = ["undo"]
    elif entry.startswith('<COMMIT'):
        tx_id = entry.split()[1][:-1]
        data_dict[tx_id] = ["redo"]
    elif entry.startswith('<CKPT'):
        keys_to_delete = [key for key, value in data_dict.items() if value == ["redo"]]
        for key in keys_to_delete:
            for entry in content:
                if entry.startswith(f'<{key}'):
                    value_dict[entry.split()[1]] = entry.split()[3][:-1]
                    del data_dict[key]
                    break
            
            

print("Undo Keys:")
for key, value in data_dict.items():
    if value == ["undo"]:
        print(f"Transaction {key}")

            
print("\nRedo Keys:")
for key, value in data_dict.items():
    if value == ["redo"]:
        print(f"Transaction {key}")


for key in data_dict:
    if data_dict[key] == ["undo"]:
        for entry in content:
            if entry.startswith(f'<{key}'):
                value_dict[entry.split()[1]] = entry.split()[2]
                break
                
    elif data_dict[key] == ["redo"]:
        for entry in content:
            if entry.startswith(f'<{key}'):
                value_dict[entry.split()[1]] = entry.split()[3][:-1]
                break


print("\nFinal Values:")
for key, value in value_dict.items():
    print(f"{key}: {value}")