import io
from pathlib import Path
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

from docx import Document
from docx.shared import Inches

from app.core.database import get_supabase_service_client


class ExportService:
    """Handle resume export to PDF and DOCX formats"""
    
    def __init__(self):
        self.templates_dir = Path(__file__).parent / "templates"
    
    async def export_resume(self, resume_id: str, format: str) -> tuple[bytes, str, str]:
        """Export resume in specified format"""
        
        # Get resume data from database
        supabase = get_supabase_service_client()
        result = supabase.table("resumes").select("*").eq("id", resume_id).execute()
        
        if not result.data:
            raise ValueError(f"Resume {resume_id} not found")
        
        resume_record = result.data[0]
        # Use optimized data if available, otherwise fall back to parsed data
        resume_data = resume_record.get("optimized_data") or resume_record["parsed_data"]
        
        if format == "pdf":
            return await self._generate_pdf(resume_data, resume_id)
        elif format == "docx":
            return await self._generate_docx(resume_data, resume_id)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    async def _generate_pdf(self, resume_data: dict, resume_id: str) -> tuple[bytes, str, str]:
        """Generate ATS-compliant PDF using ReportLab"""
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
        styles = getSampleStyleSheet()
        
        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            spaceAfter=12,
            alignment=1  # Center alignment
        )
        
        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            spaceAfter=6,
            spaceBefore=12
        )
        
        story = []
        personal = resume_data["personal_info"]
        
        # Name
        story.append(Paragraph(personal["name"], title_style))
        
        # Contact info
        contact_info = []
        if personal.get("email"):
            contact_info.append(personal["email"])
        if personal.get("phone"):
            contact_info.append(personal["phone"])
        if personal.get("location"):
            contact_info.append(personal["location"])
        
        if contact_info:
            story.append(Paragraph(" | ".join(contact_info), styles['Normal']))
            story.append(Spacer(1, 12))
        
        # Experience
        if resume_data.get("experience"):
            story.append(Paragraph("Experience", heading_style))
            for exp in resume_data["experience"]:
                title_company = f"<b>{exp['title']} - {exp['company']}</b>"
                story.append(Paragraph(title_company, styles['Normal']))
                story.append(Paragraph(f"<i>{exp['duration']}</i>", styles['Normal']))
                for desc in exp["description"]:
                    story.append(Paragraph(f"• {desc}", styles['Normal']))
                story.append(Spacer(1, 6))
        
        # Skills
        if resume_data.get("skills"):
            story.append(Paragraph("Skills", heading_style))
            skills = resume_data["skills"]
            if skills.get("technical"):
                tech_skills = f"<b>Technical:</b> {', '.join(skills['technical'])}"
                story.append(Paragraph(tech_skills, styles['Normal']))
            if skills.get("frameworks"):
                frameworks = f"<b>Frameworks:</b> {', '.join(skills['frameworks'])}"
                story.append(Paragraph(frameworks, styles['Normal']))
            if skills.get("tools"):
                tools = f"<b>Tools:</b> {', '.join(skills['tools'])}"
                story.append(Paragraph(tools, styles['Normal']))
            story.append(Spacer(1, 6))
        
        # Projects
        if resume_data.get("projects"):
            story.append(Paragraph("Projects", heading_style))
            for project in resume_data["projects"]:
                story.append(Paragraph(f"<b>{project['name']}</b>", styles['Normal']))
                story.append(Paragraph(project['description'], styles['Normal']))
                if project.get("technologies"):
                    tech_list = f"<b>Technologies:</b> {', '.join(project['technologies'])}"
                    story.append(Paragraph(tech_list, styles['Normal']))
                story.append(Spacer(1, 6))
        
        # Education
        if resume_data.get("education"):
            story.append(Paragraph("Education", heading_style))
            for edu in resume_data["education"]:
                story.append(Paragraph(f"<b>{edu['degree']}</b>", styles['Normal']))
                edu_info = edu['institution']
                if edu.get("graduation_year"):
                    edu_info += f" | {edu['graduation_year']}"
                if edu.get("gpa"):
                    edu_info += f" | GPA: {edu['gpa']}"
                story.append(Paragraph(edu_info, styles['Normal']))
        
        doc.build(story)
        pdf_bytes = buffer.getvalue()
        buffer.close()
        
        filename = f"{personal['name'].replace(' ', '_')}_resume.pdf"
        return pdf_bytes, "application/pdf", filename
        
        filename = f"{resume_data['personal_info']['name'].replace(' ', '_')}_resume.pdf"
        return pdf_bytes, "application/pdf", filename
    
    async def _generate_docx(self, resume_data: dict, resume_id: str) -> tuple[bytes, str, str]:
        """Generate ATS-compliant DOCX using python-docx"""
        
        doc = Document()
        
        # Personal Info
        personal = resume_data["personal_info"]
        doc.add_heading(personal["name"], 0)
        
        contact_info = []
        if personal.get("email"):
            contact_info.append(personal["email"])
        if personal.get("phone"):
            contact_info.append(personal["phone"])
        if personal.get("location"):
            contact_info.append(personal["location"])
        
        if contact_info:
            doc.add_paragraph(" | ".join(contact_info))
        
        # Experience
        if resume_data.get("experience"):
            doc.add_heading("Experience", 1)
            for exp in resume_data["experience"]:
                p = doc.add_paragraph()
                p.add_run(f"{exp['title']} - {exp['company']}").bold = True
                doc.add_paragraph(exp["duration"])
                for desc in exp["description"]:
                    doc.add_paragraph(f"• {desc}")
        
        # Skills
        if resume_data.get("skills"):
            doc.add_heading("Skills", 1)
            skills = resume_data["skills"]
            if skills.get("technical"):
                doc.add_paragraph(f"Technical: {', '.join(skills['technical'])}")
            if skills.get("frameworks"):
                doc.add_paragraph(f"Frameworks: {', '.join(skills['frameworks'])}")
        
        # Projects
        if resume_data.get("projects"):
            doc.add_heading("Projects", 1)
            for project in resume_data["projects"]:
                p = doc.add_paragraph()
                p.add_run(project["name"]).bold = True
                doc.add_paragraph(project["description"])
                if project.get("technologies"):
                    doc.add_paragraph(f"Technologies: {', '.join(project['technologies'])}")
        
        # Education
        if resume_data.get("education"):
            doc.add_heading("Education", 1)
            for edu in resume_data["education"]:
                if edu.get("degree") and edu.get("institution"):
                    doc.add_paragraph(f"{edu['degree']} - {edu['institution']}")
        
        # Save to bytes
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        filename = f"{personal['name'].replace(' ', '_')}_resume.docx"
        content_type = "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        return buffer.getvalue(), content_type, filename
    
    def _build_html(self, resume_data: dict) -> str:
        """Build HTML content for PDF generation with inline CSS"""
        
        personal = resume_data["personal_info"]
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{personal['name']} - Resume</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    font-size: 11pt;
                    line-height: 1.4;
                    margin: 0.5in;
                    color: #000;
                }}
                .resume {{
                    max-width: 8.5in;
                }}
                header {{
                    text-align: center;
                    margin-bottom: 20pt;
                }}
                h1 {{
                    font-size: 18pt;
                    font-weight: bold;
                    margin: 0 0 8pt 0;
                }}
                h2 {{
                    font-size: 14pt;
                    font-weight: bold;
                    margin: 16pt 0 8pt 0;
                    border-bottom: 1pt solid #000;
                }}
                h3 {{
                    font-size: 12pt;
                    font-weight: bold;
                    margin: 12pt 0 4pt 0;
                }}
                .contact {{
                    font-size: 10pt;
                    margin-bottom: 8pt;
                }}
                .duration {{
                    font-style: italic;
                    margin: 0 0 8pt 0;
                }}
                ul {{
                    margin: 8pt 0;
                    padding-left: 20pt;
                }}
                li {{
                    margin-bottom: 4pt;
                }}
                section {{
                    margin-bottom: 16pt;
                }}
                .job, .project {{
                    margin-bottom: 12pt;
                }}
            </style>
        </head>
        <body>
            <div class="resume">
                <header>
                    <h1>{personal['name']}</h1>
                    <div class="contact">
        """
        
        contact_info = []
        if personal.get("email"):
            contact_info.append(personal["email"])
        if personal.get("phone"):
            contact_info.append(personal["phone"])
        if personal.get("location"):
            contact_info.append(personal["location"])
        
        html += " | ".join(contact_info)
        html += """
                    </div>
                </header>
        """
        
        # Experience
        if resume_data.get("experience"):
            html += "<section><h2>Experience</h2>"
            for exp in resume_data["experience"]:
                html += f"""
                <div class="job">
                    <h3>{exp['title']} - {exp['company']}</h3>
                    <p class="duration">{exp['duration']}</p>
                    <ul>
                """
                for desc in exp["description"]:
                    html += f"<li>{desc}</li>"
                html += "</ul></div>"
            html += "</section>"
        
        # Skills
        if resume_data.get("skills"):
            html += "<section><h2>Skills</h2>"
            skills = resume_data["skills"]
            if skills.get("technical"):
                html += f"<p><strong>Technical:</strong> {', '.join(skills['technical'])}</p>"
            if skills.get("frameworks"):
                html += f"<p><strong>Frameworks:</strong> {', '.join(skills['frameworks'])}</p>"
            html += "</section>"
        
        # Projects
        if resume_data.get("projects"):
            html += "<section><h2>Projects</h2>"
            for project in resume_data["projects"]:
                html += f"""
                <div class="project">
                    <h3>{project['name']}</h3>
                    <p>{project['description']}</p>
                """
                if project.get("technologies"):
                    tech_str = f"<strong>Technologies:</strong> {', '.join(project['technologies'])}"
                    html += f"<p>{tech_str}</p>"
                html += "</div>"
            html += "</section>"
        
        # Education
        if resume_data.get("education"):
            html += "<section><h2>Education</h2>"
            for edu in resume_data["education"]:
                if edu.get("degree") and edu.get("institution"):
                    html += f"<p>{edu['degree']} - {edu['institution']}"
                    if edu.get("graduation_year"):
                        html += f" ({edu['graduation_year']})"
                    html += "</p>"
            html += "</section>"
        
        html += """
            </div>
        </body>
        </html>
        """
        
        return html
    
    def _build_printable_html(self, resume_data: dict) -> str:
        """Build HTML optimized for browser PDF printing"""
        
        personal = resume_data["personal_info"]
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{personal['name']} - Resume</title>
            <style>
                @media print {{
                    body {{ margin: 0.5in; }}
                    .no-print {{ display: none; }}
                }}
                body {{ 
                    font-family: Arial, sans-serif; 
                    font-size: 11pt; 
                    line-height: 1.4;
                    margin: 0.5in;
                    color: #000;
                }}
                h1 {{ 
                    font-size: 18pt; 
                    margin-bottom: 10pt; 
                    border-bottom: 2pt solid #000;
                    padding-bottom: 5pt;
                }}
                h2 {{ 
                    font-size: 14pt; 
                    margin: 15pt 0 8pt 0; 
                    color: #333;
                }}
                h3 {{ 
                    font-size: 12pt; 
                    margin: 10pt 0 5pt 0; 
                    font-weight: bold;
                }}
                p {{ margin: 5pt 0; }}
                ul {{ margin: 5pt 0; padding-left: 20pt; }}
                li {{ margin-bottom: 3pt; }}
                .contact {{ 
                    font-size: 10pt; 
                    margin-bottom: 15pt; 
                    color: #666;
                }}
                .duration {{ 
                    font-style: italic; 
                    color: #666; 
                    margin-bottom: 5pt;
                }}
                .print-instruction {{
                    background: #f0f0f0;
                    padding: 10pt;
                    margin-bottom: 20pt;
                    border-left: 4pt solid #007acc;
                }}
            </style>
        </head>
        <body>
            <div class="print-instruction no-print">
                <strong>To save as PDF:</strong> Use your browser's Print function (Ctrl+P) 
                and select "Save as PDF"
            </div>
            
            <h1>{personal['name']}</h1>
            <div class="contact">
        """
        
        contact_info = []
        if personal.get("email"):
            contact_info.append(personal["email"])
        if personal.get("phone"):
            contact_info.append(personal["phone"])
        if personal.get("location"):
            contact_info.append(personal["location"])
        if personal.get("github"):
            contact_info.append(f"GitHub: {personal['github']}")
        if personal.get("linkedin"):
            contact_info.append(f"LinkedIn: {personal['linkedin']}")
        
        html += " | ".join(contact_info) + "</div>"
        
        # Experience
        if resume_data.get("experience"):
            html += "<h2>Experience</h2>"
            for exp in resume_data["experience"]:
                html += f"<h3>{exp['title']} - {exp['company']}</h3>"
                html += f"<div class='duration'>{exp['duration']}</div>"
                html += "<ul>"
                for desc in exp["description"]:
                    html += f"<li>{desc}</li>"
                html += "</ul>"
        
        # Skills
        if resume_data.get("skills"):
            html += "<h2>Skills</h2>"
            skills = resume_data["skills"]
            if skills.get("technical"):
                html += f"<p><strong>Technical:</strong> {', '.join(skills['technical'])}</p>"
            if skills.get("frameworks"):
                html += f"<p><strong>Frameworks:</strong> {', '.join(skills['frameworks'])}</p>"
            if skills.get("tools"):
                html += f"<p><strong>Tools:</strong> {', '.join(skills['tools'])}</p>"
        
        # Projects
        if resume_data.get("projects"):
            html += "<h2>Projects</h2>"
            for project in resume_data["projects"]:
                html += f"<h3>{project['name']}</h3>"
                html += f"<p>{project['description']}</p>"
                if project.get("technologies"):
                    html += f"<p><strong>Technologies:</strong> {', '.join(project['technologies'])}</p>"
        
        # Education
        if resume_data.get("education"):
            html += "<h2>Education</h2>"
            for edu in resume_data["education"]:
                html += f"<h3>{edu['degree']}</h3>"
                html += f"<p>{edu['institution']}"
                if edu.get("graduation_year"):
                    html += f" | {edu['graduation_year']}"
                if edu.get("gpa"):
                    html += f" | GPA: {edu['gpa']}"
                html += "</p>"
        
        html += """
        </body>
        </html>
        """
        
        return html

    def _build_simple_html(self, resume_data: dict) -> str:
        """Build minimal HTML content as fallback for WeasyPrint issues"""
        
        personal = resume_data["personal_info"]
        
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>{personal['name']} - Resume</title>
            <style>
                body {{ font-family: Arial, sans-serif; font-size: 11pt; margin: 0.5in; }}
                h1 {{ font-size: 18pt; margin-bottom: 10pt; }}
                h2 {{ font-size: 14pt; margin: 15pt 0 8pt 0; }}
                h3 {{ font-size: 12pt; margin: 10pt 0 5pt 0; }}
                p {{ margin: 5pt 0; }}
                ul {{ margin: 5pt 0; padding-left: 20pt; }}
            </style>
        </head>
        <body>
            <h1>{personal['name']}</h1>
            <p>
        """
        
        contact_info = []
        if personal.get("email"):
            contact_info.append(personal["email"])
        if personal.get("phone"):
            contact_info.append(personal["phone"])
        if personal.get("location"):
            contact_info.append(personal["location"])
        
        html += " | ".join(contact_info) + "</p>"
        
        # Experience
        if resume_data.get("experience"):
            html += "<h2>Experience</h2>"
            for exp in resume_data["experience"]:
                html += f"<h3>{exp['title']} - {exp['company']}</h3>"
                html += f"<p><em>{exp['duration']}</em></p>"
                html += "<ul>"
                for desc in exp["description"]:
                    html += f"<li>{desc}</li>"
                html += "</ul>"
        
        # Skills
        if resume_data.get("skills"):
            html += "<h2>Skills</h2>"
            skills = resume_data["skills"]
            if skills.get("technical"):
                html += f"<p><strong>Technical:</strong> {', '.join(skills['technical'])}</p>"
            if skills.get("frameworks"):
                html += f"<p><strong>Frameworks:</strong> {', '.join(skills['frameworks'])}</p>"
        
        # Projects
        if resume_data.get("projects"):
            html += "<h2>Projects</h2>"
            for project in resume_data["projects"]:
                html += f"<h3>{project['name']}</h3>"
                html += f"<p>{project['description']}</p>"
                if project.get("technologies"):
                    html += f"<p><strong>Technologies:</strong> {', '.join(project['technologies'])}</p>"
        
        # Education
        if resume_data.get("education"):
            html += "<h2>Education</h2>"
            for edu in resume_data["education"]:
                if edu.get("degree") and edu.get("institution"):
                    html += f"<p>{edu['degree']} - {edu['institution']}"
                    if edu.get("graduation_year"):
                        html += f" ({edu['graduation_year']})"
                    html += "</p>"
        
        html += "</body></html>"
        return html


export_service = ExportService()