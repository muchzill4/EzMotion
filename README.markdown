EzMotion
========

Sublime Text 2 plugin inspired by Vim [EasyMotion](https://github.com/Lokaltog/vim-easymotion) plugin.
Thanks to [SublimeJump](https://github.com/tednaleid/SublimeJump) I managed to figure things out quicker.

Usage
=====

Since I'm not a big fan of plugins providing default bindings if it's not necessary, you'll have to do it yourself.

Please add following to your user keymap:

    { "keys": [<keys here>], "command": "ez_motion", "args": {"forward": true } },
    { "keys": [<keys here>], "command": "ez_motion" }


On top of that, if you want sexy looks, you should add ezmotion scopes to your colorscheme:
It's important to set background to something similar, but not same as your actual background (for some reason, ST2 reverts colors if they are the same).

    <dict>
        <key>scope</key><string>ezmotion.bookmark</string>
        <key>settings</key>
        <dict>
            <key>foreground</key>
            <string>#ff0000</string>
            <key>background</key>
            <string>#1c1b1b</string>
        </dict>
    </dict>

    <dict>
        <key>scope</key><string>ezmotion.fade</string>
        <key>settings</key>
        <dict>
            <key>foreground</key>
            <string>#857f78</string>
            <key>background</key>
            <string>#1c1b1b</string>
        </dict>
    </dict>

Info
====

It's in alpha stage, since I have to figure out how to:
* fix *Undo Stack*
* use multiple cursors
* expand selections

And add features like:
* configuration options
* motions by lines.

Apart from that - pretty usable state.

Undo stack
==========

Please be aware, that this plugin is editing text in current view in order to render bookmarks. After that it will do an 'undo' action to make things readable again, but you will be able to 'redo' and mess things up. Be aware! Sublime dragons ahead! Use cvs! ;)