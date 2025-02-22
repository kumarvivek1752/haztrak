import json

import pytest

from apps.sites.models import RcraSitePermission
from apps.sites.serializers import (
    ContactSerializer,
    RcraPermissionSerializer,
    RcraSitePermissionSerializer,
    RcraSiteSerializer,
)


class TestContactSerializer:
    @pytest.fixture
    def contact_serializer(self, haztrak_json) -> ContactSerializer:
        return ContactSerializer(data=haztrak_json.CONTACT.value)

    def test_serializes_contact_model(self, contact_serializer) -> None:
        assert contact_serializer.is_valid() is True


class TestRcraSiteSerializer:
    @pytest.fixture
    def rcra_site_serializer(self, haztrak_json) -> RcraSiteSerializer:
        return RcraSiteSerializer(data=haztrak_json.HANDLER.value)

    def test_serializes(self, rcra_site_serializer):
        assert rcra_site_serializer.is_valid() is True


class TestRcraSitePermissionSerializer:
    """
    This Test suite is for haztrak's internal record of
    user's RCRAInfo site permissions.
    """

    @pytest.fixture(autouse=True)
    def _permissions(self, rcra_permission_factory):
        self.permissions = rcra_permission_factory()

    @pytest.fixture
    def permission_serializer(self, haztrak_json) -> RcraSitePermissionSerializer:
        return RcraSitePermissionSerializer(data=haztrak_json.SITE_PERMISSION.value)

    def test_serializes(self, permission_serializer) -> None:
        assert permission_serializer.is_valid() is True

    def test_object_serializes_permission_object(self) -> None:
        serializer = RcraSitePermissionSerializer(self.permissions)
        site_permission_json = json.dumps(serializer.data)
        assert str(self.permissions.biennial_report) in site_permission_json


class TestEpaPermissionSerializer:
    """
    This Test suite is for Haztrak's serializer for communication with
    RCRAInfo for a user's site permissions.

    We don't use EPaPermissionSerializer to communicate internally, so
    currently we don't serialize, only deserialize
    """

    @pytest.fixture
    def epa_permission_serializer(self, haztrak_json) -> RcraPermissionSerializer:
        return RcraPermissionSerializer(data=haztrak_json.EPA_PERMISSION.value)

    def test_deserializes_epa_permissions(
        self, epa_permission_serializer, rcra_profile_factory, site_factory
    ) -> None:
        if not epa_permission_serializer.is_valid():
            # if something is wrong with the serializer fixture, fail
            assert False
        RcraSitePermission.objects.create(
            **epa_permission_serializer.validated_data,
            site=site_factory(),
            profile=rcra_profile_factory(),
        )
