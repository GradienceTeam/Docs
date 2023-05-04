.. highlight:: shell

===================
🔌️ Troubleshooting
===================

Here are described most common issues with Gradience and guides how to fix them

Gradience doesn't start
-----------------------

There are number of reasons for this, they include the following:


* There are error in `gtk.css`
* There are issue with current build
* There are issue with the package

To get more info on why this happens launch Gradience from terminal:


* For Flatpak: `flatpak run com.github.GradienceTeam.Gradience`
* For System package: `GTK_DEBUG=all gradience`

If there are no logs, try updating Gradience or reinstalling it, if you are using system package try using Flatpak version instead

If the logs mention `gtk.css`\ , you can try removing both `~/.config/gtk-3.0/gtk.css` and `~/.config/gtk-4.0/gtk.css` using this command:

`rm -rf .config/gtk-4.0 .config/gtk-3.0`

Theme are reset after reboot or on next login
---------------------------------------------

This issue is very common, it is caused either by **\ *Custom Accent Colors*\ ** or **\ *Material You Color Theming*\ ** extensions, this happens because they override the `gtk.css` theming file with their own, to solve that simply disable those extensions and re-apply the preset

Gradience looks broken
----------------------

This can be caused by a lot of factors, some of them include:


* There are theme applied that are not compatible with Libadwaita
* There are set hardcoded theme in environment or in Flatpak override
* Your distribution are shipping custom theme out-of-the-box

To fix it try the following:

Set system theme to default **\ *Adwaita*\ ** using:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


* GNOME Tweaks
* This command: `gsettings set org.gnome.desktop.interface gtk-theme 'Adwaita'`

Check the `settings.ini` files and remove lines that contain `gtk-theme`
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`cat ~/.config/gtk-3.0/settings.ini`
`cat ~/.config/gtk-4.0/settings.ini`

Check if there are theme override in environment:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`cat ~/.bash_profile`
`cat ~/.bashrc`

Remove `GTK_THEME=<THEME_NAME>` if present
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check if there are theme overrides for Flatpak:


* User: `cat ~/.local/share/flatpak/overrides/global`
* System: `cat /var/lib/flatpak/overrides/global`

If the file are something like this:

.. code-block::

   [Context]
   filesystems=/home/JohnDoe/.themes;/home/JohnDoe/.icons;/home/JohnDoe/.local/share/themes;/home/JohnDoe/.local/share/icons;

   [Environment]
   GTK_THEME=<THEME_NAME>

Then remove the `GTK_THEME=<THEME_NAME>`, in some cases adding `unset-environment=GTK_THEME;` to `[Context]` is required

My issue are not described here, what I can do?
-----------------------------------------------

You can ask for help in our `Matrix <https://matrix.to/#/#Gradience:matrix.org>`_ or `Discord <https://discord.com/invite/4njFDtfGEZ>`_ rooms, we will try our best to help you
