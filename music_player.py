import tkinter as tk
from tkinter import filedialog, messagebox
import os
from pygame import mixer

class MusicPlayer:
    """
    A simple music player application with a colorful GUI,
    built with Tkinter and Pygame's mixer module.
    """
    def __init__(self, master):
        self.master = master
        self.master.title("RhythmFlow - Green Glow") # Updated title for the new theme
        self.master.geometry("650x650") # Slightly wider and taller for better layout
        self.master.resizable(False, False) # Keep the window fixed
        self.master.configure(bg="#0A1A0A") # Very dark forest green for main background

        # Initialize Pygame mixer for audio playback
        mixer.init()

        # --- Application State Variables ---
        self.playlist = [] # Stores full paths of songs
        self.current_song_index = -1 # Index of the currently playing song
        self.is_paused = False # Flag to track if music is paused

        # --- GUI Elements --- 

        # Top Frame for "Now Playing" section (simulating album art and song info)
        now_playing_frame = tk.Frame(self.master, bg="#1A2A1A", bd=0, relief=tk.FLAT) # Slightly lighter dark green
        now_playing_frame.pack(pady=(30, 20), padx=30, fill=tk.X)

        # Placeholder for Album Art (simple colored square)
        self.album_art_placeholder = tk.Label(now_playing_frame, text="🎵",
                                              font=("Helvetica", 60), bg="#2A3A2A", fg="#B3B3B3", # Font changed here
                                              width=5, height=2, relief=tk.FLAT, bd=0)
        self.album_art_placeholder.pack(side=tk.LEFT, padx=(0, 20))

        # Song Info Frame
        song_info_frame = tk.Frame(now_playing_frame, bg="#1A2A1A") # Matches now_playing_frame
        song_info_frame.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Song Title Label
        self.song_title_label = tk.Label(song_info_frame, text="No song loaded",
                                         font=("Helvetica", 22, "bold"), fg="#FFFFFF", bg="#1A2A1A", # Font changed here
                                         wraplength=350, anchor="w", justify="left")
        self.song_title_label.pack(pady=(0, 5), fill=tk.X)

        # Artist/Album Label (placeholder for now)
        self.artist_album_label = tk.Label(song_info_frame, text="Add songs to start listening!",
                                           font=("Helvetica", 14), fg="#E0E0E0", bg="#1A2A1A", # Font changed here
                                           wraplength=350, anchor="w", justify="left")
        self.artist_album_label.pack(fill=tk.X)

        # Frame for the Playlist (Listbox) - Cleaned up design
        playlist_frame = tk.Frame(self.master, bg="#0A1A0A", bd=0, relief=tk.FLAT) # Matches main window background
        playlist_frame.pack(pady=(0, 20), padx=30, fill=tk.BOTH, expand=True)

        # Scrollbar for the playlist
        scrollbar = tk.Scrollbar(playlist_frame, troughcolor="#2A3A2A", bg="#4CAF50", width=12) # Vibrant Green scrollbar
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Listbox to display the songs in the playlist
        self.playlist_listbox = tk.Listbox(playlist_frame, bg="#1A2A1A", fg="#FFFFFF", # Dark green background, white text
                                           selectbackground="#66BB6A", selectforeground="#0A1A0A", # Brighter green selection
                                           font=("Helvetica", 13), bd=0, relief=tk.FLAT, # Font changed here
                                           height=10, selectmode=tk.SINGLE,
                                           yscrollcommand=scrollbar.set,
                                           highlightthickness=0) # Remove default focus border
        self.playlist_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.playlist_listbox.yview)

        # Bind the listbox selection event to play the selected song
        self.playlist_listbox.bind("<<ListboxSelect>>", self.on_song_select)

        # --- Playback Control Panel (New Section) ---
        # This frame will contain all playback controls and volume
        playback_panel_frame = tk.Frame(self.master, bg="#1A2A1A", bd=0, relief=tk.FLAT) # Matches now playing frame
        playback_panel_frame.pack(pady=(10, 20), padx=30, fill=tk.X)

        # Frame for control buttons (centered within playback_panel_frame)
        control_buttons_frame = tk.Frame(playback_panel_frame, bg="#1A2A1A", bd=0, relief=tk.FLAT)
        control_buttons_frame.pack(pady=(10, 5)) # Padding top and bottom

        # Configure columns to expand equally to center the buttons
        for i in range(5):
            control_buttons_frame.grid_columnconfigure(i, weight=1)

        # Button styling with emojis for icons (Spotify-like flat design)
        button_style = {
            "font": ("Helvetica", 18), # Font changed here
            "bg": "#1A2A1A", # Transparent background relative to its parent frame
            "fg": "#E0E0E0", # Lighter grey for icons
            "activebackground": "#1A2A1A", # Transparent on click
            "activeforeground": "#FFFFFF", # White text on click
            "relief": tk.FLAT,
            "bd": 0,
            "padx": 10,
            "pady": 5,
            "width": 3 # Smaller width for icon buttons
        }

        # Create control buttons with emoji icons
        self.prev_button = tk.Button(control_buttons_frame, text="⏮️", command=self.prev_song, **button_style)
        self.prev_button.grid(row=0, column=0, padx=5, pady=5)

        self.play_button = tk.Button(control_buttons_frame, text="▶️", command=self.play_song, **button_style)
        self.play_button.grid(row=0, column=1, padx=5, pady=5)

        self.pause_button = tk.Button(control_buttons_frame, text="⏸️", command=self.pause_song, **button_style)
        self.pause_button.grid(row=0, column=2, padx=5, pady=5)

        self.stop_button = tk.Button(control_buttons_frame, text="⏹️", command=self.stop_song, **button_style)
        self.stop_button.grid(row=0, column=3, padx=5, pady=5)

        self.next_button = tk.Button(control_buttons_frame, text="⏭️", command=self.next_song, **button_style)
        self.next_button.grid(row=0, column=4, padx=5, pady=5)

        # Add/Remove Buttons below main controls (within the same playback_panel_frame)
        action_button_style = {
            "font": ("Helvetica", 11, "bold"), # Font changed here
            "bg": "#2A3A2A", # More distinct dark green for action buttons
            "fg": "#FFFFFF",
            "activebackground": "#4CAF50", # Vibrant Green on click
            "activeforeground": "#FFFFFF", # White text on click
            "relief": tk.FLAT,
            "bd": 0,
            "padx": 15,
            "pady": 8,
            "width": 12
        }
        self.add_button = tk.Button(playback_panel_frame, text="Add Songs", command=self.add_songs, **action_button_style)
        self.add_button.pack(side=tk.LEFT, padx=(30, 5), pady=10) # Pack to the left

        self.remove_button = tk.Button(playback_panel_frame, text="Remove Song", command=self.remove_song, **action_button_style)
        self.remove_button.pack(side=tk.RIGHT, padx=(5, 30), pady=10) # Pack to the right

        # Volume control (integrated into the playback_panel_frame)
        volume_control_frame = tk.Frame(playback_panel_frame, bg="#1A2A1A") # Matches playback panel background
        volume_control_frame.pack(pady=(5, 10), fill=tk.X)

        tk.Label(volume_control_frame, text="Volume:", font=("Helvetica", 10), fg="#E0E0E0", bg="#1A2A1A").pack(side=tk.LEFT, padx=(30, 10)) # Font changed here
        self.volume_slider = tk.Scale(volume_control_frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                      command=self.set_volume, bg="#1A2A1A", fg="#4CAF50", # Vibrant Green for slider
                                      highlightbackground="#1A2A1A", troughcolor="#66BB6A", # Brighter green trough for visibility
                                      length=200, relief=tk.FLAT, bd=0, showvalue=0) # Hide default value
        self.volume_slider.set(50) # Set initial volume to 50%
        self.volume_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 30)) # Add padx to the right

    def add_songs(self):
        """
        Opens a file dialog to allow the user to select multiple music files
        (MP3 and WAV formats are supported). Adds selected songs to the playlist
        and updates the listbox.
        """
        songs = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select Music Files",
                                           filetypes=(("MP3 Files", "*.mp3"),
                                                      ("WAV Files", "*.wav"),
                                                      ("All Files", "*.*")))
        if songs:
            for song in songs:
                self.playlist.append(song)
                song_name = os.path.basename(song) # Get just the filename for display
                self.playlist_listbox.insert(tk.END, song_name)
            messagebox.showinfo("Success", f"{len(songs)} song(s) added to playlist.")
            # Update initial artist/album text if songs are added
            if self.artist_album_label.cget("text") == "Add songs to start listening!":
                self.artist_album_label.config(text="Ready to play!")
        else:
            messagebox.showinfo("Info", "No songs selected.")

    def on_song_select(self, event=None):
        """
        Called when a song is selected in the playlist listbox.
        Updates the current_song_index and plays the selected song.
        """
        selected_indices = self.playlist_listbox.curselection()
        if selected_indices:
            self.current_song_index = selected_indices[0]
            self.play_song()

    def play_song(self):
        """
        Plays the currently selected song. If paused, it resumes playback.
        If no song is selected, it attempts to play the first song in the playlist.
        """
        if not self.playlist:
            self.song_title_label.config(text="Please add songs to the playlist.")
            self.artist_album_label.config(text="")
            return

        if self.is_paused:
            mixer.music.unpause()
            self.is_paused = False
            self.play_button.config(text="⏸️") # Change icon to pause when playing
        else:
            if self.current_song_index == -1:
                # If no song was explicitly selected, try to play the first one
                if self.playlist:
                    self.song_title_label.config(text="No songs in playlist to play.")
                    self.artist_album_label.config(text="")
                    return

            try:
                song_path = self.playlist[self.current_song_index]
                mixer.music.load(song_path)
                mixer.music.play()
                self.update_song_info(song_path)
                self.play_button.config(text="⏸️") # Change icon to pause when playing
            except Exception as e:
                messagebox.showerror("Playback Error", f"Could not play song: {e}")
                self.song_title_label.config(text="Error playing song.")
                self.artist_album_label.config(text="Check file path or format.")

    def pause_song(self):
        """Pauses the currently playing song."""
        if mixer.music.get_busy():
            mixer.music.pause()
            self.is_paused = True
            self.play_button.config(text="▶️") # Change icon to play when paused

    def stop_song(self):
        """Stops the currently playing song and resets the player state."""
        mixer.music.stop()
        self.is_paused = False
        self.song_title_label.config(text="No song loaded")
        self.artist_album_label.config(text="Add songs to start listening!")
        self.play_button.config(text="▶️") # Reset icon to play

    def next_song(self):
        """Plays the next song in the playlist."""
        if self.playlist:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self.playlist_listbox.selection_clear(0, tk.END)
            self.playlist_listbox.selection_set(self.current_song_index)
            self.play_song()
        else:
            messagebox.showinfo("Info", "Playlist is empty.")

    def prev_song(self):
        """Plays the previous song in the playlist."""
        if self.playlist:
            self.current_song_index = (self.current_song_index - 1 + len(self.playlist)) % len(self.playlist)
            self.playlist_listbox.selection_clear(0, tk.END)
            self.playlist_listbox.selection_set(self.current_song_index)
            self.play_song()
        else:
            messagebox.showinfo("Info", "Playlist is empty.")

    def remove_song(self):
        """Removes the selected song from the playlist and listbox."""
        selected_indices = self.playlist_listbox.curselection()
        if selected_indices:
            index_to_remove = selected_indices[0]
            
            # Stop playback if the removed song was currently playing
            if index_to_remove == self.current_song_index:
                self.stop_song()
                self.current_song_index = -1 # Reset current song index

            # Remove from listbox and internal playlist
            self.playlist_listbox.delete(index_to_remove)
            del self.playlist[index_to_remove]

            # Adjust current_song_index if a song before it was removed
            if index_to_remove < self.current_song_index:
                self.current_song_index -= 1
            elif index_to_remove == self.current_song_index and not self.playlist:
                # If the last song was removed and playlist is now empty
                self.current_song_index = -1
                self.song_title_label.config(text="No song loaded")
                self.artist_album_label.config(text="Add songs to start listening!")
            elif index_to_remove == self.current_song_index and self.playlist:
                # If the current song was removed, and there are still songs,
                # set index to the new song at the same position (if exists)
                # or the last song if the removed one was the last.
                if self.current_song_index >= len(self.playlist):
                    self.current_song_index = len(self.playlist) - 1
                # No need to play automatically, user can select next
            messagebox.showinfo("Success", "Song removed from playlist.")
        else:
            messagebox.showinfo("Info", "Please select a song to remove.")

    def set_volume(self, val):
        """Sets the volume of the music player."""
        volume = float(val) / 100
        mixer.music.set_volume(volume)

    def update_song_info(self, song_path):
        """Updates the labels with the name of the currently playing song and placeholder artist/album."""
        song_name = os.path.basename(song_path)
        self.song_title_label.config(text=song_name)
        # For a real Spotify-like player, you'd extract actual artist/album from metadata
        self.artist_album_label.config(text="Unknown Artist - Unknown Album")

# Main execution block
if __name__ == "__main__":
    root = tk.Tk()
    player = MusicPlayer(root)
    root.mainloop()
