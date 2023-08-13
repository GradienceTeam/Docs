"""
    hig_www.hig_palette
    ~~~~~~~~~~~~~~~~~~~

    Access properties of GNOME's HIG palette via rST roles.
"""

from urllib.parse import urljoin
import base64

from docutils.utils import unescape
from docutils import nodes
from sphinx.errors import ExtensionError

# Name of this extension
extname = "hig_palette"
# The variable in conf.py that maps color names to (R, G, B) tuples
colors_var = "hig_palette_colors_rgb"
# This can be used within the CSS to apply styles to the resulting image
svg_class_name = "hig-palette-swatch"

"""
Creates an SVG containing a rect, filled with the RGB tuple passed in.
"""
def create_palette_svg_str(rgb):
    return """
    <svg width="100%%" height="100%%"
        xmlns="http://www.w3.org/2000/svg"
        xmlns:xlink="http://www.w3.org/1999/xlink">

    <rect width="100%%" height="100%%" fill="rgb%s" />
    </svg>
    """ % rgb.__str__()

def create_rgb_node(rgb):
    output = rgb.__str__()
    return nodes.Text(output, output)

def create_hex_node(rgb):
    red, green, blue = rgb
    output = f"#{red:02x}{green:02x}{blue:02x}"
    return nodes.Text(output, output)

def create_svg_node(rgb, name):
    svg_str = create_palette_svg_str(rgb)
    svg_base64_str = base64.b64encode(svg_str.encode("ascii"))
    uri = f"data:image/svg+xml;base64,{svg_base64_str.decode('ascii')}"

    node = nodes.image(svg_str)
    node["uri"] = uri

    node.set_class(svg_class_name)
    node["alt"] = f"Color '{name}' from the GNOME HIG palette"

    return node

"""
Creates a role function that can be registered with Sphinx.
"""
def make_palette_role(color_mappings, representation):
    valid_representations = ["rgb", "hex", "svg"]

    if not representation in valid_representations:
        raise ExtensionError("Cannot generate representation '%s' for colors"
            % representation, modname=extname)

    def role(type, rawtext, text, lineno, inliner, options={}, content={}):
        color_name = unescape(text)

        if not color_name in color_mappings:
            raise ExtensionError(
                "Definition for color '%s' not found in conf.py" % color_name,
                modname=extname)

        color_rgb = color_mappings[color_name]
        node = None

        if representation == "rgb":
            node = create_rgb_node(color_rgb)
        elif representation == "hex":
            node = create_hex_node(color_rgb)
        elif representation == "svg":
            node = create_svg_node(color_rgb, color_name)

        return [node], []

    return role

def setup_palette_roles(app):
    color_mappings = app.config[colors_var]

    # returns a text node with a tuple (R, G, B) representing a defined color
    app.add_role("palette-rgb", make_palette_role(color_mappings, "rgb"))
    # returns a text node with the hexadecimal representation of a defined color
    app.add_role("palette-hex", make_palette_role(color_mappings, "hex"))
    # returns an image node set to an SVG from create_palette_svg()
    app.add_role("palette-svg", make_palette_role(color_mappings, "svg"))

def setup(app):
    app.add_config_value(colors_var, {}, "env")
    app.connect("builder-inited", setup_palette_roles)

    return {
        "version": "0.1",
        "parallel_read_safe": True,
        "parellel_write_safe": True
    }
