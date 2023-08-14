[Syncthing](https://syncthing.net/) is an awesome piece of software used to keep files in sync across multiple devices using end-to-end encryption without requiring port forwarding or leaving files on a third-party server.

This guide is intended to allow syncing of files in netvm-less qubes across two (or more) devices running Qubes. This could be used to sync bookmarks for split-browser, or for keeping a KeepassXC file up to date.


## Requirements

You will need to install `syncthing` in the **template**

:exclamation:***This relies on the previous guide for using `qubes-sync` with multiple qubes*** (<https://forum.qubes-os.org/t/use-qubes-sync-with-multiple-clients-and-one-server/19780>). It assumes this directory structure exists:

```
/rw/syncdir/
  authorized_keys/
  clientvm1/
    writable/
  clientvm2/
    writable/
```

In this structure, all directories except `writable` are owned by root. Each `writable` folder is owned by a single user per client qube.

## Set up syncthing

Run syncthing as root (this is used to manage file ownership correctly, and it's not a security risk for an appvm):
```
sudo syncthing -home /rw/syncdir/syncthing-config
```

Add a new folder with the label "syncdir" and set the path to `/rw/syncdir`. Add these ignore patterns for this folder:
```
/authorized_keys/*
/sshd_config-addition
/syncthing-config
```

Enable "Copy Ownership From Parent" in Actions > Advanced > Folder "syncdir"

Add a new device and share the folder with it. Accept the share on the new device.

Once the folder has been synced to the new device, manually set permissions to the correct user for the new device. Do this for every `/writable` folder.
```sh
chown -R sync-$CLIENTNAME /rw/syncdir/$CLIENTNAME/writable
```

### Start syncthing automatically

Append this to `/rw/config/rc.local`:
```sh
sudo syncthing -no-browser -home /rw/syncdir/syncthing-config
```

## Set up split-browser sync

Create a new file `/etc/split-browser/00-sync.bash` in the **template** for `split-browser`

```
SB_DATA_DIR=${SB_DATA_DIR:-~/sync/split-browser}
```

Then copy any existing data to the sync folder in the `split-browser` **appvm**:
```sh
cp -r ~/.local/share/split-browser ~/sync/
```