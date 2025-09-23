from src.cleaning import to_region_group

def test_region_map():
    assert to_region_group('Московская область', ['московская область']) == 'MO'
    assert to_region_group('Санкт-Петербург', ['московская область']) == 'Rest'
