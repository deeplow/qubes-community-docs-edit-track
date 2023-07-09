Here are short instructions to build an up to date Fedora template the absolute quickest way and minimal headache. Maybe not 60 seconds...but this is a high level overview.

Advantages and disadvantages are covered after.
  
```shell
# Get the qubes builder
git clone https://github.com/QubesOS/qubes-builder
cd qubes-builder
# Use the base config already in the repo
cp example-configs/templates.conf builder.conf

# Append custom settings to builder.conf
# Better to update values in-place, but this is the 60 second version
cat >>builder.conf <<EOF

# Build Fedora 33; fc33+minimal or other flavors could be given
DISTS_VM = fc33

# Use the Qubes online repo for Qubes packages since we are not building them
USE_QUBES_REPO_VERSION = \$(RELEASE)

# Use the 'current' repo; not 'current-testing'
USE_QUBES_REPO_TESTING = 0

# Don't build dom0 packages
TEMPLATE_ONLY = 1

# Since this is TEMPLATE_ONLY, list the only components needed
TEMPLATE = builder-rpm linux-template-builder

EOF

# install build dependencies
make install-deps

# Download and verify sources (only Qubes git repos)
make get-sources-git

# Build the template
make template
```

The template will be at `qubes-src/linux-template-builder/rpm/noarch/*.rpm`

To give the template a different name so that it can be installed alongside the official Fedora templates and is not seen as an update,

```shell
make TEMPLATE_NAME=fedorabuilt template
```

Advantages:

- No build chroot is setup, no code is actually compiled saving download and time compared to a normal build
- Uses official Qubes repo for qubes packages
- Downloads most up-to-date Fedora packages at build time, so no need to download 2GB of templates and an additional 1GB of updates
- Moves more download bandwidth onto Fedora mirrors as opposed to Qubes/Qubes mirrors
- Learn how the Qubes build process works


Disadvantages:

- Doesn't build Qubes packages from source? Check your threat model first
- The template RPM will be unsigned, which makes installing it more difficult in Qubes. This is meant to be installed on the same computer; distribution is not recommended.
- Depending on internet speed and computer performance, it may take more time
- If the build fails, debugging is not very fun

This same process should in theory work on other templates (Debian, Archlinux), but may require some COMPONENTS to be built first.

This means: add more components to the `TEMPLATE` variable, `make get-sources`, `make qubes-vm`, then `make template`.