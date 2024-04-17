from tabulate import tabulate
import textwrap

def load_tracklist(tracklist_data):
    """
    Process the tracklist data and return a list of dictionaries representing rows of data.
    """
    # Split the data into rows
    rows = tracklist_data.strip().split('\n')
    # Split each row into columns based on tabs
    rows = [row.split('\t') for row in rows]
    # Extract the headers
    headers = rows[0]
    # Create dictionaries for each row
    dict_rows = [create_dict(row, headers) for row in rows[1:]]
    return dict_rows

def create_dict(row, headers):
    """
    Create a dictionary for a row using the provided headers.
    """
    return {header: value.strip() for header, value in zip(headers, row)}

def merge_consecutive_rows(rows):
    """
    Merge consecutive rows with the same values for specified keys.
    """
    merged_rows = []
    i = 0
    while i < len(rows):
        current_row = rows[i].copy()
        start = int(current_row.get('Start', 0))
        end = int(current_row.get('End', 0))
        # Find consecutive rows with the same values for specified keys
        while i + 1 < len(rows) and \
              all(rows[i + 1].get(key) == current_row.get(key) for key in ['Artists', 'Track', 'Id', 'Albums']):
            end = int(rows[i + 1].get('End', 0))
            i += 1
        current_row['Start'] = str(start)
        current_row['End'] = str(end)
        merged_rows.append(current_row)
        i += 1
    return merged_rows

# Define the seconds_to_time function
def seconds_to_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return "{:02}:{:02}:{:02}".format(hours, minutes, seconds)

def format_tracklist(merged_rows):
    """
    Format the tracklist for display.
    """
    headers = merged_rows[0].keys()
    for row_dict in merged_rows:
        row_dict['Start'] = seconds_to_time(int(row_dict['Start']))
        row_dict['End'] = seconds_to_time(int(row_dict['End']))
        # Wrap the text for long cells
        for key in ['Artists', 'Track Title', 'Albums']:
            row_dict[key] = '\n'.join(textwrap.wrap(row_dict[key], width=20))

    table_data = [[row[key] for key in headers] for row in merged_rows]

    return tabulate(table_data, headers=headers, tablefmt="fancy_grid", colalign=("left",), disable_numparse=True)

def get_track_counts(rows):
    """
    Calculate track counts for each artist and album.
    """
    artist_tracks = {}
    album_tracks = {}
    for row_dict in rows:
        artist = row_dict['Artists']
        title = row_dict['Track Title']
        if artist in artist_tracks:
            artist_tracks[artist].append(title)
        else:
            artist_tracks[artist] = [title]
        album = row_dict['Albums']
        if album in album_tracks:
            album_tracks[album].append(title)
        else:
            album_tracks[album] = [title]
    return artist_tracks, album_tracks

def get_exceeding_artists(artist_tracks):
    """
    Identify artists with 5 or more tracks.
    """
    exceeding_artists = {}
    for artist, tracks in artist_tracks.items():
        if len(tracks) >= 5:
            exceeding_artists[artist] = {'count': len(tracks), 'tracks': tracks}
    return exceeding_artists

def get_exceeding_albums(album_tracks):
    """
    Identify albums with 4 or more tracks.
    """
    exceeding_albums = {}
    for album, tracks in album_tracks.items():
        if len(tracks) >= 4:
            exceeding_albums[album] = {'count': len(tracks), 'tracks': tracks}
    return exceeding_albums

def get_consecutive_artist_tracks(merged_rows):
    """
    Identify consecutive tracks by the same artist.
    """
    consecutive_artist_tracks = {}
    current_artist = None
    current_count = 0
    current_tracks = []

    for row in merged_rows:
        artist = row['Artists']
        track = row['Track Title']

        if artist == current_artist:
            current_count += 1
            current_tracks.append(track)
        else:
            if current_artist is not None and current_count > 3:
                consecutive_artist_tracks[current_artist] = {'count': current_count, 'tracks': current_tracks}

            current_artist = artist
            current_count = 1
            current_tracks = [track]

    if current_artist is not None and current_count > 3:
        consecutive_artist_tracks[current_artist] = {'count': current_count, 'tracks': current_tracks}

    return consecutive_artist_tracks

def get_consecutive_album_tracks(merged_rows):
    """
    Identify consecutive tracks from the same album.
    """
    consecutive_album_tracks = {}
    current_album = None
    current_count = 0
    current_tracks = []
    
    for row in merged_rows:
        album = row['Albums']
        track = row['Track Title']
        
        if album == current_album:
            current_count += 1
            current_tracks.append(track)
        else:
            if current_album is not None and current_count > 2:
                consecutive_album_tracks[current_album] = {'count': current_count, 'tracks': current_tracks}
                
            current_album = album
            current_count = 1
            current_tracks = [track]
    
    # Add the last consecutive tracks after the loop
    if current_album is not None and current_count > 2:
        consecutive_album_tracks[current_album] = {'count': current_count, 'tracks': current_tracks}
    
    return consecutive_album_tracks

def check_all_for_repeated_tracks(consecutive_album_tracks, consecutive_artist_tracks, exceeding_artists, exceeding_albums):
    all_repeated_tracks = {}
    
    for tracks_dict in [consecutive_album_tracks, consecutive_artist_tracks, exceeding_artists, exceeding_albums]:
        for key, value in tracks_dict.items():
            tracks = value['tracks']
            repeated = []
            seen = set()
            for track in tracks:
                if track in seen:
                    repeated.append(track)
                else:
                    seen.add(track)
            if repeated:
                all_repeated_tracks.setdefault(key, []).extend(repeated)
    
    return all_repeated_tracks

def format_reason_for_restriction(exceeding_artists, exceeding_albums, consecutive_artist_tracks, consecutive_album_tracks):
    """
    Format the reasons for restriction for display.
    """
    result_text = ""
    if exceeding_artists:
        result_text += "Max Tracks By Artist:\n"
        for artist, data in exceeding_artists.items():
            result_text += f"{artist}: {data['count']} tracks\n"
            for track in data['tracks']:
                result_text += f"\t- {track}\n"
        result_text += f"\n"

    if consecutive_artist_tracks:
        result_text += "Max Consecutive Tracks By Artist:\n"
        for artist, data in consecutive_artist_tracks.items():
            result_text += f"{artist}: {data['count']} tracks\n"
            for track in data['tracks']:
                result_text += f"\t- {track}\n"
        result_text += f"\n"

    if exceeding_albums:
        result_text += "Max Tracks From Album:\n"
        for album, data in exceeding_albums.items():
            result_text += f"{album}: {data['count']} tracks\n"
            for track in data['tracks']:
                result_text += f"\t- {track}\n"
        result_text += f"\n"

    if consecutive_album_tracks:
        result_text += "Max Consecutive Tracks From Album:\n"
        for album, data in consecutive_album_tracks.items():
            result_text += f"{album}: {data['count']} tracks\n"
            for track in data['tracks']:
                result_text += f"\t- {track}\n"
        result_text += f"\n"

    return result_text

def format_macro_info(exceeding_artists, consecutive_artist_tracks, exceeding_albums, consecutive_album_tracks):
    """
    Format macro info for display.
    """
    macro_info = f"Our audio fingerprinter has detected that this show contains:\n\n"
    if exceeding_artists:
        for artist, data in exceeding_artists.items():
            macro_info += f"\t\t- {data['count']} tracks by {artist}:\n"
            for track in data['tracks']:
                macro_info += f"\t\t\t\t- {track}\n"
        macro_info += f"\t\tThis exceeds the limit set for the number of total tracks by one recording artist.\n\n"
    if consecutive_artist_tracks:
        for artist, data in consecutive_artist_tracks.items():
            macro_info += f"\t\t - {data['count']} consecutive tracks by {artist}:\n"
            for track in data['tracks']:
                macro_info += f"\t\t\t\t- {track}\n"
        macro_info += f"\t\tThis exceeds the limit set for the number of consecutive tracks by one recording artist.\n\n"
    if exceeding_albums:
        for album, data in exceeding_albums.items():
            macro_info += f"\t\t- {data['count']} tracks from the album \"{album}\":\n"
            for track in data['tracks']:
                macro_info += f"\t\t\t\t- {track}\n"
        macro_info += f"\t\tThis exceeds the limit set for the number of total tracks from the same album.\n\n"
    if consecutive_album_tracks:
        for album, data in consecutive_album_tracks.items():
            macro_info += f"\t\t- {data['count']} consecutive tracks from the album \"{album}\":\n"
            for track in data['tracks']:
                macro_info += f"\t\t\t\t- {track}\n"
        macro_info += f"\t\tThis exceeds the limit set for the number of consecutive tracks from the same album.\n\n"
    return macro_info
