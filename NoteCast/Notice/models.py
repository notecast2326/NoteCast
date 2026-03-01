from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from pdf2image import convert_from_path
from PIL import Image
import os
from django.core.files import File
class CustomUser(AbstractUser):

    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('hod', 'HOD'),
        ('staff', 'Office Staff'),
    )

    DEPARTMENT_CHOICES = (
        ('bsc_cs', 'B.Sc. Computer Science'),
        ('bsc_micro', 'B.Sc. Microbiology'),
        ('bsc_biochem', 'B.Sc. Biochemistry'),
        ('bsc_biotech', 'B.Sc. Biotechnology'),
        ('bsc_psy', 'B.Sc Psychology'),
        ('bsc_food', 'B.Sc. Food Technology'),
        ('bcom_ca', 'B.Com with Computer Application'),
        ('bcom_fin', 'B.Com Finance'),
        ('bcom_mark', 'B.Com Marketing'),
        ('bcom_coop', 'B.Com Co-operation'),
        ('bba', 'B.B.A.'),
        ('ba_eng', 'B.A English'),
        ('ba_eco', 'B.A Economics'),
        ('msc_cs', 'M.Sc Computer Science'),
        ('msc_biotech', 'M.Sc Biotechnology'),
        ('msc_micro', 'M.Sc Microbiology'),
        ('msc_biochem', 'M.Sc Biochemistry'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    email = models.EmailField(unique=True)

    department = models.CharField(max_length=30, choices=DEPARTMENT_CHOICES, blank=True, null=True)
    admission_no = models.CharField(max_length=50, blank=True, null=True)

    # 🔥 NEW PROFILE FIELDS
    photo = models.ImageField(upload_to='profile_photos/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)
    university_reg_no = models.CharField(max_length=50, blank=True, null=True)

    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']





class Notice(models.Model):

    NOTICE_CATEGORY = (
        ('office', 'Office Notice'),
        ('department', 'Department Notice'),
    )

    DISPLAY_CATEGORY = (
        ('academic', 'Academic Notices'),
        ('events', 'Events & Programs'),
        ('department_updates', 'Department Notices'),
        ('exam', 'Exam Notifications'),
        ('holiday', 'Holiday Announcements'),
        ('urgent', 'Urgent Alerts'),
        ('clubs', 'Clubs & Activities'),
    )

    notice_subject = models.CharField(max_length=200)
    message = models.TextField()
    file_upload = models.FileField(upload_to='notices/', blank=True, null=True)

    # ✅ NEW FIELD
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)

    category = models.CharField(max_length=20, choices=NOTICE_CATEGORY)
    display_category = models.CharField(max_length=30, choices=DISPLAY_CATEGORY)

    department = models.CharField(max_length=100, blank=True, null=True)

    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    # ✅ AUTOMATIC THUMBNAIL GENERATION

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.file_upload and self.file_upload.name.lower().endswith('.pdf'):

            try:
                from pathlib import Path

                # Use Path for safe Windows handling
                pdf_path = Path(self.file_upload.path)
                print("PDF Path:", pdf_path)

                pages = convert_from_path(
                    str(pdf_path),
                    first_page=1,
                    last_page=1,
                    poppler_path=r"C:/poppler-25.12.0/Library/bin"
                )

                if pages:
                    thumb_filename = f"notice_{self.pk}.jpg"
                    thumb_path = Path(settings.MEDIA_ROOT) / "thumbnails" / thumb_filename

                    thumb_path.parent.mkdir(parents=True, exist_ok=True)

                    pages[0].save(str(thumb_path), "JPEG")

                    self.thumbnail = f"thumbnails/{thumb_filename}"
                    super().save(update_fields=["thumbnail"])

                    print("✅ Thumbnail created successfully!")

            except Exception as e:
                print("❌ Thumbnail generation failed:", e)