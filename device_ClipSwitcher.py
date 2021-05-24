# name=ClipSwitcher

import midi	# The script will use MIDI functions.

# This array contains list of FL Studio performance mode clip numbers.
# From 0 to 11 - up to 12 clips placed on FL Studio track 1.
# From 12 to 23 - up to 12 clips placed on track 2 and so on.
# At the same time each array item value is MIDI note data1 value used by FL Studio to fire appropriate clip:
# 0 is C0 - fires the track1.clip 0 when you hit CO on midi keyboard, 1 is C#0 turns off track1.clip0 and fires
# track1.clip1 and so on.
# This works for clips located in the same track
# For my exapmple I used 8 clips on track 1. It is possible to use many clips located on many different tracks.
# But if you what each single pedal press to turn on next clip and turn off current clip, this will work only if your
# current and next clips both located on the same track. If you current and next clips are located on different tracks
# sending one midi message to turn on next clip will only turn on next clip and current clip will not be turned off.
# Unfortunately I did not find the way allowing to generate additional midi message to command current clip to mute
# when next clip is on another track

# Edit contents of this array correponding to your clips-track distribution.
# For example if you want to play loop: track1.clip2 -> track1.clip4-> track1.clip5 -> track1.clip1 the array will
# look like: clipSequence = [1, 3, 4]
# Another example for the case when you set up 5 clips on track1 and 3 clips on track2:
# clipSequence = [0, 1, 2, 3, 4, 12, 13, 14]
# As mentioned above it will work, but when you press pedal 6th time, track1.clip5 will not mute


clipSequence = [0, 1, 2, 3, 4, 5, 6, 7]

class TPlayer():
	"""Handles OnMidiMsg(). Verifies it is the CC sustain pedal on message. Replaces incoming CC mesage with Note On
	message and leaves its further handling to FL Studio. FL Studio recieves Note On message and plays corresponding
	clip according to it. The currentClip classs member stores currently running clip."""

	def __init__(self):
		self.currentClip = -1 # Init with -1

	def OnMidiMsg(self, event):
		event.handled = False

		# Check the message is MIDICC type (176) and is sustain pedal (64) on (127) message
		if event.midiId == midi.MIDI_CONTROLCHANGE and event.data1 == 64 and event.data2 == 127:
			self.IterateToNextClipNumber()  # increment to next sequence number to fire next clip
			event.midiId = midi.MIDI_NOTEON  # replace with MIDI note On message (144)
			event.data1 = clipSequence[self.currentClip]  # C0 note
			event.data2 = 100  # note velocity (seems does not matter)
			print(event.midiId, event.data1, event.data2)

	def IterateToNextClipNumber(self):
		if self.currentClip < len(clipSequence) - 1:
			self.currentClip += 1
		else:
			self.currentClip = 0

player = TPlayer()	#Create the instance of class

def OnMidiMsg(event):
	player.OnMidiMsg(event) #handle OnMidiMsg
