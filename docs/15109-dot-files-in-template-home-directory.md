Hello,

If I want to configure an application in multiple qubes, where can I put the config files (i.d., dot files [0]) in the template so that I can configure it once and have the changes in every qube based on that template? Is this where bind-dirs[1] come in?

As an example, I would like to have my standard emacs configurations automaticly present in every qube I base on my debian template.

If I understand Qubes correctly, the app qubes won't receive a copy of template's home directory---only the root file structure, but they have a separate home directory. Do I need to configure each app qube's applications separately, or can I do so in their template?

Thanks in advance if you happen to have time to answer!




[0] https://forum.qubes-os.org/t/what-exactly-are-dot-files-how-do-you-guys-save-and-recreate-your-setup-automatically/10558/2

[1] https://www.qubes-os.org/doc/bind-dirs/