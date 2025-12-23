import React, { useState } from 'react';
import axios from 'axios';
import { Upload, FileText, Target, TrendingUp, AlertCircle, CheckCircle2, XCircle, Sparkles } from 'lucide-react';

const API_BASE = import.meta.env.VITE_API_BASE_URL;
fetch(`${API_BASE}/analyze`)

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [loading, setLoading] = useState(false);
  const [generatingJD, setGeneratingJD] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile && selectedFile.type === 'application/pdf') {
      setFile(selectedFile);
      setError('');
    } else {
      setError('Please select a valid PDF file');
      setFile(null);
    }
  };

  const handleGenerateJD = async () => {
    if (!jobTitle.trim()) {
      setError('Please enter a job title');
      return;
    }

    setGeneratingJD(true);
    setError('');

    const formData = new FormData();
    formData.append('job_title', jobTitle);

    try {
      const response = await axios.post(`${API_BASE_URL}/generate-jd`, formData);
      setJobDescription(response.data.job_description);
      setError('');
    } catch (err) {
      setError('Failed to generate job description. Please try again.');
    } finally {
      setGeneratingJD(false);
    }
  };

  const handleAnalyze = async () => {
    if (!file) {
      setError('Please upload your resume');
      return;
    }
    if (!jobDescription.trim()) {
      setError('Please enter job description');
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('job_description', jobDescription);

    try {
      const response = await axios.post(`${API_BASE_URL}/analyze`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-blue-600';
    if (score >= 40) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getScoreGradient = (score) => {
    if (score >= 80) return 'from-green-500 to-emerald-600';
    if (score >= 60) return 'from-blue-500 to-indigo-600';
    if (score >= 40) return 'from-yellow-500 to-orange-600';
    return 'from-red-500 to-rose-600';
  };

  return (
    <div className="min-h-screen py-8 px-4">
      {/* Header */}
      <header className="max-w-6xl mx-auto mb-12 text-center">
        <div className="inline-flex items-center gap-3 mb-4">
          <div className="p-3 bg-gradient-to-br from-blue-600 to-purple-600 rounded-2xl shadow-lg">
            <Target className="w-8 h-8 text-white" />
          </div>
          <h1 className="text-5xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            AI Resume Analyzer
          </h1>
        </div>
        <p className="text-gray-600 text-lg max-w-2xl mx-auto">
          Powered by Machine Learning • TF-IDF Vectorization • Cosine Similarity Algorithm
        </p>
      </header>

      <div className="max-w-6xl mx-auto grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Input Section */}
        <div className="space-y-6">
          {/* Job Title Input with Auto-Generate */}
          <div className="glass-effect rounded-2xl p-6">
            <label className="flex items-center gap-2 text-lg font-semibold text-gray-800 mb-3">
              <Sparkles className="w-5 h-5 text-purple-600" />
              Quick Generate (Just Enter Job Title)
            </label>
            <div className="flex gap-3">
              <input
                type="text"
                value={jobTitle}
                onChange={(e) => setJobTitle(e.target.value)}
                placeholder="e.g., Full Stack Developer, Data Scientist, DevOps Engineer..."
                className="flex-1 p-4 border-2 border-gray-200 rounded-xl focus:border-purple-500 focus:ring-4 focus:ring-purple-100 transition-all"
                onKeyPress={(e) => e.key === 'Enter' && handleGenerateJD()}
              />
              <button
                onClick={handleGenerateJD}
                disabled={generatingJD}
                className="px-6 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold rounded-xl shadow-lg hover:shadow-xl transition-all disabled:opacity-50"
              >
                {generatingJD ? (
                  <div className="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <Sparkles className="w-5 h-5" />
                )}
              </button>
            </div>
            <p className="text-sm text-gray-500 mt-2">
              💡 Try: "Full Stack Developer", "Data Scientist", "DevOps Engineer", "Mobile Developer"
            </p>
          </div>

          {/* Job Description */}
          <div className="glass-effect rounded-2xl p-6">
            <label className="flex items-center gap-2 text-lg font-semibold text-gray-800 mb-3">
              <FileText className="w-5 h-5 text-blue-600" />
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here... Include required skills, qualifications, and responsibilities."
              className="w-full h-64 p-4 border-2 border-gray-200 rounded-xl focus:border-blue-500 focus:ring-4 focus:ring-blue-100 transition-all resize-none"
            />
          </div>

          {/* File Upload */}
          <div className="glass-effect rounded-2xl p-6">
            <label className="flex items-center gap-2 text-lg font-semibold text-gray-800 mb-3">
              <Upload className="w-5 h-5 text-blue-600" />
              Upload Resume (PDF)
            </label>
            <div className="relative">
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                className="hidden"
                id="file-upload"
              />
              <label
                htmlFor="file-upload"
                className="flex flex-col items-center justify-center w-full h-40 border-3 border-dashed border-gray-300 rounded-xl cursor-pointer hover:border-blue-500 hover:bg-blue-50 transition-all"
              >
                <Upload className="w-12 h-12 text-gray-400 mb-2" />
                <span className="text-gray-600 font-medium">
                  {file ? file.name : 'Click to upload PDF'}
                </span>
                <span className="text-sm text-gray-400 mt-1">Max size: 5MB</span>
              </label>
            </div>
          </div>

          {/* Analyze Button */}
          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="w-full py-4 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white font-bold text-lg rounded-xl shadow-lg hover:shadow-xl transform hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none"
          >
            {loading ? (
              <span className="flex items-center justify-center gap-2">
                <div className="w-5 h-5 border-3 border-white border-t-transparent rounded-full animate-spin"></div>
                Analyzing...
              </span>
            ) : (
              <span className="flex items-center justify-center gap-2">
                <TrendingUp className="w-5 h-5" />
                Analyze Resume
              </span>
            )}
          </button>

          {/* Error Message */}
          {error && (
            <div className="glass-effect rounded-xl p-4 border-l-4 border-red-500 bg-red-50">
              <div className="flex items-center gap-2">
                <AlertCircle className="w-5 h-5 text-red-600" />
                <p className="text-red-800 font-medium">{error}</p>
              </div>
            </div>
          )}
        </div>

        {/* Results Section */}
        <div className="space-y-6">
          {result ? (
            <>
              {/* Match Score Card */}
              <div className="glass-effect rounded-2xl p-8 text-center">
                <h2 className="text-2xl font-bold text-gray-800 mb-6">Match Score</h2>
                
                {/* Circular Progress */}
                <div className="relative inline-flex items-center justify-center">
                  <svg className="w-48 h-48 transform -rotate-90">
                    <circle
                      cx="96"
                      cy="96"
                      r="88"
                      stroke="currentColor"
                      strokeWidth="12"
                      fill="none"
                      className="text-gray-200"
                    />
                    <circle
                      cx="96"
                      cy="96"
                      r="88"
                      stroke="currentColor"
                      strokeWidth="12"
                      fill="none"
                      strokeDasharray={`${2 * Math.PI * 88}`}
                      strokeDashoffset={`${2 * Math.PI * 88 * (1 - result.match_score / 100)}`}
                      className={`bg-gradient-to-r ${getScoreGradient(result.match_score)} transition-all duration-1000`}
                      strokeLinecap="round"
                    />
                  </svg>
                  <div className="absolute">
                    <p className={`text-6xl font-bold ${getScoreColor(result.match_score)}`}>
                      {result.match_score}%
                    </p>
                  </div>
                </div>
                
                <p className="mt-6 text-gray-600 text-lg leading-relaxed">
                  {result.summary}
                </p>
              </div>

              {/* Matched Keywords */}
              <div className="glass-effect rounded-2xl p-6">
                <div className="flex items-center gap-2 mb-4">
                  <CheckCircle2 className="w-5 h-5 text-green-600" />
                  <h3 className="text-xl font-bold text-gray-800">
                    Matched Skills ({result.matched_keywords.length})
                  </h3>
                </div>
                <div className="flex flex-wrap gap-2">
                  {result.matched_keywords.map((keyword, idx) => (
                    <span
                      key={idx}
                      className="px-4 py-2 bg-green-100 text-green-700 rounded-lg font-medium border border-green-200"
                    >
                      ✓ {keyword}
                    </span>
                  ))}
                </div>
              </div>

              {/* Missing Keywords */}
              <div className="glass-effect rounded-2xl p-6">
                <div className="flex items-center gap-2 mb-4">
                  <XCircle className="w-5 h-5 text-red-600" />
                  <h3 className="text-xl font-bold text-gray-800">
                    Missing Skills ({result.missing_keywords.length})
                  </h3>
                </div>
                <div className="flex flex-wrap gap-2">
                  {result.missing_keywords.map((keyword, idx) => (
                    <span
                      key={idx}
                      className="px-4 py-2 bg-red-100 text-red-700 rounded-lg font-medium border border-red-200"
                    >
                      ✗ {keyword}
                    </span>
                  ))}
                </div>
              </div>
            </>
          ) : (
            <div className="glass-effect rounded-2xl p-12 text-center">
              <div className="w-24 h-24 mx-auto mb-6 bg-gradient-to-br from-gray-100 to-gray-200 rounded-full flex items-center justify-center">
                <TrendingUp className="w-12 h-12 text-gray-400" />
              </div>
              <h3 className="text-2xl font-bold text-gray-800 mb-3">
                Ready to Analyze
              </h3>
              <p className="text-gray-600 max-w-md mx-auto">
                Upload your resume and paste the job description to get an AI-powered
                match analysis with actionable insights.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Footer */}
      <footer className="max-w-6xl mx-auto mt-12 text-center text-gray-500 text-sm">
        <p>Built with React, FastAPI, Scikit-learn & MongoDB | © 2024 AI Resume Analyzer</p>
      </footer>
    </div>
  );
}

export default App;