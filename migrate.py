import datetime
import re
import time
import os
from pathlib import Path

header_regex = re.compile("^(#+) *(.+)")
todo_task_regex = re.compile("^\\[([ \\.xX-]*)\\]")
todo_task_regex_keep = re.compile("^\\[([ \\.]*)\\]")
start_spaces = re.compile("^[\t ]*")
rep_task_regex = re.compile("([0-9]+)[xX]([0-9]+)")
rep_task_regex_any = re.compile(".+?(([0-9]+)[xX]([0-9]+))")
rep_task_regex_prefix = re.compile(".+?(?=[0-9])")

def process_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    lines = [line.replace('\t', '    ') for line in lines]

    indices_to_remove = []  # we'll remove these lines
    output_lines = lines.copy()  # what we'll return 
    delete_nested, indent_len = False, 0  # to know if we delete nested

    for ind, line in enumerate(lines):

        if len(line) < 1:  # remove if empty
            indices_to_remove.append(ind)
            delete_nested, indent_len = False, 0
        elif delete_nested and indent_len < len(line) - len(line.lstrip(' ')):
                indices_to_remove.append(ind)
        # if not-bullet, skip
        elif line.lstrip(' ')[0] != '-':
            pass # could happen to mantain '[x] note without bullet'
        else:
            if delete_nested:  # indentation level does not imply deletion
                delete_nested, indent_len = False, 0

            aline = line.lstrip(' ')[1:].lstrip(' ')  # remove '-  '
            # if rep pattern, reset and remove symbol [x]
            if rep_task_regex_any.match(aline):
                prefix_len = len(rep_task_regex_prefix.match(aline).group())
                new_aline = aline[:prefix_len] + '0x' + aline[prefix_len:].lower().split('x')[1]  # reset
                if todo_task_regex.match(aline):
                    new_aline = new_aline.split('[')[0] + '[ ]' + new_aline.split(']')[1]  # remove symbols
                output_lines[ind] = line.split('-')[0] + '- ' + new_aline
            # if bullet not completed, reset  (if pomodoro pattern, remove dots)
            elif todo_task_regex_keep.match(aline):
                new_line = '[ ]' + aline[len(todo_task_regex.match(aline).group()):]
                output_lines[ind] = line.split('-')[0] + '- ' + new_line
            # if bullet completed [x] or discarded [-] go to nested and delete all
            elif todo_task_regex.match(aline):
                delete_nested = True
                indent_len = len(line) - len(line.lstrip(' '))
                indices_to_remove.append(ind)
    
    output_lines = [out_line for ind, out_line in enumerate(output_lines) if ind not in indices_to_remove]
    return output_lines

def run_migrate(filename=None, reset=False):
    # current filename as string, e.g. "2022_01_11.md"
    current_date = datetime.datetime.now().strftime("%Y_%m_%d")
    today_filename = current_date + '.md'

    # delete file or exit if file already exists
    if reset and today_filename in os.listdir():
        input("Do you really want to remove today's file?")
        os.remove(today_filename)
    elif today_filename in os.listdir():
        print("Today's entry already exists!")
        exit()

    # create file from scratch
    open(today_filename, 'w').close()

    # get latest date contents
    if not filename:
        latest_filename = sorted([fname for fname in os.listdir() if fname != today_filename and fname[:2]=='20' and fname[-3:] == '.md'])[-1]
    else:
        latest_filename = filename

    # process filename
    output_lines = process_file(latest_filename)

    # write 
    with open(today_filename, 'a') as f:
        f.writelines(output_lines)


if __name__ == '__main__':
    run_migrate()
