# Faster-Watching

A simple Python script that automatically generates summaries and actionable takeaways from YouTube videos as they are added to a playlist and saves them to your preferred location and format.

**Features:**
* Automatically checks a designated YouTube playlist for new video additions.
* Fetches the video transcript using the `youtube-transcript-api`.
* Uses the powerful and efficient Gemini 2.5 Flash model to create a concise summary and a bulleted list of key takeaways.
* Supports output in Markdown (.md), DOCX (.docx), and plain text (.txt) formats.
* Appends the output to a single file, creating a searchable archive of video insights.

<hr>

### Getting Started

These instructions will get you a copy of the project up and running on your local machine.

#### **Prerequisites**

You will need:
* **Python 3.8 or higher** installed on your system.
* A **YouTube Data API v3 key** from the [Google Cloud Console](https://console.cloud.google.com/).
* A **Gemini API key** from [Google AI Studio](https://aistudio.google.com/app/apikey).
* **Git** for cloning the repository.
* The `python-docx` library, which is required for DOCX output.

#### **Installation**

1.  **Clone the Repository**
    ```sh
    git clone [https://github.com/your-username/faster-watching.git](https://github.com/your-username/faster-watching.git)
    cd faster-watching
    ```

2.  **Set Up a Python Virtual Environment**
    This ensures that the project's dependencies don't interfere with your global Python packages.
    ```sh
    # Create the virtual environment
    python3 -m venv venv

    # Activate the virtual environment
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    venv\Scripts\activate
    ```

3.  **Install Dependencies**
    With your virtual environment activated, install all required Python libraries.
    ```sh
    pip install -r requirements.txt
    ```

<hr>

### Configuration and Usage

1.  **Environment Variables**
    For security and ease of use, you can manage your configuration variables through a `.env` file in the root of your project. Create a file named `.env` and add the following variables, replacing the placeholders with your actual values.

    * `PLAYLIST_ID`: The ID of the YouTube playlist to monitor.
    * `YOUTUBE_API_KEY`: Your YouTube Data API v3 key.
    * `GEMINI_API_KEY`: Your Gemini API key.
    * `OUTPUT_PATH`: The path to the directory where you want to save the output file.
    * `OUTPUT_FORMAT`: The desired output format. **Must be one of `md`, `docx`, or `txt`**.

    ```ini
    # .env example
    PLAYLIST_ID="YOUR_PLAYLIST_ID"
    YOUTUBE_API_KEY="YOUR_YOUTUBE_API_KEY"
    GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
    OUTPUT_PATH="C:/Users/YourUser/Documents/ObsidianVault"
    OUTPUT_FORMAT="md"
    ```
    

2.  **Run the Script**
    You can test the script by running it manually from the terminal.
    ```sh
    python main.py
    ```

Working on how to run uninterrupted !!
<hr>

### License

This project is licensed under the MIT License.