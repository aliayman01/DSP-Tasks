def ReadSignalFile(file_name):
    expected_indices = []
    expected_samples = []
    with open(file_name, 'r') as f:
        # Skip 3 header lines ([SignalType], [IsPeriodic], [N1])
        f.readline()
        f.readline()
        f.readline()

        # Read samples line by line
        line = f.readline()
        while line:
            L = line.strip()
            parts = L.split()
            if len(parts) >= 2:
                V1 = int(parts[0])
                V2 = float(parts[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
    return expected_indices, expected_samples


def AddSignalSamplesAreEqual(userFirstSignal, userSecondSignal, Your_indices, Your_samples, output_file_path=""):
    file_name = output_file_path
    if not file_name:
        if userFirstSignal == 'Signal1.txt' and userSecondSignal == 'Signal2.txt':
            file_name = "resources/task1/outputs/Signal1+Signal2.txt"
        elif userFirstSignal == 'Signal1.txt' and userSecondSignal == 'Signal3.txt':
            file_name = "resources/task1/outputs/Signal1+Signal3.txt"

    expected_indices, expected_samples = ReadSignalFile(file_name)

    if (len(expected_samples) != len(Your_samples)) or (len(expected_indices) != len(Your_indices)):
        msg = "Addition Test case failed, your signal have different length from the expected one"
        print(msg)
        return False, msg

    for i in range(len(Your_indices)):
        if Your_indices[i] != expected_indices[i]:
            msg = "Addition Test case failed, your signal have different indicies from the expected one"
            print(msg)
            return False, msg

    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            msg = "Addition Test case failed, your signal have different values from the expected one"
            print(msg)
            return False, msg

    msg = "Addition Test case passed successfully"
    print(msg)
    return True, msg


def MultiplySignalByConst(User_Const, Your_indices, Your_samples, output_file_path=""):
    file_name = output_file_path
    if not file_name:
        if User_Const == 5:
            file_name = "resources/task1/outputs/MultiplySignalByConstant-Signal1 - by 5.txt"
        elif User_Const == 10:
            file_name = "resources/task1/outputs/MultiplySignalByConstant-Signal2 - by 10.txt"

    expected_indices, expected_samples = ReadSignalFile(file_name)

    if (len(expected_samples) != len(Your_samples)) or (len(expected_indices) != len(Your_indices)):
        msg = f"Multiply by {User_Const} Test case failed, your signal have different length from the expected one"
        print(msg)
        return False, msg

    for i in range(len(Your_indices)):
        if Your_indices[i] != expected_indices[i]:
            msg = f"Multiply by {User_Const} Test case failed, your signal have different indicies from the expected one"
            print(msg)
            return False, msg

    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            msg = f"Multiply by {User_Const} Test case failed, your signal have different values from the expected one"
            print(msg)
            return False, msg

    msg = f"Multiply by {User_Const} Test case passed successfully"
    print(msg)
    return True, msg


def SignalSamplesAreEqual(TaskName, output_file_name, Your_indices, Your_samples):
    expected_indices, expected_samples = ReadSignalFile(output_file_name)

    if (len(expected_samples) != len(Your_samples)) or (len(expected_indices) != len(Your_indices)):
        msg = f"{TaskName} Test case failed, your signal have different length from the expected one"
        print(msg)
        return False, msg

    for i in range(len(Your_indices)):
        if Your_indices[i] != expected_indices[i]:
            msg = f"{TaskName} Test case failed, your signal have different indicies from the expected one"
            print(msg)
            return False, msg

    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            msg = f"{TaskName} Test case failed, your signal have different values from the expected one"
            print(msg)
            return False, msg

    msg = f"{TaskName} Test case passed successfully"
    print(msg)
    return True, msg