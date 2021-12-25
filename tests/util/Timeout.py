from multiprocessing.context import Process
from deprecated.sphinx import deprecated


@deprecated(version='0.1.0', reason="no multiprocessnig")
def timeoutTestCase( method,timeout) -> object:
    """
    currently not used

    :param method: python method
    :param timeout: time
    :return: bool, true or false
    """
    p1 = Process(target=method, name='Process_inc_forever')
    p1.start()
    p1.join(timeout=timeout)
    p1.terminate()
    if p1.exitcode is None:
        return False
    else:
        return True