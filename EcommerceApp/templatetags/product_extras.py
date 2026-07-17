# EcommerceApp/templatetags/product_extras.py

from django import template

register = template.Library()

@register.filter
def get_images(product):
    """Return a list of all available product images."""
    images = [product.product_image]
    if product.image1:
        images.append(product.image1)
    if product.image2:
        images.append(product.image2)
    if product.image3:
        images.append(product.image3)
    return images

# EcommerceApp/templatetags/product_extras.py

@register.filter
def multiply(value, arg):
    return value * arg

