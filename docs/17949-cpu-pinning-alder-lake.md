If you have an Alder Lake or newer Intel CPU, you probably want the option to load a qube on the P or E cores, and this might help someone who is new to xen.

[https://dev.qubes-os.org/projects/core-admin/en/latest/libvirt.html](https://dev.qubes-os.org/projects/core-admin/en/latest/libvirt.html)
[https://libvirt.org/formatdomain.html#cpu-allocation](https://libvirt.org/formatdomain.html#cpu-allocation)

First, you need to add the following to GRUB
`dom0_max_vcpus=4 dom0_vcpus_pin`
If you want to use SMT read the notes at the end.

The CPU I’m using is the 12900K, which has 16 physical cores and 24 threads with SMT enabled.
The cores 0-15 are P cores and 16-23 are E cores.

If you want to move dom0 to the E cores, it can be done like this:

```
/usr/sbin/xl vcpu-pin Domain-0 0 20-23
/usr/sbin/xl vcpu-pin Domain-0 1 20-23
/usr/sbin/xl vcpu-pin Domain-0 2 20-23
/usr/sbin/xl vcpu-pin Domain-0 3 20-23
```
It will move dom0 from the first 4 cores to the last 4 cores, but it needs to be done every time the system boots.

It’s easy to make a xen-user.xml that uses jinja to automatically set the cpuset of a qube based on 
the name, this is an example of how you can do it with prefixing the name with p-core or e-core.

You probably don’t want to just make two groups, this is just an example of how it can be done.

```
{% extends 'libvirt/xen.xml' %}
{% block basic %}
	<name>{{ vm.name }}</name>
        <uuid>{{ vm.uuid }}</uuid>
        {% if ((vm.virt_mode == 'hvm' and vm.devices['pci'].persistent() | list)
            or vm.maxmem == 0) -%}
            <memory unit="MiB">{{ vm.memory }}</memory>
        {% else -%}
            <memory unit="MiB">{{ vm.maxmem }}</memory>
        {% endif -%}
	<currentMemory unit="MiB">{{ vm.memory }}</currentMemory>
	{% if vm.name.startswith('p-core') -%}
	    <vcpu cpuset="0-15">{{ vm.vcpus }}</vcpu>
	{% elif vm.name.startswith('e-core') -%}
	    <vcpu cpuset="16-23">{{ vm.vcpus }}</vcpu>
	{% else -%}
            <vcpu cpuset="0-15">{{ vm.vcpus }}</vcpu>
	{% endif -%}
{% endblock %}
```
If you want to see how your qubes are pinned, you can use the command:
`/usr/sbin/xl vcpu-list`

You can change the performance state of the individual cores:
`/usr/sbin/xenpm set-scaling-governor 0 performance`
This needs to be set every time the system boots, and the default setting is ondemand.

**Qubes admin events**

It's possible to use qubes admin events to pin or migrate qubes, this method has the advantage it happens after the qube has started, and it's possible to use on qubes that doesn't use xen-user.xml

```
#!/usr/bin/env python3

import asyncio
import subprocess

import qubesadmin
import qubesadmin.events

# i5-13600k (smt=off)
P_CORES = '0-5'
E_CORES = '6-13'

tag = 'performance'

def _vcpu_pin(name, cores):
    cmd = ['xl', 'vcpu-pin', name, 'all', cores]   
    subprocess.run(cmd).check_returncode()

def pin_by_tag(vm, event, **kwargs):
    vm = app.domains[str(vm)]
    if tag in list(vm.tags):
        _vcpu_pin(vm.name, P_CORES)
        print(f'Pinned {vm.name} to P-cores')
    else:
        _vcpu_pin(vm.name, E_CORES)
        print(f'Pinned {vm.name} to E-cores')

app = qubesadmin.Qubes()
dispatcher = qubesadmin.events.EventsDispatcher(app)
dispatcher.add_handler('domain-start', pin_by_tag)
asyncio.run(dispatcher.listen_for_events())
```
Thanks to @noskb for shown how to use admin events.

**CPU pools**

You can use CPU pools as an alternative to pinning, which has the advantage of the pool configuration being defined in a single place.

If you are using CPU pools with SMT enabled, you probably need to use the credit scheduler, SMT doesn't seem to work with credit2.

All cores start in the pool named Pool-0, dom0 needs to remain in Pool-0.

This is how you split the cores in a ecores and pcores pool, and leave 2 cores in Pool-0 for dom0.
> /usr/sbin/xl cpupool-cpu-remove Pool-0 2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23
> /usr/sbin/xl cpupool-create name=\"pcores\" sched=\"credit2\"
> /usr/sbin/xl cpupool-cpu-add pcores 2,3,4,5,6,7,8,9,10,11,12,13,14,15
> /usr/sbin/xl cpupool-create name=\"ecores\" sched=\"credit2\"
> /usr/sbin/xl cpupool-cpu-add ecores 16,17,18,19,20,21,22,23

When the pools have been created, you can migrate domains to the pools with this command:

> /usr/sbin/xl cpupool-migrate sys-net ecores

**Using qrexec to migrate qubes**

With CPU pools, it's easy to make a qrexec rpc command to allow qubes to request to be moved to pcores.

Policy files `/etc/qubes-rpc/policy/qubes.PCores`
```
$anyvm dom0 allow
```

Qubes-rpc file `/etc/qubes-rpc/qubes.PCores`
```
#!/bin/bash

pool=$(/usr/sbin/xl list -c $QREXEC_REMOTE_DOMAIN | awk '{if(NR!=1) {print $7}}')

if [[ $pool == "ecores" ]]; then
	/usr/sbin/xl cpupool-migrate $QREXEC_REMOTE_DOMAIN pcores
fi
```
From any qube you can use the command `qrexec-client-vm dom0 qubes.PCores` and the qube will be moved to pcores, if the qube currently is placed on ecores.

This allows you to start qubes on E cores, and be moved to P cores when you start a program that needs to run on P cores.

The qrexec can be added to menu commands

> Exec=bash -c ‘qrexec-client-vm dom0 qubes.PCores&&blender’

This is an example of how you can automatically move a qube to pcores when you start blender.

**Notes on SMT.**

Using `sched-gran=core` doesn't seem to work with Alder Lake, xen dmesg has the following warning.

```
(XEN) ***************************************************
(XEN) Asymmetric cpu configuration.
(XEN) Falling back to sched-gran=cpu.
(XEN) ***************************************************
```
Using SMT can be dangerous, and not being able to use sched-gran=core makes it more dangerous.

**Unless you understand and are okay with the consequences of enabling SMT, you should just leave it off.**

If you are running your system with SMT enabled you can take advantage of the fact that E cores can’t hyper thread, even with SMT enabled the E cores are essentially running with SMT off.

You can also disable SMT for individual cores by changing the cpuset, where you don't use the sibling core.

E.g. with SMT enabled, core 0 and 1 are running on the same physical core, but if you don't use core 1 that core is no longer able to hyper thread.

Disabling SMT is that same as xen using the cpuset 0,2,4,6,8,10,12,14