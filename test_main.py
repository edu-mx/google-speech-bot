from main import get_token_bot, TTS
def test_get_token_bot():
    file1 = get_token_bot()
    assert file1 != None
    
    file2 = get_token_bot('requirements.txt')
    assert file2 != None

def test_TTS():
    audio_text = TTS()
    assert audio_text != None
    assert '.mp3' in audio_text

