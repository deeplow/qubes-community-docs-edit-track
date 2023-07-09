Just in case anyone needs help with this to resize dom0 from say 20G to 50G. I needed the extra space in order to install the kali community qubes template.

Run these in dom0 terminal:

sudo lvresize --size 50G /dev/mapper/qubes_dom0-root
sudo resize2fs /dev/mapper/qubes_dom0-root