By default, the Qubes installation media only supports creating the core `sys-*` qubes derived from "full" Templates. :woozy_face:

For many users choosing Qubes OS for it's security & privacy efforts ...

![](upload://l0pfsSTWokBtwdNDGy1gGwnwrrc.gif)

---

Here is a simple `bash` solution:

[https://github.com/cayc3/swap-sys](https://github.com/cayc3/swap-sys)

---
# TL;DR:
1. Create TemplateVM + AppVM (Template for disposable) for each `sys-*` qubes
2. Shutdown `sys-*` qubes
3. Backup existing `sys-*` qubes
4. Remove existing `sys-*` qubes
5. Salt new `sys-*` qubes based on desired TemplateVM

---

[details="Note about driver selection:"]
For `sys-net`, be sure to replace `firmware-iwlwifi` in the script with appropriate drivers for system used.
[/details]

---

# Disclaimer:
IMO, "rebuilding" a Qubes install with only `dom0` + a single functional `TemplateVM` ought be within any Qubes operator's abilities.

If unable to read/understand this basic script, **DO NOT USE** as, there is a good chance failure to run successfully can lead to a system which feels unusable (not actually the case) and some novice users may feel as though a reinstall is necessary.