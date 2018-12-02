#!/usr/bin/env bash

# resize pngs
mogrify -resize 16x -quality 90 -path ./16/logo/ ./originals/tags/*.png
mogrify -resize 32x -quality 90 -path ./32/logo/ ./originals/tags/*.png
mogrify -resize 48x -quality 90 -path ./48/logo/ ./originals/tags/*.png
mogrify -resize 96x -quality 90 -path ./96/logo/ ./originals/tags/*.png
# resize and convert to png
mogrify -resize 16x -quality 90 -path ./16/logo/ -background none -format png ./originals/logo/*.svg
mogrify -resize 32x -quality 90 -path ./32/logo/ -background none -format png ./originals/logo/*.svg
mogrify -resize 48x -quality 90 -path ./48/logo/ -background none -format png ./originals/logo/*.svg
mogrify -resize 96x -quality 90 -path ./96/logo/ -background none -format png ./originals/logo/*.svg
