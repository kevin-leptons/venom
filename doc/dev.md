# Contributions

## Enter virtual environment

```bash
# Ensure that git is installed
# Ensure that python v2.7 is installed and set to default

# Clone repository
git clone https://github.com/kevin-leptons/venom.git
cd venom

# Create python virtual environments
./dev init

# Active python virtual environments
source venv/bin/active

# Install development packages
# Only require on first time or on update dependency package
./dev install

# Or exit virtual after do not work any more
deactivate
```

## Retrieve themes

```bash
# List name of all of themes
./ctl list

# Or query properties of theme
./ctl list <theme-name>
```

## Build

**Warning**: Convert icons required more time

```bash
# Build all of themes
./ctl build

# Or build specific themes
./ctl build <theme-name-1> <theme-name-2> ...
```

## Apply/Remove theme

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
[setting.py](../setting.py). ThemeConfig created by

- First argument is name of theme
- Second argument is front color, use to display text, border.
It is hex code in RGB format
- Third argument is back color, use for background
- Fourth argument is danger color, use for warning, error text

```python
themes = OrderedDict([
    ...
    ('venom-red', ThemeConfig('venom-red', '#0000ff', 'black', 'red'))
])
```

## Packaging

```bash
# Packaging debian package
./ctl dist
```

## Clean build files

```bash
# Clean all of build files
./ctl clean

# Clean build files of specific theme
./ctl clean <theme-name-1> <theme-name-2> ...
```
