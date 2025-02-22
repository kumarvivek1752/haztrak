from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from .base_models import SitesBaseModel
from .site_models import Site


class RcraProfile(SitesBaseModel):
    """
    Contains a user's RcraProfile information, such as username, and API credentials.
    Has a one-to-one relationship with the User model.
    """

    class Meta:
        ordering = ["rcra_username"]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    rcra_api_key = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    rcra_api_id = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    rcra_username = models.CharField(
        max_length=128,
        null=True,
        blank=True,
    )
    phone_number = models.CharField(
        max_length=15,
        null=True,
        blank=True,
    )
    email = models.EmailField()

    def __str__(self):
        return f"{self.user.username}"

    def sync(self):
        """Launch task to sync use profile. ToDo: remove this method"""
        from apps.sites.tasks import sync_user_sites

        task = sync_user_sites.delay(str(self.user.username))
        return task

    @property
    def is_api_user(self) -> bool:
        """Returns true if the use has Rcrainfo API credentials"""
        if self.rcra_username and self.rcra_api_id and self.rcra_api_key:
            return True
        return False


class RcraSitePermission(SitesBaseModel):
    """
    RCRAInfo Site Permissions per module connected to a user's RcraProfile
    and the corresponding Site
    """

    CERTIFIER = "Certifier"
    PREPARER = "Preparer"
    VIEWER = "Viewer"

    EPA_PERMISSION_LEVEL = [
        (CERTIFIER, "Certifier"),
        (PREPARER, "Preparer"),
        (VIEWER, "Viewer"),
    ]

    class Meta:
        verbose_name = "RCRA Site Permission"
        ordering = ["site__rcra_site__epa_id"]

    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    profile = models.ForeignKey(
        RcraProfile,
        on_delete=models.PROTECT,
        related_name="permissions",
    )
    site_manager = models.BooleanField(
        default=False,
    )
    annual_report = models.CharField(
        max_length=12,
        choices=EPA_PERMISSION_LEVEL,
    )
    biennial_report = models.CharField(
        max_length=12,
        choices=EPA_PERMISSION_LEVEL,
    )
    e_manifest = models.CharField(
        max_length=12,
        choices=EPA_PERMISSION_LEVEL,
    )
    my_rcra_id = models.CharField(
        max_length=12,
        choices=EPA_PERMISSION_LEVEL,
    )
    wiets = models.CharField(
        max_length=12,
        choices=EPA_PERMISSION_LEVEL,
    )

    def __str__(self):
        return f"{self.profile.user}: {self.site.rcra_site.epa_id}"

    def clean(self):
        if self.site_manager:
            fields = ["annual_report", "biennial_report", "e_manifest", "my_rcra_id", "wiets"]
            for field_name in fields:
                if getattr(self, field_name) != "Certifier":
                    raise ValidationError(
                        f"The value for the '{field_name}' field must be set to 'Certifier'."
                    )
