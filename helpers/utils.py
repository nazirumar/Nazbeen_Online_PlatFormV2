

from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

def compress_image(image):
    # Open the image using Pillow
    im = Image.open(image)

    # Convert image to RGB if it is in a different mode (e.g., RGBA, P)
    if im.mode in ("RGBA", "P"):
        im = im.convert("RGB")

    # Create a BytesIO object to save the compressed image
    im_io = BytesIO()

    # Save the image to the BytesIO object with a lower quality (default: 85)
    im.save(im_io, format="JPEG", quality=300, optimize=True)

    # Create a new InMemoryUploadedFile object for the compressed image
    new_image = InMemoryUploadedFile(
        im_io,
        "ImageField",
        image.name,
        "image/jpeg",
        sys.getsizeof(im_io),
        None,
    )
    return new_image
