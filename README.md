# Research Dashboard Generator

Transform your research papers, business reports, and academic documents into beautiful, interactive dashboards with AI-powered insights and visualizations.

## Features

🤖 **Free Cloud AI** - Uses Groq API with Llama 3.1 models (ultra-fast, free, cloud-based!)

📊 **Interactive Charts** - Automatic generation of beautiful visualizations (line, bar, pie, radar, scatter charts) from numerical data

🎨 **Multiple Themes** - Customizable layouts including:
- Single-column (simple documents)
- Two-column (comparative analysis)
- Dashboard-cards (business reports)
- Scientific-paper (academic research)

📤 **Easy Export** - Export dashboards as standalone HTML files or print-ready PDFs

🚀 **Modern UI** - Stunning interface with glassmorphism effects, smooth animations, and responsive design

☁️ **Deploy Anywhere** - Cloud-ready with API key authentication (no local AI installation needed)

## Supported File Types

- PDF documents
- Microsoft Word (DOCX, DOC)
- Plain text (TXT)

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd PlotResearch
```

### 2. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 3. Get Free Groq API Key

1. Visit: **https://console.groq.com**
2. Sign up (free, no credit card required)
3. Go to: https://console.groq.com/keys
4. Create a new API key
5. Copy your API key

See [GROQ_SETUP.md](GROQ_SETUP.md) for detailed instructions with screenshots.

### 4. Configure environment
```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```env
AI_PROVIDER=groq
GROQ_API_KEY=gsk_your_api_key_here
GROQ_MODEL=llama-3.1-70b-versatile
```

### 5. Run the application
```bash
python app.py
```

### 6. Open your browser
```
http://localhost:5000
```

## Alternative: Use Google Gemini

If you prefer Gemini over Groq:

1. Get API key from: https://makersuite.google.com/app/apikey
2. Install: `pip install google-generativeai`
3. Update `.env`:
   ```env
   AI_PROVIDER=gemini
   GEMINI_API_KEY=your_gemini_key_here
   ```

## Usage

1. **Upload Document**: Drag and drop or click to browse for your PDF, DOCX, or TXT file
2. **AI Analysis**: The system automatically analyzes your document and extracts:
   - Key sections (abstract, methodology, results, conclusions, etc.)
   - Numerical data and metrics
   - Relevant insights and findings
3. **View Dashboard**: Explore your interactive dashboard with charts and visualizations
4. **Export**: Download as HTML or print as PDF

## Project Structure

```
PlotResearch/
├── app.py                 # Flask application
├── analyzer.py            # Document analysis engine
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── .env.example         # Environment variables template
├── templates/           # HTML templates
│   ├── index.html      # Landing page
│   ├── dashboard.html  # Dashboard display
│   └── export.html     # Export template
├── static/             # Static assets
│   ├── css/
│   │   └── style.css   # Styles
│   └── js/
│       ├── main.js     # Upload handling
│       └── dashboard.js # Dashboard functionality
└── sample_documents/   # Sample files for testing
```

## Technology Stack

- **Backend**: Flask (Python)
- **AI**: Groq API (Llama 3.1) or Google Gemini
- **Charts**: Chart.js
- **Styling**: Modern CSS with glassmorphism
- **Document Parsing**: PyPDF2, python-docx

## Configuration

Edit `config.py` to customize:
- Upload folder location
- Maximum file size
- Allowed file extensions
- API settings

## API Endpoints

- `GET /` - Landing page
- `POST /upload` - Upload and analyze document
- `GET /dashboard/<id>` - View dashboard
- `GET /export/<id>` - Export dashboard
- `GET /api/dashboard/<id>` - Get dashboard JSON

## Sample Documents

The `sample_documents/` folder contains example files:
- `research_paper.txt` - Academic research paper on climate change
- `business_report.txt` - Business strategy report for e-commerce expansion

## Development

To run in development mode:
```bash
python app.py
```

The application will run on `http://localhost:5000` with debug mode enabled.

## License

MIT License

## Support

For issues, questions, or contributions, please open an issue on GitHub.

## Acknowledgments

- Google Gemini AI for document analysis
- Chart.js for beautiful visualizations
- Flask community for excellent documentation
