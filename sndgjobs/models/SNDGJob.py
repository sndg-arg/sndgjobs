import uuid

from django.conf import settings
import random
import string
import subprocess as sp
import shlex

from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel


class SNDGJobStatus(models.TextChoices):
    NEW = 'NW', _('NEW')
    QUEUED = 'QE', _('QUEUED')
    PAUSED = 'PA', _('PAUSED')
    RUNNING = 'RU', _('RUNNING')
    ERROR = 'ER', _('ERROR')
    CANCELLED = 'CA', _('CANCELLED')
    FINISHED = 'FS', _('FINISHED')
    UNKNOWN = 'UK', _('UNKNOWN')



class SNDGJob(PolymorphicModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cmd = models.TextField()
    error = models.TextField()
    retry = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=SNDGJobStatus.choices, default=SNDGJobStatus.NEW)
    stdout = models.TextField(default="")
    stderr = models.TextField(default="")

    def update_status(self, status, text=""):
        jt = SNDGJobTrace(status=status, job=self, info=text)
        self.status = status
        self.trace.add(jt, bulk=False)

    def init(self):
        self.stdout = settings.MEDIA_ROOT + ''.join(
            random.choices(string.ascii_lowercase, k=5)) + ".out"
        self.stderr = settings.MEDIA_ROOT + ''.join(
            random.choices(string.ascii_lowercase, k=5)) + ".err"
        self.update_status(SNDGJobStatus.RUNNING)

    def run(self):
        with open(self.stdout, "w") as hout, open(self.stderr, "w") as herr:
            sp.run(shlex.split(self.cmd), stdout=hout, stderr=herr)

    def __str__(self):
        return str(self.id)



class SNDGJobTrace(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=SNDGJobStatus.choices)
    job = models.ForeignKey(SNDGJob, on_delete=models.CASCADE, related_name="trace")
    info = models.TextField()


"""
import uuid

from django.conf import settings
import random
import string
import subprocess as sp
import shlex

from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel


class SNDGJobStatus(models.TextChoices):
    NEW = 'NW', _('NEW')
    QUEUED = 'QE', _('QUEUED')
    PAUSED = 'PA', _('PAUSED')
    RUNNING = 'RU', _('RUNNING')
    ERROR = 'ER', _('ERROR')
    CANCELLED = 'CA', _('CANCELLED')
    FINISHED = 'FS', _('FINISHED')
    UNKNOWN = 'UK', _('UNKNOWN')



class SNDGJob(PolymorphicModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cmd = models.TextField()
    error = models.TextField()
    retry = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=SNDGJobStatus.choices, default=SNDGJobStatus.NEW)
    stdout = models.TextField(default="")
    stderr = models.TextField(default="")

    def update_status(self, status, text=""):
        jt = SNDGJobTrace(status=status, job=self, info=text)
        self.status = status
        self.trace.add(jt, bulk=False)

    def init(self):
        self.stdout = settings.MEDIA_ROOT + ''.join(
            random.choices(string.ascii_lowercase, k=5)) + ".out"
        self.stderr = settings.MEDIA_ROOT + ''.join(
            random.choices(string.ascii_lowercase, k=5)) + ".err"
        self.update_status(SNDGJobStatus.RUNNING)

    def run(self):
        with open(self.stdout, "w") as hout, open(self.stderr, "w") as herr:
            sp.run(shlex.split(self.cmd), stdout=hout, stderr=herr)

    def __str__(self):
            return self.title



class SNDGJobTrace(PolymorphicModel):
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=2, choices=SNDGJobStatus.choices)
    job = models.ForeignKey(SNDGJob, on_delete=models.CASCADE, related_name="trace")
    info = models.TextField()
"""