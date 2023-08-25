def test_get_token_bot():
    from main import get_token_bot
    file1 = get_token_bot()
    assert file1 != None
    file2 = get_token_bot(filename='requirements.txt')
    assert file2 != None
