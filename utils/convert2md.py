def json2md(data, level=1):
    md = ""

    if isinstance(data, dict):

        for key, value in data.items():

            md += "#" * level + f" {key}\n\n"

            md += json2md(value, level + 1)


    elif isinstance(data, list):

        for item in data:

            if isinstance(item, (dict, list)):

                md += json2md(item, level)

            else:

                md += f"- {item}\n"

    
    else:
        md += f"{data}\n\n"

    return md