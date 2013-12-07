Sublime Text 3 plugin for 'goimports'
========================

This is a plugin for Sublime Text 3 that will use [goimports](http://github.com/bradfitz/goimports "goimports repository") to tidy/clean/add/remove package imports in your
Go (golang) source code based on what you have used in it.

- ***Makes sure you read the [goimports](http://github.com/bradfitz/goimports "goimports repository") notes and understand its limitations.*** Consider this as a disclaimer as well. This plugin ***___modifies your code___*** upon saving and any bug in [goimports](http://github.com/bradfitz/goimports "goimports repository") is likely to affect your precious code!

Installation
-

In the terminal of your choice, change the current path to Sublime Text 3's package folder, and then clone this repository as `GoImports`.

On OSX, this will be:
```bash

$ cd ~/Library/Application Support/Sublime Text 3/Packages/
$ git clote https://github.com/spamwax/goimports-sublime-text-3.git GoImports
```

If you haven't already installed [goimports](http://github.com/bradfitz/goimports "goimports repository") package, do so by issuing this:

`$ go get github.com/bradfitz/goimports`

This will add a `goimports` binary file to your GOPATH's bin folder.
You need to find the path to that binary for the next step.

Settings
-
Open plugin's setting file in Sublime Text 3 by navigating to `Preferences > Package Settings > GoImports > Settings - User`

Set the `goimports_bin` to the path of `goimports` on your machine (see above.)

You can disable the plugin by setting the value of `goimports_enabled` to `false`

The other settings are self-explanatory and have a brief comment line as well.

Usage
-
On every save, the plugin will pass the content of the current Go (golang) file to `goimports` and
replace it with the output that it provides ***iff*** there were no errors encountered.

You can do the same thing by pressing the 'F4' key or choosing the menu item `Run GoImports`
from `Tools > GoImports` menu in Sublime Text 3.

Limitations/Issues
-
Since this plugin uses [goimports](http://github.com/bradfitz/goimports "goimports repository"), it will be inherently limited to that tool's issues.
One main issue I encountered was when the 3-rd party package name did not match its folder name.

In this case [goimports](http://github.com/bradfitz/goimports "goimports repository") removes the package import. To fix this, import the packages like so (named package)

```go
import(
Alfred "bitbucket.org/listboss/go-alfred"
)
```

TODO
-
- Automatically parse GOPATH's 'bin' folders to find the `goimports` binary.
If not found try to install it. Finally Alert the user about how to install and
set the settings.

