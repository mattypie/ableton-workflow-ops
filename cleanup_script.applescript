-- Safe Cleanup Script for Ableton Live 12
-- This script clears blocking dialogs like "Save changes" and "Stop audio".

log "Activating Ableton Live 12 Suite for cleanup..."
tell application "Ableton Live 12 Suite" to activate
delay 1

tell application "System Events"
	tell process "Live"
		-- Check for "Save changes" (Command+D for "Don't Save")
		-- Using 'every window' to avoid index errors if no windows exist
		set saveWindows to (every window whose title contains "Save")
		if (count of saveWindows) > 0 then
			log "Found Save dialog. Sending Command+D."
			keystroke "d" using {command down}
			delay 1
		end if

		-- Check for "This action will stop audio" (Enter for "OK")
		set alertWindows to (every window whose title contains "Live" or description contains "stop audio")
		if (count of alertWindows) > 0 then
			log "Found Stop Audio dialog. Sending Enter."
			keystroke return
			delay 1
		end if
		
		-- Final generic check for any small alert windows
		if exists window 1 then
			if (title of window 1 is "") or (title of window 1 contains "Live") then
				log "Found potential alert window. Sending Enter."
				keystroke return
				delay 0.5
			end if
		end if
	end tell
end tell
