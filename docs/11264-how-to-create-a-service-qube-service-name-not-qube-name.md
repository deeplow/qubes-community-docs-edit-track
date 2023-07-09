I could just clone a service qube, sure.

But what if I don't want it to inherit everything from the clone-donor.

What if I want to start from scratch?

Using GUI to create a qube creates a qube with the 'Qube:name' format.

I want to create a service qube with the 'Service:name' format.

Is there a CLI trick to this?  Or a GUI trick to this?

I'm specifically looking to create another disposable sys-net.  I'm operating with disposable sys-net by default, but I want another one which is based on a different templateVM.  The goal is to have two sys-nets, one of which randomizes MAC address and host name, and one which maintains it's original state.
 
(use the forum search function to learn how to randomize; I'll place a link here once I've figured out how)

I've tried cloning 'Service: sys-net' (disposable in my case) but that forces it to inherit it's default template qube.  Is it possible to change the template of a cloned qube after creation?

However it's achieved, the logic here being that it can't have the same default template as that would mean the two qubes would function identically but just have different names.

'sys-net' and 'sys-net random' both require different templates to have distinctly separate functions.