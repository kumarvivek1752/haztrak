import pytest
from django.db import IntegrityError

from apps.trak.models import WasteCode


@pytest.mark.django_db
class TestWasteCodesModel:
    federal_codes = [
        ("D001", "IGNITABLE WASTE"),
        ("D002", "CORROSIVE WASTE"),
        ("D003", "REACTIVE WASTE"),
    ]
    state_waste_codes = [
        ("123", "Unspecified alkaline solution"),
        ("131", "Aqueous solution (2 < pH < 12.5) containing reactive anions"),
        ("132", "Aqueous solution w/metals"),
        ("133", "Aqueous solution with 10% or more total organic residues"),
    ]

    @pytest.fixture
    def create_codes(self, waste_code_factory):
        for code in self.federal_codes:
            waste_code_factory(code=code[0], description=[1], code_type=WasteCode.CodeType.FEDERAL)
        for code in self.state_waste_codes:
            waste_code_factory(code=code[0], description=[1], code_type=WasteCode.CodeType.STATE)

    def test_base_manager_retrieves_all(self, create_codes) -> None:
        # Act
        codes = WasteCode.objects.all()
        # Assert
        assert len(codes) == (len(self.state_waste_codes) + len(self.federal_codes))

    def test_federal_manager_retrieves_federal_waste_codes(self, create_codes) -> None:
        # Act
        codes = WasteCode.federal.all()
        # Assert
        assert len(codes) == len(self.federal_codes)

    def test_state_manager_retrieves_state_waste_codes(self, create_codes) -> None:
        codes = WasteCode.state.all()
        assert len(codes) == len(self.state_waste_codes)

    def test_waste_codes_are_unique(self, waste_code_factory) -> None:
        code = "D005"
        waste_code_factory(code=code)
        with pytest.raises(IntegrityError):
            WasteCode.objects.create(code=code)
