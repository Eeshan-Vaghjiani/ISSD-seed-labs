# A separate evidence shell: ordinary-user execution with output-only recording.
unset PROMPT_COMMAND
HISTFILE="$LAB_EVIDENCE/terminal-$LAB_ROLE.history"
HISTCONTROL=
HISTSIZE=100000
HISTFILESIZE=100000
shopt -s histappend
PS1='\u@\h [${LAB_ROLE}:lab-files]\$ '
PS2='> '
PS4='+ '
export PS1 PS2 PS4
printf '\033]0;%s\007' "$LAB_TITLE"
cd /home/seed/issd-member5/lab-files
printf 'Member 5: %s\n' "$LAB_TITLE"
printf 'Visible desktop automation; full output and scrollback retained.\n'
printf 'Session: %s\nTranscript: %s/terminal-%s.typescript\n' \
    "$LAB_SESSION" "$LAB_EVIDENCE" "$LAB_ROLE"
id
pwd
date -Is
if [[ $(id -u) != 1000 || $EUID != 1000 ]]; then
    printf 'Expected ordinary seed shell; stopping.\n' >&2
    exit 1
fi
