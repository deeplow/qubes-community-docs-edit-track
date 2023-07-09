Hello all,

I want to share a nice trick I learned a few years ago from a blog entry written by Lars Michelsen (https://larsmichelsen.com/ ) which unfortunately disappeared¹ from the WWW in the meanwhile.

Before I begin tinkering around on newly installed systems like for example the Qubes OS 4.1.0-rc4 which came out last week I usually add the following three lines to my $HOME/.bashrc file:
     
```
     if [ -z "$HISTTIMEFORMAT" ]
     then export HISTTIMEFORMAT="%F %T "
     fi
```

Why this?  If the variable HISTTIMEFORMAT is set in an interactive shell this shell starts to record additional timestamps when commands were entered into the $HOME/.bash_history file.  Together with increased size settings for the HISTSIZE and/or HISTFILESIZE variables and archives of my .bash_history files this has been extremly helpful for me to document my activities not only in Qubes OS.

I hope someone else will find this as helpful as I did.
I would love to see this included as a default in future versions of Qubes OS.

Best regards, Peter Funk
footnote ¹): original path was larsmichelsen.com/open-source/bash-timestamp-in-bash-history/