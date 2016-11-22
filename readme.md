# venom

This is very simple themes for gtk-3. It base on two main color. And all of
icons sync by main color. Package provide three theme color for review. Target platform is `GNOME 3.14`

## Green on Black

![venom-green](asset/venom-green.png)

## Teal on Black

![venom-green](asset/venom-teal.png)

## Orange on Black

![venom-green](asset/venom-orange.png)

# Usage

- It will be coming soon with Debian package
- Now, people can try to use by follow contribution instructions

# Contribution

## Enter virtual environment

```bash
# Ensure that git is installed
# Ensure that python v2.7 is installed and set to default

# Clone repository
git clone https://github.com/kevin-leptons/venom.git
cd venom

# Create python virtual environments
./setup.py init

# Active python virtual environments
. venv/bin/active

# Install development packages
./setup.py dev
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

Define more theme by add (key, value) to `themes` variable in file [setting.py](setting.py)

```python
themes = OrderedDict([
    ...
    ('venom-red', ThemeConfig('venom-red', '#0000ff', 'black', 'red'))
])
```

## Clean build files

```bash
# Clean all of build files
./ctl clean

# Clean build files of specific theme
./ctl clean <theme-name-1> <theme-name-2> ...
```
