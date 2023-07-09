This is how to use me_cleaner on the T480, but this will work on other laptops as well.

The main requirement is an eprom programmer, you are going to need to read and write the firmware eprom. The CH341a is a cheap ($10) option that should work with most roms, you are also going to need a clip to connect the programmer to the chip.

**Read the ROM**

First you need to dump the rom, if you don't know how to find the EPROM search Google.

> $ flashrom -p ch341a_spi -r firmware.rom

If this fails and return a list of possible chip types, then you need to specify the chip to be used, picking any chip from the list should work, you use -c to specify the chip type.

> $ flashrom -p ch341a_spi -c MX25L12805D -r firmware.rom

[details="Command output"]
```
$ flashrom -p ch341a_spi -c MX25L12805D -r firmware.rom
flashrom v1.2 on Linux 5.15.0-48-generic (x86_64)
flashrom is free software, get the source code at https://flashrom.org

Using clock_gettime for delay loops (clk_id: 1, resolution: 1ns).
Found Winbond flash chip "MX25L12805D" (16384 kB, SPI) on ch341a_spi.
Reading flash... done.
$
```
[/details]

When you are able to read the firmware, you should read it 2-3 times and compare the files using the `md5sum` command. It's very important that you have a valid and verified ROM dump, if you have multiple files with the same md5 checksum you know it is a valid dump.

**NOT HAVING A VALID BACKUP CAN RESULT IN YOU BRICKING THE LAPTOP**

> $ md5sum firmware1.rom firmware2.rom firmware3.rom

[details="Command output"]
```
$ md5sum firmware1.rom firmware2.rom firmware3.rom
3e83a431f807d483e63a7aae55c73b89  firmware1.rom
3e83a431f807d483e63a7aae55c73b89  firmware2.rom
3e83a431f807d483e63a7aae55c73b89  firmware3.rom
$
```
[/details]

**Cleaning the ROM**

*Cleaning the ROM on the T480 adds a 30 sec boot delay, unless you really want the ROM cleaned, you should use the HAP disable method.*

All you need to do to clean the dump is use me_cleaner, it will create a new image with ME removed, which you can write to the firmware EPROM.

> $ ~/src/me_cleaner/me_cleaner.py firmware.rom -S -O clean.rom

On newer versions of ME this is not likely to work without whitelisting ME modules, which is done with the -w option. On the T480, you need to whitelist DLMP and MFS.

> $ ~/src/me_cleaner/me_cleaner.py firmware.rom -S -w DLMP,MFS -O clean.rom

[details="Command output"]
```
$ ~/src/me_cleaner/me_cleaner.py firmware.rom -S -w DLMP,MFS -O clean.rom
Full image detected
Found FPT header at 0x3010
Found 11 partition(s)
Found FTPR header: FTPR partition spans from 0x1000 to 0xa8000
Found FTPR manifest at 0x1478
ME/TXE firmware version 11.8.92.4222 (generation 3)
Public key match: Intel ME, firmware versions 11.x.x.x
The HAP bit is NOT SET
Reading partitions list...
 FTPR (0x00001000 - 0x0000a8000, 0x000a7000 total bytes): NOT removed
 FTUP (0x00110000 - 0x0001bc000, 0x000ac000 total bytes): removed
 DLMP (0x000a6000 - 0x0000a9000, 0x00003000 total bytes): NOT removed
 PSVN (0x00000e00 - 0x000001000, 0x00000200 total bytes): removed
 IVBP (0x0010c000 - 0x000110000, 0x00004000 total bytes): removed
 MFS  (0x000a8000 - 0x00010c000, 0x00064000 total bytes): NOT removed
 NFTP (0x00110000 - 0x0001bc000, 0x000ac000 total bytes): removed
 ROMB (      no data here      , 0x00000000 total bytes): nothing to remove
 FLOG (0x001bc000 - 0x0001bd000, 0x00001000 total bytes): removed
 UTOK (0x001bd000 - 0x0001bf000, 0x00002000 total bytes): removed
 ISHC (      no data here      , 0x00000000 total bytes): nothing to remove
Removing partition entries in FPT...
Removing EFFS presence flag...
Correcting checksum (0x5e)...
Reading FTPR modules list...
 FTPR.man     (uncompressed, 0x001478 - 0x002064): NOT removed, partition manif.
 rbe.met      (uncompressed, 0x002064 - 0x0020fa): NOT removed, module metadata
 fptemp.met   (uncompressed, 0x0020fa - 0x002132): NOT removed, module metadata
 kernel.met   (uncompressed, 0x002132 - 0x0021c0): NOT removed, module metadata
 syslib.met   (uncompressed, 0x0021c0 - 0x002224): NOT removed, module metadata
 bup.met      (uncompressed, 0x002224 - 0x0027e6): NOT removed, module metadata
 pm.met       (uncompressed, 0x0027e6 - 0x002894): NOT removed, module metadata
 vfs.met      (uncompressed, 0x002894 - 0x0031c0): NOT removed, module metadata
 evtdisp.met  (uncompressed, 0x0031c0 - 0x00334e): NOT removed, module metadata
 loadmgr.met  (uncompressed, 0x00334e - 0x003476): NOT removed, module metadata
 busdrv.met   (uncompressed, 0x003476 - 0x0037fa): NOT removed, module metadata
 gpio.met     (uncompressed, 0x0037fa - 0x003944): NOT removed, module metadata
 prtc.met     (uncompressed, 0x003944 - 0x003af4): NOT removed, module metadata
 policy.met   (uncompressed, 0x003af4 - 0x003cb4): NOT removed, module metadata
 crypto.met   (uncompressed, 0x003cb4 - 0x003e3e): NOT removed, module metadata
 heci.met     (uncompressed, 0x003e3e - 0x00400a): NOT removed, module metadata
 storage.met  (uncompressed, 0x00400a - 0x004306): NOT removed, module metadata
 pmdrv.met    (uncompressed, 0x004306 - 0x00442a): NOT removed, module metadata
 maestro.met  (uncompressed, 0x00442a - 0x004514): NOT removed, module metadata
 fpf.met      (uncompressed, 0x004514 - 0x00462c): NOT removed, module metadata
 hci.met      (uncompressed, 0x00462c - 0x00472e): NOT removed, module metadata
 fwupdate.met (uncompressed, 0x00472e - 0x004836): NOT removed, module metadata
 ptt.met      (uncompressed, 0x004836 - 0x004942): NOT removed, module metadata
 touch_fw.met (uncompressed, 0x004942 - 0x004a80): NOT removed, module metadata
 rbe          (Huffman     , 0x004a80 - 0x007940): NOT removed, essential
 fptemp       (LZMA/uncomp., 0x007940 - 0x009940): removed
 kernel       (Huffman     , 0x009940 - 0x019980): NOT removed, essential
 syslib       (Huffman     , 0x019980 - 0x02abc0): NOT removed, essential
 bup          (Huffman     , 0x02abc0 - 0x0546c0): NOT removed, essential
 pm           (LZMA/uncomp., 0x0546c0 - 0x056980): removed
 vfs          (LZMA/uncomp., 0x056980 - 0x05ec80): removed
 evtdisp      (LZMA/uncomp., 0x05ec80 - 0x060640): removed
 loadmgr      (LZMA/uncomp., 0x060640 - 0x0634c0): removed
 busdrv       (LZMA/uncomp., 0x0634c0 - 0x064d40): removed
 gpio         (LZMA/uncomp., 0x064d40 - 0x065e40): removed
 prtc         (LZMA/uncomp., 0x065e40 - 0x0669c0): removed
 policy       (LZMA/uncomp., 0x0669c0 - 0x06b700): removed
 crypto       (LZMA/uncomp., 0x06b700 - 0x0793c0): removed
 heci         (LZMA/uncomp., 0x0793c0 - 0x07d280): removed
 storage      (LZMA/uncomp., 0x07d280 - 0x0816c0): removed
 pmdrv        (LZMA/uncomp., 0x0816c0 - 0x082840): removed
 maestro      (LZMA/uncomp., 0x082840 - 0x0845c0): removed
 fpf          (LZMA/uncomp., 0x0845c0 - 0x085f80): removed
 hci          (LZMA/uncomp., 0x085f80 - 0x086800): removed
 fwupdate     (LZMA/uncomp., 0x086800 - 0x08b540): removed
 ptt          (LZMA/uncomp., 0x08b540 - 0x0a0e80): removed
 touch_fw     (LZMA/uncomp., 0x0a0e80 - 0x0a8000): removed
The ME minimum size should be 1118208 bytes (0x111000 bytes)
The ME region can be reduced up to:
 00003000:00113fff me
Setting the HAP bit in PCHSTRP0 to disable Intel ME...
Checking the FTPR RSA signature... VALID
Done! Good luck!
$
```
[/details]

On other laptops, finding the modules you need to whitelist is going to require some trial and error. Adding all the modules from the partition list and removing them one at a time is one way to do it, but it does take some time because you need to flash the ROM multiple times.

**HAP disabling ME**

HAP disabling ME doesn't modify the ME section of the ROM, it sets a bit in the Intel Flash Descriptor (IFD). Because it doesn't delete the ROM content you don't need to worry about whitelisting modules.
> $ ~/src/me_cleaner/me_cleaner.py firmware.rom -s -O disabled.rom
[details="Command output"]
```
$ ~/src/me_cleaner/me_cleaner.py firmware.rom -s -O disabled.rom
Full image detected
Found FPT header at 0x3010
Found 11 partition(s)
Found FTPR header: FTPR partition spans from 0x1000 to 0xa8000
Found FTPR manifest at 0x1478
ME/TXE firmware version 11.8.92.4222 (generation 3)
Public key match: Intel ME, firmware versions 11.x.x.x
The HAP bit is NOT SET
Setting the HAP bit in PCHSTRP0 to disable Intel ME...
Checking the FTPR RSA signature... VALID
Done! Good luck!
$
```
[/details]

**Write the ROM**

When you have made an image with me_cleaner you just need to write it to the EPROM, and you are done.

> $ flashrom -p ch341a_spi -c MX25L12805D -w new_firmware.rom
[details="Command output"]
```
$ flashrom -p ch341a_spi -c MX25L12805D -w new_firmware.rom
flashrom v1.2 on Linux 5.15.0-48-generic (x86_64)
flashrom is free software, get the source code at https://flashrom.org

Using clock_gettime for delay loops (clk_id: 1, resolution: 1ns).
Found Winbond flash chip "W25Q128.V" (16384 kB, SPI) on ch341a_spi.
Reading old flash chip contents... done.
Erasing and writing flash chip... Erase/write done.
$
```
[/details]

**Unbrick your laptop**
If the laptop is unable to boot, you can flash the original ROM, make sure you make a backup of the original ROM.

If you tried to clean the ROM, and it doesn't work, you can always try to HAP disable ME.