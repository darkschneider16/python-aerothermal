from behave import *
from iber import Iber

@given('credentials')
def step_impl(context):
    """Step credentials"""
    context.connection = Iber()
