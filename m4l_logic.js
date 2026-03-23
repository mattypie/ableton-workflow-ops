// M4L Automation Logic for Ableton Auto Exporter
// This script runs inside a [js] object in a Max for Live device.

autowatch = 1;

var stateFilePath = "/Users/manas/Documents/AlphaCentuari/ableton auto exporter/automation_state.json";
var pollInterval = 1000; // 1 second
var task = new Task(pollStatus, this);

function loadbang() {
    post("M4L automation script loaded.\n");
    task.interval = pollInterval;
    task.repeat();
}

function pollStatus() {
    var state = readState();
    if (!state) return;

    if (state.status === "waiting_for_m4l") {
        updateStatus("ready");
    } else if (state.status === "start_export") {
        if (state.mode === "realtime") {
            performRealtimeExport(state);
        } else if (state.mode === "gui") {
            performGUIExport(state);
        }
    }
}

function readState() {
    var f = new File(stateFilePath, "read");
    if (!f.isopen) return null;
    var content = f.readstring(f.eof);
    f.close();
    try {
        return JSON.parse(content);
    } catch (e) {
        return null;
    }
}

function updateStatus(newStatus, extraData) {
    var state = readState() || {};
    state.status = newStatus;
    if (extraData) {
        for (var key in extraData) {
            state[key] = extraData[key];
        }
    }
    var f = new File(stateFilePath, "write");
    if (f.isopen) {
        f.writestring(JSON.stringify(state, null, 4));
        f.close();
    }
}

function performRealtimeExport(state) {
    post("Starting Real-time Export...\n");
    updateStatus("exporting");

    var api = new LiveAPI("live_set");
    var loopStart = api.get("loop_start");
    var loopLength = api.get("loop_length");

    post("Loop Start: " + loopStart + " Length: " + loopLength + "\n");

    // 1. Set playback position
    api.set("current_song_time", loopStart);

    // 2. Start Transport
    api.set("is_playing", 1);

    // 3. Monitor for end
    var endTask = new Task(function () {
        var currentTime = api.get("current_song_time");
        if (currentTime >= (loopStart + loopLength)) {
            api.set("is_playing", 0);
            updateStatus("done");
            arguments.callee.task.cancel();
        }
    }, this);
    endTask.interval = 500;
    endTask.repeat();
}

function performGUIExport(state) {
    post("Ready for GUI Export. Please trigger CMD+R manually or via script.\n");
    // GUI export is best handled by the Python launcher triggering a keypress
    // Once triggered, the M4L device doesn't have a built-in way to know when 'Render' is done
    // unless we use a timer or silence detection.
    // For now, we report 'done' after a fixed delay or wait for user.
    updateStatus("ready_for_gui");
}

function post(msg) {
    // Standard Max post to console
    this.patcher.message("script", "send", "out", msg);
}
