
import json
import sys
import pathlib
import copy
import task3

VALUES_OBJ = {
  "values": [
    {"id": 2, "value": "passed"},
    {"id": 41, "value": "passed"},
    {"id": 73, "value": "passed"},
    {"id": 110, "value": "failed"},
    {"id": 122, "value": "failed"},
    {"id": 234, "value": "passed"},
    {"id": 238, "value": "passed"},
    {"id": 345, "value": "passed"},
    {"id": 653, "value": "passed"},
    {"id": 690, "value": "failed"},
    {"id": 5321, "value": "passed"},
    {"id": 5322, "value": "failed"},
  ]
}

TESTS_OBJ = {
  "tests": [
    {"id": 2, "title": "Smoke test", "value": ""},
    {"id": 41, "title": "Debug test", "value": ""},
    {
      "id": 73,
      "title": "Performance test",
      "value": "",
      "values": [
        {
          "id": 345,
          "title": "Maxperf",
          "value": "",
          "values": [{
            "id": 230,
            "title": "Percent",
            "values": [
              {"id": 234, "title": "200", "value": ""},
              {"id": 653, "title": "300", "value": ""},
            ],
          }],
        },
        {
          "id": 110,
          "title": "Stability test",
          "value": "",
          "values": [{
            "id": 261,
            "title": "Percent",
            "values": [
              {"id": 238, "title": "160", "value": ""},
              {"id": 690, "title": "240", "value": ""},
            ],
          }],
        },
      ],
    },
    {
      "id": 122,
      "title": "Security test",
      "value": "",
      "values": [
        {"id": 5321, "title": "Confidentiality", "value": ""},
        {"id": 5322, "title": "Integrity", "value": ""},
      ],
    },
  ]
}

def test_set_value():
    node = copy.deepcopy(TESTS_OBJ)
    res = {str(x["id"]): x["value"] for x in VALUES_OBJ["values"]}

    task3.set_value(node, res)

    assert node["tests"][0]["value"] == "passed"   # id=2
    assert node["tests"][1]["value"] == "passed"   # id=41
    assert node["tests"][2]["values"][0]["value"] == "passed"  # id=345
    assert node["tests"][2]["values"][1]["value"] == "failed"  # id=110

    assert "value" not in node["tests"][2]["values"][0]["values"][0]  # id=230



def test_cli_real(tmp_path: pathlib.Path):
    values_path = tmp_path / "values.json"
    tests_path = tmp_path / "tests.json"
    report_path = tmp_path / "report.json"

    values_path.write_text(json.dumps(VALUES_OBJ), encoding="utf-8")
    tests_path.write_text(json.dumps(TESTS_OBJ), encoding="utf-8")

    argv_backup = sys.argv[:]
    try:
        sys.argv = ["task3.py", str(values_path), str(tests_path), str(report_path)]
        try:
            task3.main()
        except SystemExit as e:
            assert int(e.code) == 0
    finally:
        sys.argv = argv_backup

    report = json.loads(report_path.read_text(encoding="utf-8"))

    assert report["tests"][2]["values"][1]["values"][0]["values"][1]["value"] == "failed"  # id=690
    assert report["tests"][3]["values"][0]["value"] == "passed"  # id=5321

    assert "value" not in report["tests"][2]["values"][0]["values"][0]  # id=230
