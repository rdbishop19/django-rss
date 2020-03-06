from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
# Create your views here.
from rssfeed.models import Feed
from .rss_aggregator import RssAggregator
from rest_framework.decorators import action
import time

class FeedSerializer(serializers.HyperlinkedModelSerializer):
    '''
        JSON serializer for RSS Feed

        Arguments:
            serializers.HyperLinkedModelSerializer
    '''

    class Meta:
        model = Feed
        url = serializers.HyperlinkedIdentityField(
            view_name='feed',
            lookup_field='id',
        )

        fields = '__all__'


class Feeds(viewsets.ModelViewSet):
    '''Feeds view for Django-RSS'''

    queryset = Feed.objects.all()
    serializer_class = FeedSerializer

    def create(self, request, *args, **kwargs):
        '''Handle POST

        Returns:
            Response == JSON serialized Feed instance
        '''
        obj, created = Feed.objects.get_or_create(**request.data)
        if obj:
            serializer = FeedSerializer(obj, context={'request': request})
        else:
            serializer = FeedSerializer(created, context={'request': request})
        return Response(serializer.data)

    @action(methods=['get'], detail=False)
    def refresh(self, request):
        rss_object = RssAggregator('https://dev.to/feed')
        newfeed = rss_object.parse()

        entries = []
        for feedentry in newfeed.entries:
            new_entry = Feed()
            date = feedentry.get('published_parsed', '')
            iso_date = time.strftime('%Y-%m-%dT%H:%M:%SZ', date)
            new_entry.pub_date = iso_date
            new_entry.title = feedentry.get('title', '')
            new_entry.link = feedentry.get('link','')
            new_entry.description = feedentry.get('description','')
            entries.append(new_entry)
        new_items = Feed.objects.bulk_create(entries)
        serializer = FeedSerializer(new_items, context={'request': request}, many=True)
        return Response(serializer.data)
