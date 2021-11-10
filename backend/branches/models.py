from django.db import models


class Branch(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "branches"

    def __str__(self):
        return "%d - %s" % (self.id, self.name)


class BranchProducts(models.Model):
    branch = models.CharField(max_length=50)

    class Meta:
        db_table = "branches"

    def __str__(self):
        return "%d - %s" % (self.id, self.name)
