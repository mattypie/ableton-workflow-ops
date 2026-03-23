-- Hyper-Granular AppleScript for Ableton Live 12 Export
-- Arguments: LoopStart (Bar.Beat.Tick), LoopLength (Bar.Beat.Tick), OutputPath

on run argv
	set loopStartStr to item 1 of argv
	set loopLengthStr to item 2 of argv
	set outputPath to item 3 of argv
	
	-- Function to split strings like "33.1.1"
	set AppleScript's text item delimiters to "."
	set startParts to text items of loopStartStr
	set lengthParts to text items of loopLengthStr
	set AppleScript's text item delimiters to ""
	
	log "Activating Ableton Live 12 Suite..."
	tell application "Ableton Live 12 Suite" to activate
	delay 1
	
	tell application "System Events"
		tell process "Live"
			
			-- Handle blocking dialogs
			set saveWindows to (every window whose title contains "Save")
			if (count of saveWindows) > 0 then
				log "Found Save dialog. Sending Command+D."
				keystroke "d" using {command down}
				delay 1
			end if
			
			set alertWindows to (every window whose title contains "Live" or description contains "stop audio")
			if (count of alertWindows) > 0 then
				log "Found Stop Audio alert. Sending Enter."
				keystroke return
				delay 1
			end if

			-- 1. Trigger Export Dialog (CMD+SHIFT+R)
			log "Triggering Export Dialog (CMD+SHIFT+R)..."
			keystroke "r" using {command down, shift down}
			
			set exportWindowExists to false
			repeat 10 times
				set exportWindows to (every window whose title contains "Export")
				if (count of exportWindows) > 0 then
					set exportWindowExists to true
					exit repeat
				end if
				delay 0.5
			end repeat
			
			if not exportWindowExists then
				error "CRITICAL: Export dialog did not appear."
			end if
			
			log "Export dialog found. Navigating to Render Start (3 Tabs)..."
			delay 1
			
			-- 2. Navigate to Render Start Bar (Tab 1: Cancel, Tab 2: Rendered Track, Tab 3: Render Start Bar)
			keystroke tab -- Tab 1
			delay 0.3
			keystroke tab -- Tab 2
			delay 0.3
			keystroke tab -- Tab 3 (Start Bar)
			delay 0.3
			
			-- Enter Start Bar
			keystroke item 1 of startParts
			log "Entered Start Bar: " & item 1 of startParts
			delay 0.3
			
			-- Enter Start Beat
			keystroke tab -- Tab 4
			delay 0.2
			keystroke item 2 of startParts
			log "Entered Start Beat: " & item 2 of startParts
			delay 0.3
			
			-- Enter Start Tick
			keystroke tab -- Tab 5
			delay 0.2
			keystroke item 3 of startParts
			log "Entered Start Tick: " & item 3 of startParts
			delay 0.3
			
			-- Confirm Render Start
			keystroke return -- Confirm
			delay 0.5
			
			-- 3. Navigate to Render Length Bar
			keystroke tab -- Tab 6 (Length Bar)
			delay 0.3
			
			-- Enter Length Bar
			keystroke item 1 of lengthParts
			log "Entered Length Bar: " & item 1 of lengthParts
			delay 0.3
			
			-- Enter Length Beat
			keystroke tab -- Tab 7
			delay 0.2
			keystroke item 2 of lengthParts
			log "Entered Length Beat: " & item 2 of lengthParts
			delay 0.3
			
			-- Enter Length Tick
			keystroke tab -- Tab 8
			delay 0.3
			keystroke item 3 of lengthParts
			log "Entered Length Tick: " & item 3 of lengthParts
			delay 0.3
			
			-- Confirm Render Length
			keystroke return -- Confirm
			delay 0.5
			
			-- 4. Navigate back to Export Button
			-- User says 15th tab is Export. We are at Tab 8.
			-- So 15 - 8 = 7 more tabs.
			log "Tabbing to Export button (7 more tabs)..."
			repeat 7 times
				keystroke tab
				delay 0.2
			end repeat
			delay 0.5
			
			log "Triggering Export (Return)..."
			keystroke return
			delay 2
			
			-- 5. Handle macOS Save Dialog
			log "Waiting for Save dialog..."
			set saveWindowExists to false
			repeat 15 times
				set pWindows to every window
				repeat with w in pWindows
					if (title of w contains "Save") or (name of w contains "Save") or (title of w contains "Export") then
						set saveWindowExists to true
						exit repeat
					end if
				end repeat
				if saveWindowExists then exit repeat
				delay 1
			end repeat
			
			log "Opening Go To Folder (CMD+SHIFT+G)..."
			keystroke "g" using {command down, shift down}
			delay 1.5
			
			keystroke outputPath
			delay 0.5
			keystroke return -- Confirm Path
			log "Path confirmed: " & outputPath
			delay 1
			keystroke return -- Final Confirm Save
			log "Save confirmed."
			
			delay 3
		end tell
	end tell
end run
