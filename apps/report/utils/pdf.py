from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.http import HttpResponse

def render_to_pdf(template_src, context_dict={}):
    """
    Converts an HTML template into a PDF byte string.

    Args:
        template_src (str): Path to the HTML template file.
        context_dict (dict, optional): Dictionary of context data to render in the template.

    Returns:
        bytes or None: Returns PDF as bytes if successful, otherwise None.
    """
    # Load the template and render it with context data

    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    # Return PDF bytes if no errors occurred

    if not pdf.err:
        return result.getvalue()
    return None

def pdf_response(pdf_bytes, filename):
    """
    Returns an HttpResponse to send the PDF file to the user as a download.
    Args:
        pdf_bytes (bytes): PDF content as bytes.
        filename (str): The filename that will appear for download.
    Returns:
        HttpResponse: Django HTTP response with PDF content.
    """
    response = HttpResponse(pdf_bytes, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response
