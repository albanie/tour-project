###Cycling Project Tools

This repository contains tools for video analysis of Tour de France footage. 

* `distances` contains code for determining whether or not video frames contain useful distance information.
* `faces` makes use of the [dlib](http://dlib.net/) library to detect cyclist faces.
* `gradients` holds functions for extracting the gradients of Tour de France stages.
* `ocr` holds functions for automating the process of reading the "km to go" sign in the top left of the video.
* `snapshots` uses `ffmpeg` to take clusters of snapshots from video footage, then uses spectral analysis to select the sharpest images.

Example API use is given in the `notebooks` directory.