#### **SpotifyFlopy: Minimal Spotify Playlist Downloader**

SpotifyFlopy is a simple, web-based application that allows users to download songs from any Spotify playlist by providing the playlist link. Users can set their own Spotify API credentials and download high-quality music directly to their local machines.

---

### **Features**
- User-friendly web interface with a minimal and light theme.
- Input Spotify API credentials directly on the app.
- Fetch and display all songs from any Spotify playlist.
- Download songs in high quality.

---

### **Requirements**
1. **Python** (version 3.8 or higher)
2. Required Python modules:
   - `Flask`
   - `spotipy`
   - `youtube-dl`
   - `yt-dlp` (optional, if replacing `youtube-dl`)
   - `requests`
   - `beautifulsoup4`

---

### **Installation and Setup**

#### **Step 1: Clone the Repository**
Clone the project to your local machine:
```bash
git clone https://github.com/your-repo/SpotifyFlopy.git
cd SpotifyFlopy
```

#### **Step 2: Install Dependencies**
Install the required Python modules:
```bash
pip install flask spotipy youtube-dl requests beautifulsoup4
```
If you encounter issues with `youtube-dl`, consider using `yt-dlp`:
```bash
pip install yt-dlp
```

#### **Step 3: Run the Application**
Run the Flask app locally:
```bash
python app.py
```

The app will be available at: [http://localhost:5000](http://localhost:5000)

---

### **Usage**

#### **1. Set Spotify API Credentials**
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/) and create an app.
2. Copy the **Client ID**, **Client Secret**, and set the **Redirect URI** (e.g., `http://localhost:5000/callback`).
3. Open the app in your browser and input these credentials in the **SpotifyFlopy** form.

#### **2. Download Songs from a Playlist**
1. Enter the Spotify playlist URL in the provided form.
2. Click **List Songs** to fetch the songs from the playlist.
3. View the list of songs and download them to your local system.

---

### **Troubleshooting**

1. **Error: `ModuleNotFoundError`**  
   Ensure all dependencies are installed. Run:
   ```bash
   pip install -r requirements.txt
   ```
   *(Create a `requirements.txt` file with the required modules for convenience.)*

2. **Spotify API Credential Errors**:  
   Double-check your Client ID, Client Secret, and Redirect URI.

3. **Music Not Downloading**:  
   Ensure `youtube-dl` or `yt-dlp` is properly installed. Update it if needed:
   ```bash
   youtube-dl -U
   ```

---

### **Future Enhancements**
- Add support for downloading entire playlists at once.
- Enhance error handling and provide detailed feedback.
- Include a Docker setup for easy deployment.

---

### **Contributors**
- **Yash Bhujbal**  
  *Developer & Maintainer*

Feel free to fork and contribute to this project!
