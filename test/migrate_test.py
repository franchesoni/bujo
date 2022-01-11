expected = """
# Work
- [ ] Write tests
    - [ ] migrate
# Test Data
- note
-
- [ ] nesting1
    - [ ] nesting 2
        - [ ] nesting 3
            - [ ] nesting 4
                - notes of note done thing
- tabbing
    - [ ] tabs migrated
    - notes
# Nothing done
- [ ] not done
- note
# Repetition
- [ ] 0x5 things
- [ ] 0x2 other things
- [ ] Group
    - [ ] 0x3 nesting rep
    - [ ] 0x6 done nested rep
# Pomodoros
- [ ] not done
- [ ] partly done
"""

import os
from migrate import run_migrate

if __name__ == '__main__':
    # copy migrate script to this dir to use
    run_migrate('2022_01_09_test_input.md', reset=True)

    with open('test_expected.md', 'w') as f:
        f.write(expected)

    with open('test_expected.md', 'r') as f:
        expected_lines = f.read()

    latest_filename = sorted([fname for fname in os.listdir() if fname[:2]=='20' and fname[-3:] == '.md'])[-1]
    with open(latest_filename, 'r') as f:
        lines = f.read()

    assert lines.replace('\n', '') == expected_lines.replace('\n', '')
    os.remove('test_expected.md')


