from psdomain.model.base import ErrorMessage, ServiceMessage, Severity, ServiceMessageArray


def test_error_message():
    err = ErrorMessage(code=223, description="Test Error")
    assert err.code == 223
    assert err.description == "Test Error"
    #
    assert str(err) == '223 - Test Error'


def test_service_message():
    err = ServiceMessage(code=223, description="Test Error", severity=Severity.ERROR)
    assert err.code == 223
    assert err.description == "Test Error"
    #
    assert str(err) == '223 - Test Error - Error'
    # with severity in lowercase
    err_str = '{"code": 223, "description": "Test Error", "severity": "error"}'
    err = ServiceMessage.model_validate_json(err_str)
    assert err.code == 223
    assert err.description == "Test Error"
    assert err.severity == Severity.ERROR


def test_service_message_array():
    err1 = ServiceMessage(code=223, description="Test Error", severity=Severity.ERROR)
    err2 = ServiceMessage(code=523, description="Test Warning", severity=Severity.WARNING)
    arr = ServiceMessageArray(ServiceMessage=[err1, err2])
    #
    assert str(arr) == '223 - Test Error - Error\n523 - Test Warning - Warning'
