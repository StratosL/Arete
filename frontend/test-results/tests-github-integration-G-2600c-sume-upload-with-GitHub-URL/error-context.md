# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - generic [ref=e5]:
      - generic [ref=e6]:
        - heading "Arete" [level=1] [ref=e7]
        - paragraph [ref=e8]: AI-Powered Resume Optimizer
      - button "Toggle theme" [ref=e10] [cursor=pointer]:
        - img [ref=e11]
        - img
        - generic [ref=e17]: Toggle theme
  - main [ref=e18]:
    - generic [ref=e20]:
      - generic [ref=e21]:
        - heading "Upload Your Resume" [level=2] [ref=e22]
        - paragraph [ref=e23]: Upload your resume to get started with AI-powered optimization
      - generic [ref=e24]:
        - button "Choose File" [ref=e25] [cursor=pointer]
        - generic [ref=e26]:
          - generic [ref=e27]:
            - img [ref=e28]
            - generic [ref=e31]: test-resume.txt
          - paragraph [ref=e32]: Supports PDF, DOCX, and TXT files (max 10MB)
      - generic [ref=e33]:
        - generic [ref=e34]:
          - img [ref=e35]
          - generic [ref=e38]: GitHub Profile (Optional)
        - textbox "https://github.com/username" [ref=e39]: https://github.com/octocat
        - paragraph [ref=e40]: Include your GitHub profile for enhanced project analysis
      - paragraph [ref=e42]: "Failed to parse resume: 1 validation error for ResumeData personal_info.email Input should be a valid string [type=string_type, input_value=None, input_type=NoneType] For further information visit https://errors.pydantic.dev/2.9/v/string_type"
      - button "Upload & Parse Resume" [ref=e43] [cursor=pointer]
  - contentinfo [ref=e44]:
    - paragraph [ref=e46]: Arete - Transforming resumes with AI for tech professionals
```