# test_task4_param.py
import pytest
from task4 import count_moves, read_nums_file, MOVE_LIMIT


@pytest.mark.parametrize(
    "nums, limit, expected",
    [
        ([5, 5, 5], MOVE_LIMIT, 0),

        ([0, 0, 10, 10], MOVE_LIMIT, 20),  # 20

        ([0, 0, 0, 21], MOVE_LIMIT, None),

        ([-2, -1, 3], MOVE_LIMIT, 5),

        ([4, 5, 6, 3], MOVE_LIMIT, 4),

        ([1000, -1000, 0], MOVE_LIMIT, None),
    ],
)
def test_count_moves(nums, limit, expected):
    assert count_moves(nums, limit) == expected



@pytest.mark.parametrize(
    "content, expected, exc_match",
    [
        # Валидный файл с пустыми строками
        ("3\n\n6\n8\n9\n", [3, 6, 8, 9], None),

        ("1\n 16\n test_no_int\n 20\n", None, "должен состоять из целых чисел. На строке с номером"),

        ("\n \n\t\n", None, "не содержит целых чисел"),
    ],
)
def test_read_nums_file(tmp_path, content, expected, exc_match):
    p = tmp_path / "nums.txt"
    p.write_text(content, encoding="utf-8")
    with p.open("r", encoding="utf-8") as f:
        if exc_match is None:
            assert read_nums_file(f) == expected
        else:
            with pytest.raises(ValueError, match=exc_match):
                read_nums_file(f)
