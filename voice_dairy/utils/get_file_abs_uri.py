from pathlib import Path


def get_file_abs_uri(audio_file):
        """Convert local audio file path to URI format.
        
        Args:
            audio_file (str): Path to audio file
            
        Returns:
            str: URI formatted file path
        """
        abs_path = Path(audio_file).expanduser().resolve()
        return abs_path.as_uri()