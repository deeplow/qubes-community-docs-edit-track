so I wanted a way to easily transfer my pass store to new appvms [without having to transfer gpg keys] should the need arise. pass doesn't provide any export functionality that I can see, so I threw together a couple of very simple scripts to accomplish the job and figured I'd share it with anyone who might be interested. 

disclaimer! **this method is unencrypted, so you should only transfer from and to non-networked appvms.** depending on your paranoia level, that may not be satisfactorily secure. anyways...

readme-
```

These scripts are designed to be run from the same directory and should be kept together.

There should be two (in addition to this readme):
	pass-import.sh
	pass-export.sh

Two more files will be created in the export process:
	pass-entries.txt
	pass-names.txt

These scripts assume that the VMs you plan on transferring your pass store from and to are both offline. Nonetheless, you should delete both these additional text files after the information has been successfully transferred as they are unencrypted.

These scripts assume that a pass store has already been set up on the target VM and is empty. You first run the pass-export script on the VM where your password store is currently located. Once the script has completed, you can either move/copy the script directory to the target VM, and run pass-import.sh from wherever you end up mounting it. That's all.

Be sure to compare password-stores (just a few random entries should do) before deleting the old VM.

This script may require you to input your gpg key on one or both VMs during execution.
It also assumes that each entry in your pass store is no more than 9 rows deep (to account for extra info), and that each password and empty row begins with a #.
```
export script-

```
#!/bin/bash
# print current password tree to the file "pass-names.txt" and create empty file called "pass-entries.txt"
pass > pass-names.txt
echo "" > pass-entries.txt
# alias the files
file1=./pass-names.txt
file2=./pass-entries.txt
# remove the first line in both files (blank line in the case of file2) and strip out the tree characters from file1
sed -i '1d' $file1
sed -i '1d' $file2
sed -i 's/[├─└]//g' $file1
# set a variable equal to the the contents of file1
names=$(cat $file1)
# for every name [in file1], append output of "pass [name]" to file2
for i in $names; do
pass $i >> $file2
done
```
import script-

```
#!/bin/bash
# alias the files containing the extracted website names and corresponding password/account info
file1=./pass-names.txt
file2=./pass-entries.txt
# declare variables equal to the contents of the files respectively
names=$(cat $file1)
entries=$(cat $file2)
# initialize a numeric variable to sync names with entries.
index=0
# for every name in file1, increment index by 9 
# then pipe the last 9 lines of the output of [index] lines in file2 to the command "pass insert -m [corresponding name in file1]"
for i in $names; do
let "index+=9"
head -n $index $file2 | tail -9 | pass insert -m $i
done
```