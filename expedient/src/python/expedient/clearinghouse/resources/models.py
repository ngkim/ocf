'''
@author: jnaous
'''
from django.db import models
from expedient.clearinghouse.aggregate.models import Aggregate
from expedient.common.extendable.models import Extendable
from expedient.clearinghouse.slice.models import Slice
from datetime import datetime
from django.core.exceptions import ValidationError
import re
class Resource(Extendable):
    '''
    Generic model of a resource.
    
    @ivar name: A human-readable name for the resource
    @type name: L{str}
    @ivar available: Is the resources available?
    @type available: C{bool}
    @ivar status_change_timestamp: The time when C{available} changed.
    @type status_change_timestamp: L{datetime.datetime}
    @ivar aggregate: The L{Aggregate} that controls/owns this resource
    @type aggregate: L{models.ForeignKey} to L{Aggregate}
    @ivar slice_set: The set of slices this resource is in
    @type slice_set: a L{models.ManyToManyField} to L{Slice}.
    '''

    def validate_name(value):
        def error():
            raise ValidationError(
                "Invalid input: VM name should not contain blank spaces",
                code="invalid",
            )
        cntrlr_name_re = re.compile("^[\S]*$")
        m = cntrlr_name_re.match(value)
        if not m:
            error()

    
    name = models.CharField(max_length=200)
    available = models.BooleanField("Available", default=True, editable=False)
    status_change_timestamp = models.DateTimeField(
        editable=False, auto_now_add=True)
    aggregate = models.ForeignKey(
        Aggregate, verbose_name="Aggregate the resource belongs to")
    slice_set = models.ManyToManyField(
        Slice, through="Sliver", verbose_name="Slices this resource is used in")
    
    def update_timestamp(self):
        """Set the resource's status change timestamp to now.
        
        This method does not save the object, so the object still
        needs to be manually saved.
        """
        self.status_change_timestamp = datetime.now()
    
    def __unicode__(self):
        return u"Resource %s belonging to aggregate %s." % (
            self.name, self.aggregate.name)
        
class Sliver(Extendable):
    '''
    Information on the reservation of a particular resource for a slice.
    
    @ivar resource: The resource the sliver is part of.
    @type resource: L{Resource}
    @ivar slice: The slice the slice is part of.
    @type slice: L{Slice}
    '''
    
    resource = models.ForeignKey(
        Resource, verbose_name="Resource this sliver is part of")
    slice = models.ForeignKey(
        Slice, verbose_name="Slice this sliver is part of")
