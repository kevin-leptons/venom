# VENOM

![venom-logo](asset/venom-64.png)

[![Build Status](https://travis-ci.org/kevin-leptons/venom.svg?branch=master)](https://travis-ci.org/kevin-leptons/venom)

GNOME theme for Debian-8 system

Kevin Leptons <kevin.leptons@gmail.com> <br>
CC by 4.0 License <br>
May, 2017

# FEATURES

- Monochrome
- High contrast
- No border radius
- No shadow
- Help people focus on work
- Improve performance of GNOME

[Screen record on Youtube](http://www.youtube.com/watch?v=3z9AfzKiYHM)

![venom-green](asset/venom-black.png)

# USAGE

Download [venom_1.2.0-0_all.deb](https://drive.google.com/open?id=0B6Eqm2oY7b1vRnM3bklZZjB2TW8),
then follow instructions

```bash
# install
dpkg -i venom_1.2.0-0_all.deb
apt-get install -f

# use theme
# you can replace black with green or orange
venom use black

# for detail manual, look man page
man venom
```

# DEVELOPMENT

```bash
# get source files
git clone https://github.com/kevin-leptons/venom.git
cd venom

# enter python virtual environemtn
./env init
. venv/bin/active
./env install

# test
./ctl test

# build and pack
./ctl build
./ctl dist
```

[Full development documents](doc/dev.md)

# REFERENCES

- [Homepage](https://kevin-leptons.github.io/venom/)
- [Change log](changelog.md)
- [Screenshots](doc/screenshot.md)
- [Pre-builds](https://drive.google.com/open?id=0B6Eqm2oY7b1vVG55VjJrcGE3aU0)
- [GNOME](https://en.wikipedia.org/wiki/GNOME)
- [Debian](https://en.wikipedia.org/wiki/Debian)
