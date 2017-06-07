# Sublime Text Phoenix Framework Beagle

Sublime Text plugin for better Phoenix Framework experience.

**For support of v1.2 checkout branch `phoenix_v1.2`**

### Quick Start
- Clone/download plugin to your SublimeText User folder under SublimePhoenixBeagle

### Functions

  - Jump from controllers to corresponding views/templates
  - View tests from controllers
  - Jump back to controller from views
  - List Migrations

##### Configure

```
[
  { "caption": "Show More Phoenix Files", "command": "phoenix_beagle" },
  { "caption": "Phoenix Migrations List", "command": "phoenix_beagle",
    "args": { "command": "mlist"}
  }
]
```

You can override default shortcuts:

```
[
  {
    "keys": ["command+shift+k"],
    "command": "phoenix_beagle"
  },
  {
    "keys": ["command+shift+o"],
    "command": "phoenix_beagle",
    "args": { "command": "mlist"}
  }
]
```


### Showtime!
![Query](showtime/phoenix_beagle.gif?raw=true)
