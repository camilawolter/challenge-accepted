from main import InchFromMillimeters, FahrenheitFromCelsius

def test_InchFromMillimeters():
    assert abs(InchFromMillimeters(0) - 0.0) < 0.01
    assert abs(InchFromMillimeters(1) - 0.0) < 0.01
    assert abs(InchFromMillimeters(2) - 0.1) < 0.01
    assert abs(InchFromMillimeters(3) - 0.1) < 0.01
    assert abs(InchFromMillimeters(4) - 0.2) < 0.01
    assert abs(InchFromMillimeters(5) - 0.2) < 0.01
    assert abs(InchFromMillimeters(6) - 0.2) < 0.01
    assert abs(InchFromMillimeters(7) - 0.3) < 0.01
    assert abs(InchFromMillimeters(8) - 0.3) < 0.01
    assert abs(InchFromMillimeters(9) - 0.4) < 0.01
    assert abs(InchFromMillimeters(10) - 0.4) < 0.01
    assert abs(InchFromMillimeters(11) - 0.4) < 0.01
    assert abs(InchFromMillimeters(12) - 0.5) < 0.01
    assert abs(InchFromMillimeters(13) - 0.5) < 0.01
    assert abs(InchFromMillimeters(14) - 0.6) < 0.01
    assert abs(InchFromMillimeters(15) - 0.6) < 0.01
    assert abs(InchFromMillimeters(20) - 0.8) < 0.01
    assert abs(InchFromMillimeters(30) - 1.2) < 0.01
    assert abs(InchFromMillimeters(40) - 1.6) < 0.01
    assert abs(InchFromMillimeters(50) - 2.0) < 0.01

def test_FahrenheitFromCelsius():
    assert abs(FahrenheitFromCelsius(-50) + 58) < 0.01
    assert abs(FahrenheitFromCelsius(-40) + 40) < 0.01
    assert abs(FahrenheitFromCelsius(-30) + 22) < 0.01
    assert abs(FahrenheitFromCelsius(-20) + 4) < 0.01
    assert abs(FahrenheitFromCelsius(-10) - 14) < 0.01
    assert abs(FahrenheitFromCelsius(0) - 32) < 0.01
    assert abs(FahrenheitFromCelsius(10) - 50) < 0.01
    assert abs(FahrenheitFromCelsius(20) - 68) < 0.01
    assert abs(FahrenheitFromCelsius(30) - 86) < 0.01
    assert abs(FahrenheitFromCelsius(40) - 104) < 0.01
    assert abs(FahrenheitFromCelsius(50) - 122) < 0.01
    assert abs(FahrenheitFromCelsius(60) - 140) < 0.01
    assert abs(FahrenheitFromCelsius(70) - 158) < 0.01
    assert abs(FahrenheitFromCelsius(80) - 176) < 0.01
    assert abs(FahrenheitFromCelsius(90) - 194) < 0.01
    assert abs(FahrenheitFromCelsius(100) - 212) < 0.01
