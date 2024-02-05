### This was originally a pet project that was used to learn a bit more about Python. It is no longer maintaned and is used more or less for reference.

The various if statements could honestly be an if/else. In the case of new python -- a case statement probably. Again this is a very old bot. It's no longer maintained. I loved what it did, though its time has passed. Another of its kind will likely be created in the future.

The concept of this bot made use of a database to store usernames with a count that would increment when a trigger word was said. This was then stored in a database called `leaderboard.db`.

The `settings.ini` file of this bot contained the Discord API token in an attempt to keep it out of the bot itself -- for distribution specifically. This file also contained a flag for whether or not the bot could join a Discord Voice Channel -- only to be toggled by an admin.

```
[options]
joinvc = True
```
