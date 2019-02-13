# ImageToBraille (Python 3)

Converts an image to Braille Unicode art

## Running

```
python3 main.py IMAGE_FILE [-s SCALE_FACTOR -t LIGHTNESS_THRESHOLD -i]
```

The `SCALE_FACTOR` argument will pre-scale the image before it is converted. Values less than `1.0` will shrink the image, and values larger than `1.0` will enlarge the image.

The `LIGHTNESS_THRESHOLD` determines when a pixel should be given a dot or not. If the grayness value of the pixel is LESS than `LIGHTNESS_THRESHOLD`, then the pixel is too dark and the pixel will have no dot. Otherwise, that pixel will receive a dot.

The `-i` argument will invert the input before converting to Braille. This is useful for dark background with light text and vice versa.
