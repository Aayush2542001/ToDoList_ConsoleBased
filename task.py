from sys import argv
import sys
from os.path import exists
import os

CWD = os.getcwd()
taskFile = CWD + "\\task.txt"
compFile = CWD + "\\completed.txt"

def sortTask():
    with open(taskFile, 'r') as f:
        List = f.readlines()

    frame = []
    for i in range(len(List)):
        p = int(''.join(List[i].split()[:1]))
        desc = " ".join(List[i].split()[1:])
        frame.append([desc,p])

    frame = sorted(frame, key=lambda x: x[1])

    return frame

def addTask():
    if len(argv) < 4:
        sys.stdout.buffer.write("Error: Missing tasks string. Nothing added!".encode('utf8'))
    else:
        priority = argv[2]
        task_name = argv[3]

        with open(taskFile, 'a') as f:
            f.write(str(priority) + " " + task_name + "\n")
        statement = "Added task: \"" + task_name + "\" with priority " + str(priority)
        sys.stdout.buffer.write(statement.encode('utf8'))

def showReport():
    frame = sortTask()
    statement = "Pending : " + str(len(frame)) + "\n"
    for i in range(len(frame)):
        statement += str(i + 1) + ". " + frame[i][0] + " [" + str(frame[i][1]) + "]" + "\n"

    statement += "\n"

    with open(compFile, 'r') as f:
        List = f.readlines()

    statement += "Completed : " + str(len(List)) + "\n"

    for i in range(len(List)):
        statement += str(i + 1) + ". " + str(List[i])

    sys.stdout.buffer.write(statement.encode('utf8'))

def showLs():
    frame = sortTask()
    statement = ''
    if len(frame) == 0:
        statement = "There are no pending tasks!"
        sys.stdout.buffer.write(statement.encode('utf8'))
    else:
        for i in range(len(frame)):
            statement += str(i + 1) + ". " + frame[i][0] + " [" + str(frame[i][1]) + "]" + "\n"

        sys.stdout.buffer.write(statement.encode('utf8'))

def doneTask(taskIndex):
    frame = sortTask()
    if 1 > taskIndex or taskIndex > len(frame):
        statement = "Error: no incomplete item with index #" + str(taskIndex) + " exists."
        sys.stdout.buffer.write(statement.encode('utf8'))
    else:
        # line to add in completed.txt file
        lineToComplete = frame[taskIndex - 1][0]

        # add completedTask in completed.txt
        with open(compFile, 'a') as f:
            f.write(lineToComplete + "\n")

        # find row of line to delete
        lineToDelete = str(frame[taskIndex - 1][1]) + " " + frame[taskIndex - 1][0]
        with open(taskFile, 'r') as f:
            counter = 0
            for line in f:
                counter += 1
                line = line.rstrip()
                if lineToDelete == line:
                    lineNumToDelete = counter
                    break

        # storing whole file lines
        with open(taskFile, 'r') as f:
            lines = f.readlines()
        # deleting whole file and again writing except delete_line

        with open(taskFile, 'w') as f:
            ptr = 1
            for line in lines:
                if ptr == lineNumToDelete:
                    pass
                else:
                    f.write(line)
                ptr += 1
        statement = "Marked item as done."
        sys.stdout.buffer.write(statement.encode('utf8'))

def deleteTask(taskIndex):
    frame = sortTask()
    if 1 > taskIndex or taskIndex > len(frame):
        statement = "Error: task with index #" + str(taskIndex) + " does not exist. Nothing deleted."
        sys.stdout.buffer.write(statement.encode('utf8'))
    else:
        lineNumToDelete = taskIndex

        # storing whole file lines
        with open(taskFile, 'r') as f:
            lines = f.readlines()
        # deleting whole file and again writing except delete_line

        with open(taskFile, 'w') as f:
            ptr = 1
            for line in lines:
                if ptr == lineNumToDelete:
                    pass
                else:
                    f.write(line)
                ptr += 1
        statement = "Deleted task #" + str(taskIndex)
        sys.stdout.buffer.write(statement.encode('utf8'))


if __name__ == '__main__':
    if not exists(taskFile):
        file = open(taskFile, 'w')
        file.close()
    if not exists(compFile):
        file = open(compFile, 'w')
        file.close()

    help_string ="""Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text "hello world" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics"""

    if len(argv) == 1:
        sys.stdout.buffer.write(help_string.encode('utf8'))
    elif argv[1] == 'help':
        sys.stdout.buffer.write(help_string.encode('utf8'))
    elif argv[1] == 'add':
        addTask()
    elif argv[1] == 'report':
        showReport()
    elif argv[1] == 'ls':
        showLs()
    elif argv[1] == 'done':
        if len(argv) < 3:
            statement = "Error: Missing NUMBER for marking tasks as done."
            sys.stdout.buffer.write(statement.encode('utf8'))
        else:
            doneTask(int(argv[2]))
    elif argv[1] == 'del':
        if len(argv) < 3:
            statement = "Error: Missing NUMBER for deleting tasks."
            sys.stdout.buffer.write(statement.encode('utf8'))
        else:
            deleteTask(int(argv[2]))