import os
import json
import re
import base64
import io
from typing import Dict, Any, Optional, List
from config import Config
import numpy as np
from wordcloud import WordCloud
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt

# Import AI providers based on configuration
if Config.AI_PROVIDER == 'gemini':
    try:
        import google.generativeai as genai
        if Config.GEMINI_API_KEY:
            genai.configure(api_key=Config.GEMINI_API_KEY)
    except ImportError:
        print("google-generativeai not installed. Install with: pip install google-generativeai")
elif Config.AI_PROVIDER == 'groq':
    try:
        from groq import Groq
    except ImportError:
        print("groq not installed. Install with: pip install groq")

class DocumentAnalyzer:
    """Analyzes documents and generates dashboard JSON"""
    
    def __init__(self):
        self.ai_provider = Config.AI_PROVIDER
        self.model = None
        
        if self.ai_provider == 'groq':
            if Config.GROQ_API_KEY:
                try:
                    from groq import Groq
                    self.client = Groq(api_key=Config.GROQ_API_KEY)
                    self.model = 'groq'
                    print(f"✓ Using Groq API with model: {Config.GROQ_MODEL}")
                except Exception as e:
                    print(f"Failed to initialize Groq: {e}")
                    print("Get your free API key from: https://console.groq.com")
            else:
                print("⚠ GROQ_API_KEY not set. Using fallback analysis.")
                print("Get your free API key from: https://console.groq.com")
                
        elif self.ai_provider == 'gemini' and Config.GEMINI_API_KEY:
            try:
                import google.generativeai as genai
                self.model = genai.GenerativeModel('gemini-pro')
                print("✓ Using Google Gemini")
            except Exception as e:
                print(f"Failed to initialize Gemini: {e}")
    
    def extract_text(self, file_path: str) -> str:
        """Extract text from uploaded file"""
        ext = file_path.lower().split('.')[-1]
        
        if ext == 'txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        elif ext == 'pdf':
            try:
                import PyPDF2
                text = ""
                with open(file_path, 'rb') as f:
                    pdf_reader = PyPDF2.PdfReader(f)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
                return text
            except Exception as e:
                return f"Error extracting PDF: {e}"
        
        elif ext in ['docx', 'doc']:
            try:
                import docx
                doc = docx.Document(file_path)
                return "\n".join([para.text for para in doc.paragraphs])
            except Exception as e:
                return f"Error extracting DOCX: {e}"
        
        return ""
    
    def analyze_document(self, file_path: str, custom_prompt: str = "", summary_length: str = "Standard") -> Dict[str, Any]:
        """Analyze document and return dashboard JSON"""
        
        # Extract text
        text = self.extract_text(file_path)
        
        if not text or len(text.strip()) < 100:
            return self._generate_error_response("Document too short or empty")
        
        # Use AI if available
        if self.model:
            if self.ai_provider == 'groq':
                return self._analyze_with_groq(text, custom_prompt, summary_length)
            elif self.ai_provider == 'gemini':
                return self._analyze_with_gemini(text)
        
        # Fallback to rule-based analysis
        return self._analyze_with_rules(text)

    def _analyze_with_groq(self, text: str, custom_prompt: str = "", summary_length: str = "Standard") -> Dict[str, Any]:
        """Analyze using Groq API and generate complete custom HTML/CSS dashboard"""
        
        # Incorporate user preferences
        user_instructions = ""
        if custom_prompt:
            user_instructions = f"\nUSER CUSTOM INSTRUCTIONS:\n{custom_prompt}\n(Prioritize these instructions over default behavior)"
            
        summary_instruction = ""
        if summary_length == "Brief":
            summary_instruction = "Keep summaries concise and high-level. Focus on bullet points."
        elif summary_length == "Detailed":
            summary_instruction = "Provide in-depth comprehensive summaries and detailed analysis."
        
        prompt = f"""You are an elite Frontend Developer and UI/UX Designer. Your task is to analyze the provided document and create a WORLD-CLASS, HIGHLY RESPONSIVE, and ANIMATED HTML dashboard with ADVANCED VISUALIZATIONS.

CRITICAL DESIGN REQUIREMENTS:
1.  **Visual Style**: Use a modern, premium aesthetic (Glassmorphism, subtle gradients, deep shadows).
    -   Background: Use a sophisticated gradient or mesh gradient.
    -   Cards: White/translucent with backdrop-filter: blur(10px), rounded corners (border-radius: 16px+), and soft shadows.
    -   Typography: Use system fonts (Inter, system-ui) with perfect hierarchy.
2.  **Responsiveness**: MUST be fully responsive.
    -   Use CSS Grid and Flexbox.
    -   Include `@media` queries for mobile devices (stack columns, adjust padding).
    -   Ensure charts resize correctly.
3.  **Animations**: The page MUST feel alive.
    -   **Entry Animations**: Elements must fade in and slide up as they enter the viewport.
    -   **Hover Effects**: Buttons and cards must scale/lift on hover.
    -   **Chart Animations**: Charts must animate on load.
4.  **Interactivity**:
    -   Include a sticky navigation bar.
    -   Add a "Back to Top" button.
    -   Make charts interactive (tooltips enabled).
    -   Add export buttons (PDF and PowerPoint).

TECHNICAL CONSTRAINTS:
-   **Single File**: Output a single HTML string containing ALL CSS (<style>) and JS (<script>).
-   **No External CSS Files**: All styles must be embedded.
-   **Required Libraries** (use CDN):
    -   Chart.js: `https://cdn.jsdelivr.net/npm/chart.js`
    -   Plotly.js: `https://cdn.plot.ly/plotly-2.27.0.min.js`
    -   jQuery: `https://code.jquery.com/jquery-3.7.1.min.js`
    -   DataTables: `https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js`
    -   DataTables CSS: `https://cdn.datatables.net/1.13.7/css/jquery.datatables.min.css`
    -   FontAwesome (optional): For icons
    -   Google Fonts (optional)
-   **Scripting**:
    -   Write custom vanilla JS for scroll animations (IntersectionObserver).
    -   Initialize Chart.js instances properly.
    -   Initialize Plotly charts for advanced visualizations.
    -   Initialize DataTables for interactive tables.

ADVANCED VISUALIZATION REQUIREMENTS:
1.  **Heatmap**: If you find correlation data, comparison matrices, or frequency data, create a heatmap using Plotly.
2.  **Sankey Diagram**: If you find flow data (budget allocation, process flows, transitions), create a Sankey diagram using Plotly.
3.  **Interactive Tables**: If you extract tabular data, create sortable/searchable tables using DataTables.
4.  **Standard Charts**: Continue using Chart.js for bar, line, pie, and doughnut charts.

CONTENT GENERATION:
-   **Analyze** the document text below.
-   **Extract** meaningful sections (Abstract, Key Metrics, Findings, Conclusion).
-   **Visualize** data intelligently:
    -   Standard charts (Bar, Line, Doughnut) for basic metrics
    -   Heatmaps for correlations or comparison matrices
    -   Sankey diagrams for flow/allocation data
    -   Interactive tables for structured data
-   **Structure**:
    -   Header (Title, Subtitle, Export Buttons)
    -   Executive Summary / Abstract ({summary_length} length. {summary_instruction})
    -   Key Metrics Grid (Cards with big numbers)
    -   Detailed Analysis Sections
    -   Advanced Charts Section (Heatmaps, Sankey if applicable)
    -   Interactive Data Tables (if applicable)
    -   Standard Charts Section
    -   Conclusion
    -   Footer

EXPORT BUTTONS:
Include these buttons in the header:
```html
<div class="export-buttons" style="display: flex; gap: 10px; margin-top: 20px;">
    <button onclick="window.print()" style="background: #000; color: white; padding: 12px 24px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; transition: transform 0.2s;">
        📄 Export to PDF
    </button>
</div>
```

{user_instructions}

OUTPUT FORMAT:
Return ONLY the raw HTML code. Start with `<!DOCTYPE html>`. Do not wrap in markdown code blocks.

-------------------------------------
DOCUMENT CONTENT:
-------------------------------------

{text[:25000]}

-------------------------------------
GENERATE THE HTML DASHBOARD NOW:
"""
        
        try:
            # Call Groq API
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                model=Config.GROQ_MODEL,
                temperature=0.5,
                max_tokens=8000,
            )
            
            html_content = chat_completion.choices[0].message.content.strip()
            
            # Remove markdown code blocks if present
            html_content = re.sub(r'^```html\s*', '', html_content)
            html_content = re.sub(r'^```\s*', '', html_content)
            html_content = re.sub(r'\s*```$', '', html_content)
            
            # Return in format expected by Flask
            return {
                "html_content": html_content,
                "is_custom_html": True,
                "text_content": text # Return text for chat context
            }
            
        except Exception as e:
            print(f"Groq API error: {e}")
            print("Falling back to rule-based analysis...")
            return self._analyze_with_rules(text)

    def chat_with_document(self, text: str, question: str) -> str:
        """Chat with the document using Groq"""
        if not self.client:
            return "AI Chat not available (Groq API key missing)."
            
        prompt = f"""You are a helpful AI assistant. Answer the user's question based ONLY on the document content provided below.
        
DOCUMENT CONTENT:
{text[:20000]}

USER QUESTION:
{question}

ANSWER:
"""
        try:
            chat_completion = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=Config.GROQ_MODEL,
                temperature=0.3,
                max_tokens=1000,
            )
            return chat_completion.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating answer: {str(e)}"
    
    def _analyze_with_gemini(self, text: str) -> Dict[str, Any]:
        """Analyze using Gemini API"""
        
        prompt = f"""You are a Research Dashboard Generator AI.
Your job is to analyze academic papers, research reports, feasibility studies, business strategy documents, or any complex text.
You must return a structured JSON output that the Flask backend will convert into a dynamic HTML dashboard AND a Canvas-renderable HTML fragment.
Your output is NOT a fixed set of sections. You must decide which sections are relevant based on the document's actual content.

-------------------------------------
RULE 1 — Section Detection
-------------------------------------
From the uploaded text, detect which of the following section types exist:

Possible section types (include any relevant ones):
- abstract / executive summary
- objectives / research aims
- methodology / approach
- dataset overview
- experiments / results
- findings / observations
- KPIs / metrics / numerical highlights
- market analysis
- competitor analysis
- financial analysis
- SWOT (only if enough info exists)
- risks / limitations
- recommendations
- conclusion
- custom section types if needed

Include ONLY sections actually supported by the document.

-------------------------------------
RULE 2 — Output JSON Format
-------------------------------------

Return JSON shaped like:

{{
  "title": "Main Title",
  "sections": [
    {{
      "id": "unique_id",
      "title": "Section Title",
      "content_html": "<p>HTML content here</p>",

      "chart": {{
        "type": "line | bar | pie | doughnut | radar | scatter | bubble",
        "labels": [...],
        "datasets": [
          {{
            "label": "Dataset Name",
            "data": [...],
            "color": "#HEX"
          }}
        ]
      }}
    }}
  ],

  "ui_theme": {{
    "primary_color": "#0ea5e9",
    "accent_color": "#6366f1",
    "layout": "single-column | two-column | dashboard-cards | scientific-paper"
  }},

  "export_html": "<section>...fully assembled HTML body content...</section>",
  "share_ready": true
}}

NOTES:
- `export_html` should contain a fully merged HTML body snippet combining all sections in visual order.
- It must NOT contain <html>, <head>, scripts, CSS, or Tailwind classes beyond basic layout wrappers.
- Flask will wrap this in a full template.
- Canvas will directly render this HTML fragment.

If a section has no chart, set `"chart": null`.

-------------------------------------
RULE 3 — HTML Content Rules
-------------------------------------
The "content_html" field and "export_html" field must:
- Use only semantic HTML: <p>, <ul>, <li>, <strong>, <h3>, <h4>, <table>, <tr>, <td>
- NO inline CSS
- NO <script> tags
- NO external resources
- NO layout containers beyond div/section
- NO Tailwind classes (the Flask template will inject styling)

-------------------------------------
RULE 4 — Chart Extraction
-------------------------------------
If the document includes numeric data:
- Identify meaningful patterns
- Use only actual values from the text
- Choose correct visual type:

Rules:
- Time-series → line chart
- Category distribution → bar or doughnut chart
- Comparison → bar chart
- Relationship → scatter/bubble chart
- If no valid numbers → set chart to null

Never fabricate values.

-------------------------------------
RULE 5 — Theme Selection
-------------------------------------
Decide the theme based on document type:

- Academic papers → scientific-paper layout
- Business or market research → dashboard-cards
- Strategy / SWOT reports → two-column layout
- Financial documents → corporate layout

-------------------------------------
RULE 6 — Share Support
-------------------------------------
Set `"share_ready": true` when:
- All sections are valid
- JSON is structurally correct

This tells the backend to generate a shareable link.

-------------------------------------
RULE 7 — Response Format
-------------------------------------
Your ENTIRE OUTPUT must be pure JSON.
No explanations.
No markdown.
No code blocks.

Return ONLY the JSON object.

-------------------------------------
DOCUMENT TO ANALYZE:
-------------------------------------

{text[:15000]}
"""
        
        try:
            response = self.model.generate_content(prompt)
            result_text = response.text.strip()
            
            # Remove markdown code blocks if present
            result_text = re.sub(r'^```json\s*', '', result_text)
            result_text = re.sub(r'^```\s*', '', result_text)
            result_text = re.sub(r'\s*```$', '', result_text)
            
            # Parse JSON
            dashboard_data = json.loads(result_text)
            return dashboard_data
            
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._analyze_with_rules(text)
    

    
    def _analyze_with_rules(self, text: str) -> Dict[str, Any]:
        """Fallback rule-based analysis"""
        
        # Simple extraction
        lines = text.split('\n')
        title = lines[0][:100] if lines else "Document Analysis"
        
        # Detect sections
        sections = []
        
        # Abstract/Summary
        abstract_match = re.search(r'(abstract|summary|executive summary)[:\s]+(.*?)(?=\n\n|\Z)', 
                                   text, re.IGNORECASE | re.DOTALL)
        if abstract_match:
            sections.append({
                "id": "abstract",
                "title": "Abstract",
                "content_html": f"<p>{abstract_match.group(2)[:500]}</p>",
                "chart": None
            })
        
        # Extract numbers for a sample chart
        numbers = re.findall(r'\b\d+\.?\d*\b', text)
        if len(numbers) >= 3:
            chart_data = [float(n) for n in numbers[:6]]
            sections.append({
                "id": "metrics",
                "title": "Key Metrics",
                "content_html": "<p>Numerical data extracted from the document.</p>",
                "chart": {
                    "type": "bar",
                    "labels": [f"Metric {i+1}" for i in range(len(chart_data))],
                    "datasets": [{
                        "label": "Values",
                        "data": chart_data,
                        "color": "#0ea5e9"
                    }]
                }
            })
        
        # Conclusion
        conclusion_match = re.search(r'(conclusion|summary|findings)[:\s]+(.*?)(?=\n\n|\Z)', 
                                     text, re.IGNORECASE | re.DOTALL)
        if conclusion_match:
            sections.append({
                "id": "conclusion",
                "title": "Conclusion",
                "content_html": f"<p>{conclusion_match.group(2)[:500]}</p>",
                "chart": None
            })
        
        # Generate export HTML
        export_html = "<section>"
        for section in sections:
            export_html += f"<h2>{section['title']}</h2>{section['content_html']}"
        export_html += "</section>"
        
        return {
            "title": title,
            "sections": sections,
            "ui_theme": {
                "primary_color": "#0ea5e9",
                "accent_color": "#6366f1",
                "layout": "single-column"
            },
            "export_html": export_html,
            "share_ready": True
        }
    
    def _generate_word_cloud(self, text: str) -> str:
        """Generate word cloud image and return as base64 string"""
        try:
            # Create word cloud
            wordcloud = WordCloud(
                width=800,
                height=400,
                background_color='white',
                colormap='viridis',
                max_words=100,
                relative_scaling=0.5,
                min_font_size=10
            ).generate(text)
            
            # Save to buffer
            buffer = io.BytesIO()
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.tight_layout(pad=0)
            plt.savefig(buffer, format='png', bbox_inches='tight', dpi=100)
            plt.close()
            
            # Convert to base64
            buffer.seek(0)
            img_base64 = base64.b64encode(buffer.read()).decode('utf-8')
            return f"data:image/png;base64,{img_base64}"
        except Exception as e:
            print(f"Word cloud generation error: {e}")
            return ""
    
    def _extract_tabular_data(self, text: str) -> List[Dict[str, Any]]:
        """Extract tabular data from text for interactive tables"""
        tables = []
        
        # Simple pattern matching for table-like structures
        # Look for lines with multiple tab or pipe separators
        lines = text.split('\n')
        current_table = []
        
        for line in lines:
            # Check if line looks like a table row (has multiple separators)
            if '|' in line or '\t' in line:
                # Split by separator
                if '|' in line:
                    cells = [cell.strip() for cell in line.split('|') if cell.strip()]
                else:
                    cells = [cell.strip() for cell in line.split('\t') if cell.strip()]
                
                if len(cells) >= 2:  # At least 2 columns
                    current_table.append(cells)
            elif current_table:
                # End of table
                if len(current_table) >= 2:  # At least header + 1 row
                    tables.append({
                        "headers": current_table[0],
                        "rows": current_table[1:]
                    })
                current_table = []
        
        # Check for last table
        if current_table and len(current_table) >= 2:
            tables.append({
                "headers": current_table[0],
                "rows": current_table[1:]
            })
        
        return tables
    
    def _generate_heatmap_data(self, text: str) -> Optional[Dict[str, Any]]:
        """Generate heatmap data from numerical correlations in text"""
        try:
            # Extract numbers and their context
            # This is a simplified version - AI will do better job
            numbers = re.findall(r'\b\d+\.?\d*\b', text)
            if len(numbers) < 9:  # Need at least 3x3 matrix
                return None
            
            # Create a simple correlation matrix
            size = min(5, int(len(numbers) ** 0.5))  # Max 5x5
            matrix_data = [float(n) for n in numbers[:size*size]]
            
            # Reshape into matrix
            matrix = np.array(matrix_data).reshape(size, size)
            
            return {
                "type": "heatmap",
                "z": matrix.tolist(),
                "x": [f"Metric {i+1}" for i in range(size)],
                "y": [f"Category {i+1}" for i in range(size)],
                "colorscale": "Viridis"
            }
        except Exception as e:
            print(f"Heatmap generation error: {e}")
            return None
    
    def _generate_sankey_data(self, text: str) -> Optional[Dict[str, Any]]:
        """Generate Sankey diagram data from flow/transition information"""
        # This is a placeholder - AI will generate better data
        # Sankey requires source, target, and value arrays
        try:
            # Look for flow-related keywords
            flow_keywords = ['from', 'to', 'flow', 'transfer', 'allocation', 'budget']
            has_flow = any(keyword in text.lower() for keyword in flow_keywords)
            
            if not has_flow:
                return None
            
            # Simple example structure (AI will generate actual data)
            return {
                "type": "sankey",
                "node": {
                    "label": ["Source A", "Source B", "Target X", "Target Y"],
                    "color": ["#0ea5e9", "#6366f1", "#10b981", "#f59e0b"]
                },
                "link": {
                    "source": [0, 0, 1, 1],
                    "target": [2, 3, 2, 3],
                    "value": [8, 4, 2, 8]
                }
            }
        except Exception as e:
            print(f"Sankey generation error: {e}")
            return None
    
    def _generate_error_response(self, error_msg: str) -> Dict[str, Any]:
        """Generate error response"""
        return {
            "title": "Analysis Error",
            "sections": [{
                "id": "error",
                "title": "Error",
                "content_html": f"<p>{error_msg}</p>",
                "chart": None
            }],
            "ui_theme": {
                "primary_color": "#ef4444",
                "accent_color": "#dc2626",
                "layout": "single-column"
            },
            "export_html": f"<section><h2>Error</h2><p>{error_msg}</p></section>",
            "share_ready": False
        }
