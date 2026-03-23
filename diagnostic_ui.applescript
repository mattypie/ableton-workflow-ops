-- Diagnostic Script to list UI elements in Ableton Live 12 Export Window

tell application "Ableton Live 12 Suite" to activate
delay 1

tell application "System Events"
	tell process "Live"
		set exportWindow to (window 1 whose title contains "Export")
		if exportWindow exists then
			log "Export window found. Listing elements..."
			set allUIElements to UI elements of exportWindow
			repeat with elem in allUIElements
				try
					log "Class: " & (class of elem as string) & " | Name: " & (name of elem as string) & " | Description: " & (description of elem as string)
				on error
					log "Error getting element info"
				end try
			end repeat
			
			-- Look deeper into structural groups
			set allGroups to every group of exportWindow
			repeat with grp in allGroups
				log "Found Group. Listing elements inside..."
				set grpElements to UI elements of grp
				repeat with elem in grpElements
					try
						log "  - Class: " & (class of elem as string) & " | Name: " & (name of elem as string)
					on error
						log "  - Error getting group element info"
					end try
				end repeat
			end repeat
		else
			log "Export window NOT found."
		end if
	end tell
end tell
