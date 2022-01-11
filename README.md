# BuJo

Bullet-journal.

## Software
Markdown because it's awesome, and Python because it's easy. The `migrate.py` here provided will take your last record, create a new one for today, and migrate all uncompleted tasks (if any).

## How it works

You should use bullets (`-`), as everything else will be preserved. To mark a task as completed (thus not migrating it), you can write:
`- [x] my completed task`

Of course, if you complete a big task, every child will die, as follows:
```
- [x] my completed big task
    - [ ] my uncompleted task to dissapear
```

You can also drop tasks `[-]` and count time in "Pomodoro units" `[..]` which will be erased. 

Finally, you can set habits. Something like `- [x] 10x5 pushups` or `- [ ] 0x4 emails`. The counter will reset to 0 after migration.

Credit to [this Go version](https://github.com/dballard/markdown-bullet-journal)