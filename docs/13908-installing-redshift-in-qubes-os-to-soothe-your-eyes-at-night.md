Anyone who's used a computer screen at night will tell you that blue light hurts your eyes.  

Most OSes have a "Night Mode" that will lower the intensity of blue light that your display emits, reducing eye strain at night.  Unfortunately, the standard Qubes OS install does not contain anything that will do this.   

The standard Fedora repos include a package called `redshift` that will accomplish this.  

1.  In a dom0 terminal, type:
```
sudo qubes-dom0-update redshift
```
2.  Get your current latitude and longitude coordinates
-  If you're concerned about privacy, you can be Santa Claus if you want: 90.0000° N, 135.0000° W (The North Pole)
-  Bear in mind that if you do this, your screen will redshift for six months, and then blueshift for six months :stuck_out_tongue:
-  The `redshift` command seems to require a value at `-l LAT:LON` in order to be successful, but you can manually toggle colour-shifting as well.  

3.  Complete one of the following steps:
-  For automatic colour-shifting based on your system clock: 
```
redshift -l $latitude:$longitude &
```

-  For manual "oneshot" colour-shifting: 
```
redshift -l $latitude:$longitude -O $colour_temperature
```

-  To see what other options `redshift` can do: 
```
redshift -h
```
-----

I will write a way to have `systemd` activate this automatically in a future post.