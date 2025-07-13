console.log("run")
let v = document.getElementsByTagName("video")[0];

if (!v)
	return {}

let output = {};

if (v.paused) v.play();

output.network_status = v.networkState;
output.resolution_w = v.videoWidth;
output.resolution_h = v.videoHeight;
output.player_size_w = parseInt(getComputedStyle(v).width.replace("px",""));
output.player_size_h = parseInt(getComputedStyle(v).height.replace("px",""))
output.remaining_buffer = -1;
output.n_buffers = v.buffered.length;
output.paused = v.paused;
output.percent = v.currentTime / v.duration;
output.current_time = v.currentTime;
output.video_url = location.href;

for (var i=0;i<v.buffered.length;i++) {
	if (v.currentTime > v.buffered.start(i) && v.currentTime < v.buffered.end(i)) {
		output.remaining_buffer = v.buffered.end(i) - v.currentTime;
		break;
	}
}

let qual = v.getVideoPlaybackQuality()
output.dropped_frames = qual.droppedVideoFrames;
output.total_frames = qual.totalVideoFrames;
output.corrupted_frames = qual.corruptedVideoFrames;

return output;
