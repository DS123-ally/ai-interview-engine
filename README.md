# 🤖 AI Interview Engine

A comprehensive AI-powered mock interview system with advanced analytics, powered by AWS Bedrock.

## 🚀 Features

- **Real AI Evaluation**: Powered by AWS Bedrock (Amazon Titan) for authentic question generation and answer evaluation
- **Smart Question Generation**: 
  - Job description-based questions
  - Company-specific questions (Google, Amazon, Microsoft, Meta)
  - Follow-up questions based on your answers
  - Coding challenges with difficulty levels
- **Advanced Analytics**: Performance tracking, industry benchmarks, trend analysis
- **Multiple Interview Rounds**: Technical, HR, and Managerial rounds
- **Export Reports**: Excel and PDF reports with detailed insights
- **Industry Benchmarks**: Compare your performance with industry standards

## 🏗️ Architecture

- **Frontend**: Streamlit web application
- **Backend**: AWS Lambda + API Gateway
- **AI Engine**: AWS Bedrock (Amazon Titan Text Express v1)
- **Analytics**: Plotly charts and pandas data processing

## 📁 Project Structure

```
/workspace/
├── workshop/
│   ├── AI Interview Model/          # Original AWS deployment files
│   │   ├── lambda_function.py       # AWS Lambda function with Bedrock
│   │   ├── template.yaml           # SAM template for AWS deployment
│   │   ├── app.py                  # Flask app for Vercel deployment
│   │   └── deploy.sh               # Deployment script
│   └── ai-interview-clean/         # Main application
│       ├── advanced_analytics_app.py # Full-featured Streamlit app
│       ├── streamlit_app.py        # Basic Streamlit app
│       ├── requirements_bedrock.txt # Dependencies for Bedrock integration
│       └── lambda_function.py      # Lambda function
└── README.md
```

## 🛠️ Setup & Installation

### Prerequisites
- Python 3.8+
- AWS CLI configured
- AWS Bedrock access enabled

### Local Development

**One Command Setup (Linux/Mac):**
```bash
./run.sh
```

**One Command Setup (Windows):**
```cmd
run.bat
```

**Manual Setup:**
```bash
cd workshop/ai-interview-clean
pip install -r requirements_bedrock.txt
streamlit run advanced_analytics_app.py
```

### AWS Deployment
```bash
cd "workshop/AI Interview Model"
chmod +x deploy.sh
./deploy.sh
```

## 🎯 Usage

1. **Start Interview**: Choose role (SDE/ML/Cloud) and interview round
2. **Smart Questions**: Use job description or company-specific questions
3. **AI Evaluation**: Get real-time feedback from AWS Bedrock
4. **Track Progress**: View analytics and compare with industry benchmarks
5. **Export Reports**: Download detailed performance reports

## 🔧 Configuration

Update the API URL in `advanced_analytics_app.py`:
```python
API_URL = "https://your-api-gateway-url.amazonaws.com/Prod"
```

## 📊 Features Overview

### Question Types
- **Standard Questions**: Role-based technical, HR, and managerial questions
- **JD-Based**: Questions tailored to specific job descriptions
- **Company-Specific**: Questions for major tech companies
- **Coding Challenges**: Programming problems with difficulty levels
- **Follow-up Questions**: Dynamic questions based on your answers

### Analytics
- Performance trends over time
- Skills radar chart vs industry benchmarks
- Score distribution analysis
- Company-specific performance tracking
- Question type analysis

### Export Options
- **Excel Reports**: Comprehensive data with multiple sheets
- **PDF Reports**: Printable performance summaries
- **Custom Date Ranges**: Filter reports by time period

## 🤖 AI Integration

The system uses AWS Bedrock with Amazon Titan Text Express v1 for:
- Dynamic question generation based on difficulty and category
- Real-time answer evaluation with detailed scoring
- Constructive feedback and improvement suggestions
- Follow-up question generation

## 🏆 Industry Benchmarks

Compare your performance against industry standards for:
- Software Development Engineers (SDE)
- Machine Learning Engineers (ML)
- Cloud Engineers (Cloud)

Metrics include:
- Technical Accuracy
- Clarity
- Confidence
- Communication
- Relevance
- Completeness
- Structure

## 📈 Performance Tracking

- Overall score trends
- Skills breakdown by category
- Performance by interview round
- Improvement rate calculation
- Percentile ranking

## 🚀 Deployment Options

1. **Local Streamlit**: Run locally for development
2. **AWS Lambda + API Gateway**: Serverless deployment with SAM
3. **Vercel**: Web deployment with Flask backend

## 🔐 Security

- No sensitive data stored locally
- AWS IAM roles for secure Bedrock access
- Environment variables for configuration
- HTTPS endpoints for API communication

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📞 Support

For issues and questions, please open a GitHub issue or contact the development team.

---

**Built with ❤️ using AWS Bedrock, Streamlit, and modern AI technologies**