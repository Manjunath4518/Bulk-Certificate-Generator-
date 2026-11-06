import uuid
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from .forms import CertificateGenerationForm
from .models import CertificateBatch
from .services import read_participants, render_certificates


def home(request):
    form = CertificateGenerationForm()
    return render(request, "generator/home.html", {"form": form})


@require_POST
def generate_certificates(request):
    form = CertificateGenerationForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, "generator/home.html", {"form": form})

    try:
        rows = read_participants(form.cleaned_data["participants"])
        font_file = form.cleaned_data.get("font_file")
        options = {
            "name_x": form.cleaned_data["name_x"],
            "name_y": form.cleaned_data["name_y"],
            "font_size": form.cleaned_data["font_size"],
            "text_color": form.cleaned_data["text_color"],
            "extra_fields": form.cleaned_data["extra_fields"],
        }
        zip_buffer, count = render_certificates(
            form.cleaned_data["template"], rows, options,
            font_path=font_file,
        )
    except (ValueError, UnicodeDecodeError) as exc:
        form.add_error(None, str(exc))
        return render(request, "generator/home.html", {"form": form})

    batch_id = uuid.uuid4().hex
    request.session[f"certificate_batch_{batch_id}"] = {
        "zip": zip_buffer.getvalue().hex(),
        "count": count,
    }
    return render(request, "generator/success.html", {
        "batch_id": batch_id,
        "count": count,
    })


def download_batch(request, batch_id):
    data = request.session.get(f"certificate_batch_{batch_id}")
    if not data:
        raise Http404("This download session has expired. Generate the certificates again.")
    response = HttpResponse(bytes.fromhex(data["zip"]), content_type="application/zip")
    response["Content-Disposition"] = 'attachment; filename="certificates.zip"'
    return response
