# [Bash tips for everyday at the command line (Ubuntu)](https://opensource.com/article/18/5/bash-tricks)

```bash
# History related
!! # rerun last command
!* # reuse arguments from previous command
!$ # use last argument of last command
shopt -s histappend # allow multiple terminals to write to the history file
# list the most used history commands
history | awk 'BEGIN {FS="[ \t]+|\\|"} {print $3}' | sort | uniq -c | sort -nr | head

# File and navigation
cp /home/foo/realllylongname.cpp{,-old}
cd -
rename 's/text_to_find/been_renamed/' *.txt
export CDPATH='/var/log:~' # variable is used with the cd built-in.

# Bash shortcuts
    shopt -s cdspell (corrects typoos)
    ctrl + _ (undo)
    ctrl + arrow (move forward a word)
    ctrl + a (move cursor to start)
    ctrl + e (move cursor to end)
    ctrl + k (cuts everything after the cursor)
    ctrl + l (clears screen)
    ctrl + q (resume command that is in the foreground)
    ctrl + s (pause a long running command in the foreground)
    ctrl + t (swap two characters)
    ctrl + u (cuts everything before the cursor)
    ctrl + x + ctrl + e (opens the command string in an editor so that you can edit it before it runs)
    ctrl + x + * (expand glob/star)
    ctrl + xx (move to the opposite end of the line)
    ctrl + y (pastes from the buffer)
    ctrl + shift + c/v (copy/paste into terminal)

# Running commands in sequence
&& # run second command if the first is successful
; # run second command regardless of success of first one

# Redirecting I/O
2>&1 (redirect stdout and stderr to a file)

# check for open ports
echo > /dev/tcp/<server ip>/<port>
`` (use back ticks to shell out)

# Examine executable
which <command>
file <path/to/file>
command -V <some command binary> (tells you whether <some binary> is a built-in, binary or alias)
```