from bot.utils import parse_amount, detect_direction, convert


def test_parse_amount():
    assert parse_amount('100 TON')[0] == 100
    assert parse_amount('1,5 ton')[0] == 1.5
    assert parse_amount('2500 руб')[0] == 2500
    assert parse_amount('abc') is None


def test_detect_direction():
    assert detect_direction('ton', 'ton_to_rub') == ('TON', 'RUB')
    assert detect_direction('rub', 'ton_to_rub') == ('RUB', 'TON')
    assert detect_direction('', 'rub_to_ton') == ('RUB', 'TON')


def test_convert():
    price = 100
    assert convert(2, 'TON', price) == 200
    assert convert(200, 'RUB', price) == 2
