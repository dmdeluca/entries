# entries

Entries is a small python project that reads and writes journal entries. It is designed to make journaling simple and easy.

## commands

By default, entries runs in write mode, in which a user types entries in succession separated by a carriage return. However, by adding `r` to the command, you can read past journal entries by entering dates.

### examples

`python entries.py` -> runs the program in write mode.

`python entries.py r` -> runs the program in read mode.

To search for entries in read mode, type something like `july august --has apartment linda`.

## future directions

In the future, entries will have the following features:
* Search past entries by keyword
* Edit past entries
* Add search keywords to starting command
