## Terminator named tabs plugin

### About

Terminator tabs manager plugin allows to open a new tab and provide a name for it. This way you can easily locate your long running (tipically, dev) processes without having to look for them tab by tab: the user case for this plugin was in fact just that - having a number of microservices runnig locally in separate tabs and making it easier to visually identify them

### Usage

- Follow the Instal instructions and re-launch Terminator,
- In Terminator ***preferences**, under the **Plugins** tab, you should now see a **TabHelper** plugin entry: activate it by clicking on its corresponding checkbox,
- After launching Terminator again, right click within the emulator window
- If the plugin is activated, you will see a menu item (at the bottom) named **Tab Helper**,
- The **Tab Helper** submenu has an action (**named tab - new**). By clicking on it, you will be presented with a dialog box to enter the new tab name
- Enter the tab name and click "ok" - a new tab with your chosen title will be creted

### Install

Copy the python plugin file (**TabHelper.py**) to the Terminator plugins directory - wehre this is located is system dependant: on Linux it will be at 
**~/.config/terminator/plugins** - Included in this repo is a basic shell script  (**deploy_local.sh**) to copy the plugin there .

See notes on plugins for Terminator at [Read The Docs](https://terminator-gtk3.readthedocs.io/en/latest/plugins.html).

