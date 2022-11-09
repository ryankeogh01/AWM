from django.contrib.gis.db import models


class WorldBorder(models.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2, default=0)
    iso2 = models.CharField('2 Digit ISO', max_length=2, default=0)
    iso3 = models.CharField('3 Digit ISO', max_length=3, default=0)
    un = models.IntegerField('United Nations Code', default=0)
    region = models.IntegerField('Region Code', default=0)
    subregion = models.IntegerField('Sub-Region Code', default=0)
    lon = models.FloatField(default=0)
    lat = models.FloatField(default=0)

    # GeoDjango-specific: a geometry field (MultiPolygonField)
    mpoly = models.MultiPolygonField()

    # Returns the string representation of the model.
    def __str__(self):
        return self.name
