<!--- Before asking, did you search first? Press 🔍 at the upper right to search. ---->

Auto complete vm names and basic options example:
```
# qvm-check(1)                                             -*- shell-script -*-

_qvm_check()
{
    local cur prev words cword
    _init_completion || return

    if [[ $cur == -* ]]; then
        COMPREPLY=($(compgen -W '$(_parse_help "$1")' -- "$cur"))
    else
        COMPREPLY=($(IFS=$'\n' compgen -W '$(qvm-ls --raw-list)' -- "$cur"))
    fi  

} &&
    complete -F _qvm_check qvm-check
```

if you add the above script to `/usr/share/bash-completion/completions/qvm-check`

and install the required package with `sudo qubes-dom0-update bash-completion`

and source the functions and all completions with `source /usr/share/bash-completion/bash_completion`

you would se VMNAMES with:
`qvm-check <TAB><TAB>`

and option names with:
`qvm-check --<TAB><TAB>`

The above script is just an example, some `qubes-` and `qvm-` scripts require arguments and specific properties.

Would be great if more people contributed to other qubes specific scripts and maybe even push upstream to https://github.com/scop/bash-completion/tree/master/completions

For the next person trying bash-completion for `qubes-prefs`:
- to get all properties listed: `qubes-prefs --help-properties | cut -d " " -f3 | grep -v "^$"`