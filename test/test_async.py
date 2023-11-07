import aiounittest

from ddt import ddt, data
from test.mycode import larger_than_two


@ddt
class TestAsync(aiounittest.AsyncTestCase):
    @data(3, 4, 12, 23)
    async def test_larger_than_two(self, value):
        self.assertTrue(larger_than_two(value))
