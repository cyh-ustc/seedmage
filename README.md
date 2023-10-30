# SeedMage

## Docker

require **python3.12**

```
docker build -t seedmage .
```

## Torrents Directory Usage

require **python3.12**

The default torrents directory is `TORRENTS`

```
python main.py
```

## Single Torrent Usage (Old)

```

usage: seedmage.py [-h] [--update-interval UPDATE_INTERVAL]
                   torrent_file upload_speed

positional arguments:
  torrent_file          example.torrent
  upload_speed          Upload speed in kB/s

optional arguments:
  -h, --help            show this help message and exit
  --update-interval UPDATE_INTERVAL
                        Upload interval in seconds
```


## Todo

* multiple torrents [*]
* dockerfile [*]
* gracefully shutdown []
* watch torrent dir change []
* web admin page []