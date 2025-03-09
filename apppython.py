def process_song_name(song_name: str) -> tuple[str, str]:
    """
    Process a song name and return the song with its description if it's a Christmas song.
    
    Args:
        song_name (str): The name of the song
        
    Returns:
        tuple[str, str]: Tuple containing (song_name, description)
    """
    description = ""
    if "Christmas" in song_name:
        description = "Desc: Popular Christmas song"
    elif "APT" in song_name:
        description = "Desc: Popular upbeat song"
    elif "birds" in song_name:
        description = "Desc: Chill love song"
    elif "Christmas" in song_name:
        description = "Desc: Popular Christmas song"
    elif "Christmas" in song_name:
        description = "Desc: Popular Christmas song"
        
    return song_name, description 