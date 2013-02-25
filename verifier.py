#!/usr/bin/python
# -*- coding: utf8 -*-

import gdata.youtube.service
import urlparse


class Error(Exception):
    pass


class VideoVerifier(object):
    OK = 0
    NOT_READY = 1
    PROBLEM = 2
    REJECTED = 3

    STATUS = {
        OK: 'ok',
        NOT_READY: 'not ready',
        PROBLEM: 'problem',
        REJECTED: 'rejected'
    }

    verifier = None

    def __init__(self, service, video_url=None, video_id=None):
        if service == 'youtube':
            self.verifier = YoutubeVerifier(video_url, video_id)

    def get_video_status(self):
        return self.verifier.get_video_status()

    def get_video_length(self):
        return self.verifier.get_video_length()


class YoutubeVerifier(object):

    video_id = None
    status = None
    entry = None

    def __init__(self, video_url=None, video_id=None):
        self.yt_service = gdata.youtube.service.YouTubeService()
        if video_url:
            self.video_id = self.id_from_url(video_url)
        else:
            self.video_id = video_id

    @staticmethod
    def id_from_url(url):
        if not 'youtube.com' in url:
            raise Error('invalid url')

        parsed = urlparse.urlparse(url)
        video_id = urlparse.parse_qs(parsed.query)['v'][0]

        if video_id:
            return video_id
        else:
            raise Error('video id not found on url')

    def get_video_length(self):
        return self.get_video_entry().media.duration.seconds

    def get_video_entry(self):
        if not self.entry:
            try:
                self.entry = self.yt_service.GetYouTubeVideoEntry(
                    video_id=self.video_id)
            except:
                raise Error('problem fetching video entry')

        return self.entry

    def get_video_status(self):
        try:
            upload_status = self.yt_service.CheckUploadStatus(
                video_id=self.video_id)
        except:
            raise Error('problem checking video status')

        if upload_status:
            upload_status = upload_status[0]
            if upload_status == 'rejected':
                return VideoVerifier.REJECTED

            elif upload_status == 'processing':
                return VideoVerifier.NOT_READY

        return VideoVerifier.OK


# verifier = VideoVerifier(service='youtube', video_url='http://www.youtube.com/watch?v=ICHvZwueL_Q')
# print VideoVerifier.STATUS[verifier.get_video_status()]
# print verifier.get_video_length()
