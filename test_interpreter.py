import pytest
import interpreter

def test_basic_arithmetic():
    code = """
    x = 5 + 3
    fwnakse(x)
    """
    output = interpreter.run(code, capture_output=True)
    assert "8.0" in output

def test_if_else():
    code = """
    x = 10
    if x > 5
    fwnakse("megalo")
    kotsif
    fwnakse("mikro")
    miaou
    """
    output = interpreter.run(code, capture_output=True)
    assert "megalo" in output

def test_while_loop():
    code = """
    x = 3
    skarfalwnontas x > 0
    fwnakse(x)
    x = x - 1
    miaou
    """
    output = interpreter.run(code, capture_output=True)
    assert "3.0" in output
    assert "2.0" in output
    assert "1.0" in output

def test_timeout():
    code = """
    x = 1
    skarfalwnontas x > 0
    x = 1
    miaou
    """
    with pytest.raises(interpreter.TimeoutException):
        interpreter.run(code, timeout=0.1, capture_output=True)

def test_functions():
    code = """
    banana prosfesi(a)
    x = a + 5
    fwnakse(x)
    miaou
    
    prosfesi(10)
    """
    output = interpreter.run(code, capture_output=True)
    assert "15.0" in output

def test_arrays():
    code = """
    x = [10, 20, 30]
    fwnakse(x[0])
    fwnakse(x[1] + 5)
    fwnakse(x[2])
    """
    output = interpreter.run(code, capture_output=True)
    assert "10.0" in output
    assert "25.0" in output
    assert "30.0" in output
