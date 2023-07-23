import os

from django.test import TestCase
import environ


# Create your tests here.
class GetEnvTest(TestCase):

    def test_get_environment_variable(self):
        env = environ.Env(
            # set casting, default value
            DEBUG=(bool, False)
        )

        # Set the project base directory
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Take environment variables from .env file
        environ.Env.read_env(os.path.join(BASE_DIR, 'girlfriend_gpt/../girlfriend_gpt/../.env'))

        OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')  # 기본 사용방법
        print(OPENAI_API_KEY)
        self.assertIsNotNone(OPENAI_API_KEY)