# import pytest
#
# @pytest.fixture(scope="session")
# def fixture_1():
#     print("run-fixture-1")
#     return 1
#
#
# def test_example(fixture_1):
#     print("run-example-1")
#     num = fixture_1
#     assert num == 1
#
#
# def test_example2(fixture_1):
#     print("run-example-2")
#     num = fixture_1
#     assert num == 1
#
# # @pytest.mark.xfail
# # def test_example2():
# #     assert 1 == 2