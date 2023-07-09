**1.** Create a new qube with these settings:

**Type:** AppVM
**Template:** Fedora
**Networking:** sys-firewall
**Advanced:** check "provides network" and "launch settings after creation"

![1|625x338, 50%](upload://3qF0DOqCDOP3t3yPBR4kAl9NoWE.png) 

**2.** When the created-qube window settings showsup, go directly to tab **"Services"**
**2.1** Select the service **"network-manager"** then click "+" to add the respective service
**2.2** Check the **"network-manager"** field box then **"Apply"** -> **"OK"**

![2|601x500, 50%](upload://b1F9pql0DVYxMzjjsbwYy5hGyha.png) 

**3.** [Download the vpn config file from ovpn website](https://www.ovpn.com/en/guides/android-connect) (this guide used the 'finland' ovpn config file)

![5|690x372, 50%](upload://bHJkkEqmbytfN7oV82XniRHGr61.png) 

**4.** Use the **file manager** to access the folder with the **downloaded ovpn-config-file** 
**4.1** Move the file to the **created-qubes-appvm**

![6|690x372, 50%](upload://7ZTddaejOmddBbHOMZlmT2pmilm.png) 

**5.** If you have done everything right then the created-qubes-appvm will start automatically and will receive ovpn-config-file.

![7|198x141, 50%](upload://lu0KxlLMy0doL6fnIajp21z5inY.png) 

**6.** An ethernet network connection icon from the created-qube-appvm will show up on "notification area" after the appvm start.

**6.1** Select and go to: **Ethernet Network -> VPN Connections ->** ****Add a VPN connection...***

![8|514x211, 50%](upload://vZdvBxcaywVZSQE9tKruCpWsw9u.png) 

**6.2** Choose **"Import saved VPN configuration"**

![9|605x261, 50%](upload://A0OYX3sqdOvZmq87yJoHShBZ7jR.png) 

**6.3** Browse to **"QubesIncoming"** directory and select the downloaded ovpn-config-file.

![10|675x500, 50%](upload://ckAI5oSC2bHFJwout8lFjlFe10M.png) 

**7.** A window will show up with the ovpn configuration, **select the "VPN" tab**
****7.1**** On the "Authentication" field type your "ovpn login" and "password" then "SAVE"

![11|411x500, 50%](upload://jgSxfztB9wjSrDh368wh9VfsAz5.png) 

**8.** Choose password for **keyring** or leave blank

![12|690x192, 50%](upload://tV7kZLRtQuPaZbjjmE4w4Kx2wgq.png) 

**9.** **Connect to OVPN:** Notification Area -> Ethernet Network -> VPN Connections -> ***OVPN_CONFIG**(fi.helsinki.ovpn.com)*

![13|470x231, 50%](upload://h4NHx7FJYHKHp5Jz5uPHKGBcgJX.png) 

**10.** Check the connection using the **[OVPN SITE](https://www.ovpn.com)** trough the top menu.

![16|690x372, 50%](upload://7YPy0sVP7J3iigVU83nC0RxCasQ.png) 

If you have done everything right then you're browsing trough OVPN.

**If your vpn connection goes down while you're browsing you can prevent dns-leak:**

**1.** Open the Qube-Manager, select the created-qubes-appvm and open the qubes settings

![19|690x326, 50%](upload://sy2RZL4QNBs0y2YAMwmheo0zvD6.png) 

**2.** Go to the **"Firewall rules"** TAB and select the **"Limit outgoing internet connections to..."** option

![20|602x500, 50%](upload://qhhOITdOML645cGl97spol2yr7u.png) 

**3.** Click **"+"** then type the remote address
**3.1** To find the correct addresss open the downloaded ovpn-config-file with text-editor

![17|690x481, 50%](upload://sAuFo1HmgXwsxknj8fX9X0JXlJ3.png) 

**3.2** Locate the **"remote"** line address and copy it.

![18|607x500, 50%](upload://wSo24WsSZRtJkhUVrIPLUMUxGkQ.png) 

**3.3** Go back to **"Firewall rules"** TAB, click **"+"** to fill in the fields with the copied address:

**Address:** pool-1.prd.fi.helsinki.ovpn.com(the one used in this guide is the finland ovpn-config-file)
**Port/Service:** Leave blank
**Protocol:** Any

![3|601x500, 50%](upload://gGKyHdL74IzW7pLVLxtOayH0VWX.png) 

**4.** Click **"Apply"** then **"OK"** and enjoy it.