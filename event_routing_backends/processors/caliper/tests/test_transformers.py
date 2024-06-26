"""
Test the transformers for all of the currently supported events into Caliper format.
"""
import os

from django.test import TestCase

from event_routing_backends.processors.caliper.registry import CaliperTransformersRegistry
from event_routing_backends.processors.tests.transformers_test_mixin import (
    TransformersFixturesTestMixin,
    TransformersTestMixin,
)


class CaliperTransformersFixturesTestMixin(TransformersFixturesTestMixin):
    """
    Mixin for testing Caliper event transformers.

    This mixin is split into its own class so it can be used by packages outside of ERB.
    """
    registry = CaliperTransformersRegistry

    @property
    def expected_events_fixture_path(self):
        """
        Return the path to the expected transformed events fixture files.
        """
        return '{}/fixtures/expected'.format(os.path.dirname(os.path.abspath(__file__)))

    def assert_correct_transformer_version(self, transformed_event, transformer_version):
        self.assertEqual(transformed_event['extensions']['transformerVersion'], transformer_version)

    def compare_events(self, transformed_event, expected_event):
        """
        Test that transformed_event and expected_event are identical.

        Arguments:
            transformed_event (dict)
            expected_event (dict)

        Raises:
            AssertionError:     Raised if the two events are not same.
        """
        # id is a randomly generated UUID therefore not comparing that
        self.assertIn('id', transformed_event)
        expected_event.pop('id')
        transformed_event.pop('id')
        self.assertDictEqual(expected_event, transformed_event)


class TestCaliperTransformers(CaliperTransformersFixturesTestMixin, TransformersTestMixin, TestCase):
    """
    Test that supported events are transformed into Caliper format correctly.
    """
