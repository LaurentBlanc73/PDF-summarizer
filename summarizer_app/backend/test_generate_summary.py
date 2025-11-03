import pytest
from generate_summary import generate_summary


def test_generate_summary():
    # test for empty input
    assert "" == generate_summary(text="")

    # test expected behavior
    article = """The mayor of the city announced new environmental policies today aimed at reducing emissions 
    by 40% by 2035. The initiative includes expanded public transit, incentives for electric vehicles, and stricter 
    regulations on industrial polluters."""
    assert type(generate_summary(text=article)) is str

    # test error paths
    with pytest.raises(ValueError, match=r"Input has wrong type. Should be str, was .*"):
        generate_summary(2)
