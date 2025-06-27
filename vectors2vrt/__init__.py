import contextlib
from xml.etree import ElementTree

import click
from osgeo import ogr

# suppress an warning about numpy not being installed
with contextlib.redirect_stderr(None):
    ogr.DontUseExceptions()


def create_vrt_from_vector(input_files):
    """
    Creates a VRT file from multiple vector files, considering multiple layers within vector files.

    Parameters:
        input_files (list): List of paths to input vector files.
        output_vrt (str): Path to the output VRT file or '-' for stdout.
    """
    # Create the root element for the VRT XML

    vrt_root = ElementTree.Element("OGRVRTDataSource")

    for input_file in input_files:
        # Open the vector file to identify layers
        data_source = ogr.Open(input_file)
        if not data_source:
            raise click.UsageError(
                f"Failed to open input file '{input_file}'. Are you sure it's a GIS vector file?"
            )

        is_csv = data_source.GetDriver().GetName() == "CSV"

        # Add each layer to the VRT
        for layer_index in range(data_source.GetLayerCount()):
            layer = data_source.GetLayerByIndex(layer_index)
            layer_name = layer.GetName()

            # Create an OGRVRTLayer element
            layer_element = ElementTree.SubElement(
                vrt_root, "OGRVRTLayer", name=layer_name
            )

            # Add SrcDataSource and SrcLayer elements
            src_data_source = ElementTree.SubElement(layer_element, "SrcDataSource")
            src_data_source.text = input_file

            src_layer = ElementTree.SubElement(layer_element, "SrcLayer")
            src_layer.text = layer_name

            if is_csv:
                layer_defn = layer.GetLayerDefn()
                field_names = [
                    layer_defn.GetFieldDefn(i).GetName()
                    for i in range(layer_defn.GetFieldCount())
                ]

                has_lng = "lng" in field_names
                has_lat = "lat" in field_names

                if has_lng and has_lat:
                    ElementTree.SubElement(
                        layer_element,
                        "GeometryField",
                        encoding="PointFromColumns",
                        x="lng",
                        y="lat",
                    )
                else:
                    click.echo(
                        f"Warning: CSV file '{input_file}' (layer '{layer_name}') was recognized by OGR as a CSV but does not contain both 'lng' and 'lat' fields. Omitting GeometryField.",
                        err=True,
                    )

    # Write the VRT content
    tree = ElementTree.ElementTree(vrt_root)

    return tree


def validate_input(ctx, param, input_files):
    if not input_files:
        raise click.BadParameter(
            "At least one input file must be specified.", ctx=ctx, param=param
        )

    return input_files


@click.command()
@click.argument(
    "input_files", nargs=-1, type=click.Path(exists=True), callback=validate_input
)
@click.option(
    "-o",
    "--output",
    required=True,
    type=str,  # Allow '-' for stdout
    help="Path to the output VRT file or '-' to write to stdout",
)
def main(input_files, output):
    """Create a VRT file from vector inputs. Will pick up latitude and longitude columns from CSV files if and only if the field names are labeled "lat" and "lng".

    \b
    example:
       vectors2vrt A.geojson B.sqlite -o output.vrt
    """

    vrt_tree = create_vrt_from_vector(input_files)
    ElementTree.indent(vrt_tree)
    vrt_string = ElementTree.tostring(vrt_tree.getroot(), encoding="unicode")

    if output == "-":
        click.echo(vrt_string)
    else:
        with open(output, "w") as vrt_file:
            vrt_file.write(vrt_string)


if __name__ == "__main__":
    main()
