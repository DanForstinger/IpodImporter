1. Make sure pipx is set up

Check if you have pipx:

pipx --version


If not installed:

python3 -m pip install --user pipx
python3 -m pipx ensurepath


Then restart your terminal.

📦 2. Install the dependency (mutagen) using pipx

Because pipx creates a small, isolated virtual environment for a tool or script, you can install mutagen globally for your user like this:

pipx install mutagen


Or, if you prefer to just run the script inside a temporary pipx environment without installing anything globally:

pipx runpip python mutagen install mutagen


However, since this script isn’t a published package, the simpler approach is to run it in an ephemeral pipx environment with the dependencies installed inline:

🚀 3. Run the extractor script with pipx

If you saved the script as extract_ipod_music.py, you can do this in one line:

pipx run --spec mutagen python3 extract_ipod_music.py "/Volumes/Dans iPod"


That tells pipx:

“Run this Python script”

“Use a temporary environment that includes the mutagen package”

“Then clean up afterward”

🧠 Quick Summary
Action	Command
Verify pipx	pipx --version
Install pipx	python3 -m pip install --user pipx
Install mutagen permanently	pipx install mutagen
Run the script (one-liner)	pipx run --spec mutagen python3 extract_ipod_music.py "/Volumes/Dans iPod"

✅ That’s the cleanest way to use pipx: it keeps your system Python clean, uses mutagen only for this task, and runs your script in isolation.


## Playlist Extraction

You can also extract playlists. Use the script extract_ipod_playlists.py. 

Here's how to setup your environment:

🧩 Step 1: Install dependencies

Run:

pipx runpip python pyItunes install pyItunes mutagen

🚀 Step 2: Run the script

Example:

pipx run --spec "pyItunes mutagen" python3 extract_ipod_playlists.py "/Volumes/Dans iPod"