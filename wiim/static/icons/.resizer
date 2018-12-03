#!/usr/bin/env bash

# resize pngs
mogrify -resize 16x -quality 90 -path ./16/ ./originals/tags/*.png
mogrify -resize 32x -quality 90 -path ./32/ ./originals/tags/*.png
mogrify -resize 48x -quality 90 -path ./48/ ./originals/tags/*.png
mogrify -resize 96x -quality 90 -path ./96/ ./originals/tags/*.png
# resize and convert to png
mogrify -resize 16x -quality 90 -path ./16/ -background none -format png ./originals/logo/*.svg
mogrify -resize 32x -quality 90 -path ./32/ -background none -format png ./originals/logo/*.svg
mogrify -resize 48x -quality 90 -path ./48/ -background none -format png ./originals/logo/*.svg
mogrify -resize 96x -quality 90 -path ./96/ -background none -format png ./originals/logo/*.svg
