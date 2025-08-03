# IntervuewSensei - AI-Powered Interview Preparation

A modern, full-featured web application that generates personalized interview questions and answers based on job descriptions and resumes. Built with FastAPI, Jinja2 templates, and a beautiful responsive UI.

## ✨ Features

- **🎨 Modern UI/UX**: Beautiful, responsive design with smooth animations
- **📄 Document Upload**: Support for PDF, DOCX, DOC, and TXT files
- **✍️ Text Input**: Paste job descriptions and resumes directly
- **🤖 AI-Powered**: Uses Groq LLM for intelligent question generation
- **📱 Mobile Responsive**: Works perfectly on all devices
- **⚡ Real-time Processing**: Fast document analysis and question generation
- **🔒 Secure**: File validation and privacy protection
- **📋 Copy to Clipboard**: Easy sharing of generated questions

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Groq API key

### Installation

1. **Clone and navigate to the project**:

   ```bash
   cd interview_prep
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:

   ```
   GROQ_API_KEY=your_groq_api_key_here
   ```

4. **Run the application**:

   ```bash
   python app.py
   ```

5. **Access the application**:
   Open your browser and go to `http://localhost:8000`

## 📁 Project Structure

```
interview_prep/
├── app.py                 # FastAPI application
├── groq_llm.py           # InterviewQuestionGenerator class
├── requirements.txt       # Python dependencies
├── templates/
│   ├── base.html         # Base template with navigation/footer
│   └── index.html        # Main page template
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   └── js/
│       ├── main.js       # General website functionality
│       └── generator.js  # Interview generator functionality
└── README.md            # This file
```

## 🎯 How It Works

1. **Upload Documents**: Users can upload job descriptions and resumes in multiple formats
2. **AI Analysis**: The system extracts text and analyzes content using Groq LLM
3. **Generate Questions**: Creates personalized interview questions with ideal answers
4. **Export Results**: Users can copy and share the generated questions

## 🔧 API Endpoints

### Web Interface

- **GET `/`** - Main application interface
- **GET `/supported-formats`** - List supported file formats

### API Endpoints

- **POST `/generate`** - Generate questions from text input
- **POST `/upload-and-generate`** - Upload documents and generate questions
- **POST `/upload-document`** - Upload and extract text from a single document

### Example Usage

#### Text Input

```bash
curl -X POST "http://localhost:8000/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "We are hiring a Python developer...",
    "resume": "John Doe, Software Engineer..."
  }'
```

#### File Upload

```bash
curl -X POST "http://localhost:8000/upload-and-generate" \
  -F "job_description_file=@job_description.pdf" \
  -F "resume_file=@resume.docx"
```

## 🎨 UI Features

### Navigation

- **Responsive Navigation Bar**: Fixed header with smooth scrolling
- **Mobile Menu**: Hamburger menu for mobile devices
- **Smooth Scrolling**: Animated navigation to sections

### Hero Section

- **Gradient Background**: Eye-catching design with animations
- **Call-to-Action Buttons**: Clear user guidance
- **Floating Elements**: Animated cards showing the process

### Features Section

- **Card Layout**: Clean feature presentation
- **Hover Effects**: Interactive design elements
- **Icon Integration**: Font Awesome icons throughout

### Generator Interface

- **Dual Input Methods**: Text and file upload options
- **File Validation**: Real-time file type and size checking
- **Drag & Drop**: Intuitive file upload experience
- **Progress Indicators**: Loading states and feedback

### Results Display

- **Formatted Output**: Clean question and answer presentation
- **Copy Functionality**: One-click copy to clipboard
- **Responsive Layout**: Works on all screen sizes

## 🛠️ Technical Stack

### Backend

- **FastAPI**: Modern, fast web framework
- **Jinja2**: Template engine for dynamic HTML
- **LangChain**: LLM integration framework
- **Groq**: High-performance LLM provider

### Frontend

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with CSS Grid and Flexbox
- **JavaScript**: Interactive functionality
- **Font Awesome**: Icon library

### Document Processing

- **PyPDF2**: PDF text extraction
- **python-docx**: Word document processing
- **File Validation**: Size and format checking

## 🎨 Design Features

### Color Scheme

- **Primary**: Purple gradient (#667eea to #764ba2)
- **Secondary**: Pink accent (#f093fb)
- **Neutral**: Gray scale for text and backgrounds

### Typography

- **Font**: Inter (Google Fonts)
- **Weights**: 300, 400, 500, 600, 700
- **Responsive**: Scales appropriately on all devices

### Animations

- **Smooth Transitions**: CSS transitions for all interactions
- **Scroll Animations**: Elements animate as they come into view
- **Loading States**: Spinner animations during processing
- **Hover Effects**: Interactive feedback on all clickable elements

## 📱 Responsive Design

### Breakpoints

- **Desktop**: 1200px and above
- **Tablet**: 768px to 1199px
- **Mobile**: Below 768px

### Mobile Features

- **Touch-Friendly**: Large touch targets
- **Optimized Layout**: Stacked elements on small screens
- **Fast Loading**: Optimized for mobile networks

## 🔒 Security & Privacy

### File Validation

- **Size Limits**: 10MB maximum per file
- **Type Checking**: Only allowed formats accepted
- **Content Validation**: Ensures files contain readable text

### Data Protection

- **No Storage**: Files are processed in memory only
- **Secure Processing**: Temporary file handling
- **Error Handling**: Comprehensive error management

## 🚀 Performance

### Optimizations

- **Static File Serving**: Efficient CSS/JS delivery
- **Template Caching**: Jinja2 template optimization
- **Async Processing**: Non-blocking file operations
- **Minimal Dependencies**: Lightweight package selection

### Loading Times

- **Fast Initial Load**: Optimized asset delivery
- **Progressive Enhancement**: Core functionality works without JavaScript
- **Lazy Loading**: Resources loaded as needed

## 🧪 Testing

### Manual Testing

1. **File Upload**: Test all supported formats
2. **Text Input**: Verify text processing
3. **Mobile Responsive**: Test on various devices
4. **Error Handling**: Test invalid inputs

### Browser Compatibility

- **Chrome**: Full support
- **Firefox**: Full support
- **Safari**: Full support
- **Edge**: Full support

## 🛠️ Development

### Running in Development Mode

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### File Structure for Development

```
interview_prep/
├── app.py                 # Main FastAPI app
├── groq_llm.py           # LLM integration
├── templates/            # HTML templates
├── static/              # Static assets
│   ├── css/            # Stylesheets
│   └── js/             # JavaScript files
└── requirements.txt     # Dependencies
```

### Adding New Features

1. **Backend**: Add endpoints in `app.py`
2. **Frontend**: Update templates and static files
3. **Styling**: Modify `static/css/style.css`
4. **Functionality**: Update JavaScript files

## 📈 Future Enhancements

### Planned Features

- **User Accounts**: Save and manage interview sessions
- **Question Categories**: Technical, behavioral, situational
- **Export Options**: PDF, Word document export
- **Interview Scheduling**: Calendar integration
- **Analytics**: Usage statistics and insights

### Technical Improvements

- **Caching**: Redis for faster responses
- **CDN**: Content delivery network for assets
- **Monitoring**: Application performance monitoring
- **Testing**: Automated test suite

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature-name`
3. **Make your changes**: Follow the existing code style
4. **Test thoroughly**: Ensure all functionality works
5. **Submit a pull request**: Include detailed description

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **FastAPI** for the excellent web framework
- **Groq** for the high-performance LLM
- **Font Awesome** for the beautiful icons
- **Inter Font** for the typography

## 📞 Support

For support, email contact@IntervuewSensei.com or create an issue in the repository.

---

**Made with ❤️ for better interview preparation**
