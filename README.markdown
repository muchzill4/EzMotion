EzMotion
========

Sublime Text 2 plugin inspired by Vim [EasyMotion](https://github.com/Lokaltog/vim-easymotion) plugin.
Thanks to [SublimeJump](https://github.com/tednaleid/SublimeJump) I managed to figure things out quicker.

Usage
=====

Since I'm not a big fan of plugins providing default bindings if it's not necessary, you'll have to do it yourself.

Please add following to your user keymap:

    { "keys": [<keys here>], "command": "easy_motion", "args": {"forward": true } },
    { "keys": [<keys here>], "command": "easy_motion" }

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