def test_leading_pipe_flat_record_positions():
    record = "|D|Elena|223457|20101012|20121013|GLD|Sam|CA|USA|03051985|A"
    fields = record.split("|")
    assert fields[1] == "D"
    assert fields[2] == "Elena"
    assert fields[3] == "223457"
    assert fields[4] == "20101012"
    assert fields[5] == "20121013"
    assert fields[9] == "USA"
    assert fields[10] == "03051985"
    assert fields[11] == "A"
