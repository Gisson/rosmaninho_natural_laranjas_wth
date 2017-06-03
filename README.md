# Rosmaninho Natural e Laranjas
## Repo for the WhatTheHack 2017 Challenge

### "When I’m frustrated because I can’t show off my techie skills to cool companies on LinkedIn. How about GitHub?"

At the moment the main constraint we have is the network speed, so you can find this project  running on a *decent* (Gigabit) connection [over here](http://pikachu.rnl.tecnico.ulisboa.pt:31000) - http://pikachu.rnl.tecnico.ulisboa.pt:31000/.


## Installing and Running
### Python 3 is a MUST!

```bash
# Install Tornado and PyGithub
pip3 install -r requirements.txt

# You should now have a GitHub personal access tokens so you can export it
# https://github.com/settings/tokens
export GITHUB_API_TOKEN=*YOUR-TOKEN-HERE*

# Run the Web server (default port is 8888 - constant in src/server.py)
./run.sh
```

## The Challenge
It took us quite some time to pick one of the challenges, but in the end this one was it. It was both interesting and challenging - hah. We implemented a solution in python that basically ranks GitHub profiles based on their repositories - a user can filter profiles based on different technologies/languages and then apply some filters on top of it, defining a *score* for each filter. The profile is then ranked using these criteria and that is whats shown to the user.
