# Installation and Keyboard Shortcut Setup

## 1. Install the Application

```bash
# Install dependencies first
uv pip install libsass  # or: pip install libsass

# Build and install system-wide
meson setup build --prefix=/usr/local
meson compile -C build
sudo meson install -C build
```

This installs:

- `/usr/local/bin/gtk-app-launcher` - Executable
- `/usr/local/share/gtk-app-launcher/` - App files
- `/usr/local/share/applications/com.launcher.app.desktop` - Desktop entry

## 2. Set Up Keyboard Shortcut

### For GNOME/Mutter:

```bash
# Bind to Super+Space (like macOS Spotlight)
gsettings set org.gnome.settings-daemon.plugins.media-keys custom-keybindings "['/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/']"

gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ name 'App Launcher'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ command 'gtk-app-launcher'
gsettings set org.gnome.settings-daemon.plugins.media-keys.custom-keybinding:/org/gnome/settings-daemon/plugins/media-keys/custom-keybindings/custom0/ binding '<Super>space'
```

### For Hyprland:

Add to `~/.config/hypr/hyprland.conf`:

```conf
bind = SUPER, Space, exec, gtk-app-launcher
```

### For Sway:

Add to `~/.config/sway/config`:

```conf
bindsym $mod+Space exec gtk-app-launcher
```

### For i3/bspwm/Others:

Check your compositor's keybinding documentation.

## 3. Test

Press `Super+Space` and the launcher should appear!

## 4. Uninstall

```bash
sudo ninja -C build uninstall
```
