1. Launch the Watchdog
Since you are in i3wm, you want this running in the background. Open your terminal and run:

Bash
source /srv/test.io/.venv/bin/activate
/srv/test.io/.scripts/monitor_watchdog.py &
Note: The & puts it in the background. You can verify it's alive by checking the log: tail -f /srv/test.io/.agents/logs/monitor_watchdog.log.

2. The "Handshake" Test
Let's verify the Auto-Sync loop is working. We will create a new state file and see if the manifest updates itself instantly.

Create a dummy state file:

Bash
touch /srv/test.io/.agents/state/state.test_module.yml
Check the Manifests:
Wait 2 seconds, then run:

Bash
cat /srv/test.io/.agents/manifests/manifest.state.json
If you see test_module listed in that JSON file, your Self-Healing Data Loop is officially active.

3. Initialize your Test IO Profile
Now, let's use the system for real work. You need to populate your Account State so the generators can auto-fill your bug reports with your Kalamazoo location and Debian 13 environment details.

Open the Profile State: nano /srv/test.io/.agents/state/account/profile.yml

Set the Lock: Change locked: false to locked: true. This tells the system "I'm working here, don't overwrite me."

Fill in your details:

YAML
profile:
  name: "hp_prodesk"
  location: "Kalamazoo, MI"
  os: "Debian 13 (Trixie)"
  wm: "i3wm"
  device: "HP ProDesk"
locked: true
Save and Unlock: Once done, set locked: false and save. The watchdog will instantly index your profile.

4. Create the "Status Dashboard"
To keep things high-speed, you need a way to see what's "Locked" and if the "Watchdog" is still running without digging through folders.

Would you like me to update tio-cli with a status (shorthand st) command that shows:

Watchdog Status: (Running/Dead)

Active Locks: (Which files are currently locked: true)

Environment Check: (Is the .venv active?)