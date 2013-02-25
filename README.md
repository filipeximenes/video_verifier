## About

This project aims to make it easy to verify and access video data from different video servides


## Supported Services

* Youtube

## Dependencies:

gdata

You can install gdata using pip:
```
$ pip install gdata
```

## Usage
```
verifier = VideoVerifier(service='youtube', video_id='ICHvZwueL_Q')
print VideoVerifier.STATUS[verifier.get_video_status()]
print verifier.get_video_length()
```

OR

```
verifier = VideoVerifier(service='youtube', video_url='http://www.youtube.com/watch?v=ICHvZwueL_Q')
print VideoVerifier.STATUS[verifier.get_video_status()]
print verifier.get_video_length()
```

## Contributions

Contrubitions are very welcome, just post a pull request.