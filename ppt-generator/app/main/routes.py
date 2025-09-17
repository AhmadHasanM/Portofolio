from flask import Blueprint, request, jsonify, send_file, render_template, current_app
import os
from uuid import uuid4
from datetime import datetime
from .services import generate_slide_content, create_ppt
from pptx import Presentation
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import comtypes.client
import pythoncom

main = Blueprint("main", __name__, template_folder="templates", static_folder="../static")

OUTPUT_DIR = os.path.join(os.getcwd(), "generated_ppts")
TEMPLATE_DIR = os.path.join(os.getcwd(), "app", "templating", "templates")

os.makedirs(OUTPUT_DIR, exist_ok=True)

PRESENTATIONS = []


@main.route("/api/generate_ppt", methods=["POST"])
def generate_ppt():
    data = request.json
    company = data.get("company", "Company")
    contexts = [c for c in [data.get("context1"), data.get("context2"), data.get("context3")] if c]
    aiNews = data.get("aiNews", False)
    companyInsight = data.get("companyInsight", False)
    template = data.get("template", "general")
    slideCount = int(data.get("slideCount", 5))
    branding = data.get("branding", "default")
    prompt = data.get("prompt", "")

    presentation_id = str(uuid4())
    filename = f"{company}_{uuid4()}.pptx".replace(" ", "_")
    filepath = os.path.join(OUTPUT_DIR, filename)

    job = {
        "id": presentation_id,
        "company": company,
        "prompt": prompt,
        "slideCount": slideCount,
        "template": template,
        "branding": branding,
        "filename": filename,
        "download_url": f"/api/download/{filename}",
        "status": "in_queue",
        "created_at": datetime.now().strftime("%b %d, %Y %H:%M:%S")
    }
    PRESENTATIONS.append(job)

    try:
        # --- generate isi slide ---
        slides_content = generate_slide_content(company, contexts, aiNews, companyInsight, slideCount)

        # --- bikin file PPT ---
        create_ppt(slides_content, filepath, template=template, branding=branding)

        job["status"] = "completed"
        job["slides"] = slides_content   # ⬅️ tambahin biar frontend bisa render di tab Generate

        return jsonify(job)

    except Exception as e:
        job["status"] = "error"
        job["error"] = str(e)
        return jsonify(job), 500


@main.route("/api/download/<filename>")
def download_file(filename):
    filepath = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(filepath):
        try:
            return send_file(
                filepath,
                as_attachment=True,
                download_name=filename,
                mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
            )
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    return jsonify({"error": "File not found"}), 404


@main.route("/api/history/<presentation_id>", methods=["DELETE"])
def delete_presentation(presentation_id):
    """
    Hapus PPT dari PRESENTATIONS dan file fisik di folder generated_ppts
    """
    for idx, job in enumerate(PRESENTATIONS):
        if job["id"] == presentation_id:
            filepath = os.path.join(OUTPUT_DIR, job["filename"])
            if os.path.exists(filepath):
                os.remove(filepath)

            PRESENTATIONS.pop(idx)
            return jsonify({"message": "Deleted successfully ✅", "id": presentation_id}), 200

    return jsonify({"error": "Presentation not found"}), 404


@main.route("/api/history", methods=["GET"])
def history():
    return jsonify(PRESENTATIONS[::-1])


@main.route("/api/presentations", methods=["GET"])
def list_presentations():
    return jsonify(PRESENTATIONS)


@main.route("/api/template/<template>")
def preview_template(template):
    template_file = f"{template}_template.pptx"
    filepath = os.path.join(TEMPLATE_DIR, template_file)

    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=False, download_name=template_file)
    return jsonify({"error": f"Template {template} not found"}), 404


@main.route("/api/template/<template>/slides")
def template_slides(template):
    base_dir = os.path.join(current_app.static_folder, "templates", "previews", template)

    if not os.path.exists(base_dir):
        return jsonify({"error": f"Template {template} not found", "path": base_dir}), 404

    slides = [f for f in os.listdir(base_dir) if f.lower().endswith((".png", ".jpg", ".jpeg"))]
    slides.sort(key=lambda x: int(''.join(filter(str.isdigit, x)) or 0))

    return jsonify({
        "template": template,
        "count": len(slides),
        "slides": [f"/static/templates/previews/{template}/{s}" for s in slides]
    })

@main.route("/api/convert_pdf/<filename>")
def convert_pdf(filename):
    pptx_path = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(pptx_path):
        return jsonify({"error": "File not found"}), 404

    pdf_filename = filename.replace(".pptx", ".pdf")
    pdf_path = os.path.join(OUTPUT_DIR, pdf_filename)

    try:
        # ✅ Inisialisasi COM
        pythoncom.CoInitialize()

        powerpoint = comtypes.client.CreateObject("Powerpoint.Application")
        powerpoint.Visible = 1

        presentation = powerpoint.Presentations.Open(pptx_path)
        presentation.SaveAs(pdf_path, 32)  # 32 = PDF
        presentation.Close()
        powerpoint.Quit()

        pythoncom.CoUninitialize()

        return send_file(pdf_path, as_attachment=True, download_name=pdf_filename, mimetype="application/pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@main.route("/api/view/<filename>")
def view_ppt(filename):
    """
    Return PPTX file inline (untuk ditampilkan di popup/iframe).
    """
    filepath = os.path.join(OUTPUT_DIR, filename)
    if not os.path.exists(filepath):
        return jsonify({"error": "File not found"}), 404

    try:
        return send_file(
            filepath,
            as_attachment=False,
            download_name=filename,
            mimetype="application/vnd.openxmlformats-officedocument.presentationml.presentation"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@main.route("/")
def home():
    return render_template("index.html")
