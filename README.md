# Tracklist Restriction Checker

## Introduction
This program is designed to assist in checking tracklists for Mixcloud shows to ensure they comply with certain restrictions. It helps identify instances where the number of tracks by an artist, consecutive tracks by an artist, or tracks from the same album exceed specified limits.

## Accessing the Program
The executable file can be found in under the dist folder. Download the respective file depending on your operating system.

### Mac Users
You may encounter an error message when attempting to open the file. Refer to the instructions on bypassing this block [here](https://support.apple.com/en-gb/102445#:~:text=If%20you%20want%20to%20open%20an%20app%20that%20hasn%E2%80%99t%20been%20notarised%20or%20is%20from%20an%20unidentified%20developer).

## How It Works
To use the program:
1. Copy the tracklist from the Admin tool's Track Info, ensuring to start from "Start" and end with the album of the last row.
2. Click the button labeled "↵". This button clears the "Enter tracklist here" text entry field, pastes the copied text into the field, and processes it as the new tracklist for checking.

### Features
- **Clean up tracklist**: Removes track repetitions, converts seconds into hh:mm:ss format, and realigns the columns for easier readability.
- **Reason for restriction**: Specifies the reasons for any restrictions detected in the tracklist and lists the tracks contributing to each limit exceeded.
- **Macro info**: Provides information in a format ready to be copied and pasted into a reply to the user, detailing the restrictions detected in the tracklist.
- **Copy**: Allows you to copy the resulting text from "Macro info" for quick use in replies to users.

## Issues
For any issues encountered while using the program, please email mdfrolikova@gmail.com. Include steps to reproduce the issue and screenshots of any error messages if applicable.

## Sample Tracklist

```
Start   End   Artists         Track Title                   Id      Albums
0       30    Mack Fields     Bowling Ball Blues           3530145 Cults Hits Novelty Classics, Vol. 1
30      60    Mack Fields     Bowling Ball Blues           3530145 Cults Hits Novelty Classics, Vol. 1
60      90    Mack Fields     Bowling Ball Blues           3530145 Cults Hits Novelty Classics, Vol. 1
90      120   Mack Fields     Bowling Ball Blues           3530145 Cults Hits Novelty Classics, Vol. 1
120     150   Hank Locklin    I'm Tired Of Bummin Around   4838751 Queen Of Hearts
150     180   Hank Locklin    I'm Tired Of Bummin Around   4838751 Queen Of Hearts
180     210   Hank Locklin    I'm Tired Of Bummin Around   4838751 Queen Of Hearts
210     240   Hank Locklin    I'm Tired Of Bummin Around   4838751 Queen Of Hearts
240     270   Hank Locklin    I'm Tired Of Bummin Around   4838751 Queen Of Hearts
390     420   Hank Thompson   Hangover Tavern               2964975 A Six Pack To Go
420     450   Hank Thompson   Hangover Tavern               2964975 A Six Pack To Go
450     480   Hank Thompson   Hangover Tavern               2964975 A Six Pack To Go
480     510   Hank Thompson   Hangover Tavern               2964975 A Six Pack To Go
510     540   Hank Thompson   Hangover Tavern               2964975 A Six Pack To Go
540     570   Hank Thompson   Hangover Tavern               2964975 A Six Pack To Go
```
