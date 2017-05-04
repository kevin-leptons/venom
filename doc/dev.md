# Contributions

## Enter virtual environment

```bash
# Ensure that git was installed
# Ensure that python v2.7 is installed and set to default
# Ensure that inkscape, xcursorgen was installed
apt-get install git python2.7 inkscape xcursorgen

# Clone repository
git clone https://github.com/kevin-leptons/venom.git
cd venom

# Create python virtual environments
./env init

# Active python virtual environments
source venv/bin/active

# Install development packages
# Only require on first time or on update dependency package
./env install
```

## Retrieve themes

```bash
# List name of all of themes
./ctl list

# Or query properties of theme
./ctl list <theme-name>
```

## Build

```bash
# Build all of themes
./ctl build

# Or build specific themes
./ctl build <theme-name-1> <theme-name-2> ...
```

## Apply/Remove theme to system

```bash
# Operation below required privilege permission

# Try build/install/active theme on system
./ctl apply <theme-name>

# Remove one theme from system
./ctl remove <theme-name>

# Or remove multi themes from system
./ctl remove <theme-name-1> <theme-name-2> ...
```

## Define more themes

Define more theme by add (key, value) to `themes` variable in file
[setting.py](../setting.py). `ThemeConfig` created by

- First argument is name of theme
- Second argument is front color, use to display text, border.
It is hex code in RGB format
- Third argument is back color, use for background
- Fourth argument is danger color, use for warning, error text

```python
themes = OrderedDict([
    ...
    ('venom-red', ThemeConfig('venom-red', '#ff0000', 'black', 'red'))
])
```

## Packaging

```bash
# Packaging debian package
./ctl dist
```

## Testing

```bash
# Clean, build, dist, test any thing
./ctl test
```

## Clean and exit

```bash
# Clean all of build files
./ctl clean

# Or clean build files of specific theme
./ctl clean <theme-name-1> <theme-name-2> ...

# Or exit virtualenv after work
deactivate
```

# External source

Venom built on few of external sources. However, source code is restructured,
and rewritten; image is converted, and some files is removed to reduce size.
List of sources below

- GTK3 theme is cloned from
[gtk-3.16/theme/HighContrast](https://github.com/GNOME/gtk/tree/gtk-3-16/gtk/theme/HighContrast)
follow [GNU Library General pubic license](https://www.gnu.org/licenses/old-licenses/lgpl-2.0.en.html)
- Icons theme is cloned from
[Flat-Remix](https://github.com/daniruiz/Flat-Remix)
follow [Createtive Commons Attribution-ShareAlike 4.0 license](https://creativecommons.org/licenses/by-sa/4.0/)
