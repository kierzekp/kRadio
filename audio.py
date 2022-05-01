import vlc

class AudioPlayer:
    def __init__(self) -> None:
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()

        self.playing = False

    def set_media(self, stream_url: str):
        self.player.set_media(self.instance.media_new(stream_url))

    def set_volume(self, volume: int):
        self.player.audio_set_volume(volume)

    def play_media(self):
        self.playing = True
        self.player.play()

    def stop_media(self):
        self.playing = False
        self.player.stop()