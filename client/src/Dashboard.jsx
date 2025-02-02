import { useState } from "react"
import { GoogleGenerativeAI } from "@google/generative-ai"
import { jsPDF } from "jspdf"
import { saveAs } from "file-saver"
import { Document, Packer, Paragraph, TextRun } from "docx"
import { MultiStepLoader as Loader } from "./multi-step-loader";
import { IconSquareRoundedX } from "@tabler/icons-react";

const loadingStates = [
  {
    text: "Uploading & Validating Data",
  },
  {
    text: "Analyzing Key Financial Metrics",
  },
  {
    text: "Generating AI-Powered Insights",
  },
  {
    text: "Structuring Report & Visualization",
  },
  {
    text: "Finalizing & Exporting PDF",
  },
  
];
 

const API_KEY = "AIzaSyDnGZHEEEZj7m0dGNey9TqGJFtMpN7tmgg" // Replace with your actual API key

export default function DashboardPage() {

  const [company, setCompany] = useState("")
  const [reportType, setReportType] = useState("Annual")
  const [loading, setLoading] = useState(false)
  const [report, setReport] = useState(null)
  const [pdf, setPdf] = useState(null)

  const generateReport = async () => {
    if (!company) {
      alert("Please enter a company name.")
      return
    }

    setLoading(true)
    setReport(null)
    setPdf(null)

    try {
      const genAI = new GoogleGenerativeAI(API_KEY)
      const model = genAI.getGenerativeModel({ model: "gemini-1.5-pro" })

      const prompt = `
        Generate a professional ${reportType} financial report for ${company} using realistic analysis.
        Format all section titles in *bold* and make the content detailed.
        Include:
        1. *Executive Summary*
        2. *Income Statement Analysis*
        3. *Balance Sheet Analysis*
        4. *Cash Flow Statement Analysis*
        5. *Key Financial Ratios*
        6. *Revenue & Cost Breakdown*
        7. *Market & Competitive Analysis*
        8. *Debt & Capital Structure*
        9. *Financial Forecasts*
        10. *Risks & Challenges*
        11. *Management Strategy & Outlook*`

      const response = await model.generateContent(prompt)
      const result = await response.response.text()

      setReport(result)
      const generatedPdf = generatePDF(result)
      setPdf(generatedPdf)
    } catch (error) {
      console.error("Error:", error)
      alert("Failed to generate report. Please check API key or try again.")
    } finally {
      setLoading(false)
    }
  }

  const generatePDF = (reportContent) => {
    const doc = new jsPDF({ unit: "mm", format: "a4" })

    doc.setFont("helvetica", "bold")
    doc.setFontSize(26)
    doc.setTextColor(0, 123, 255)
    doc.text("FINANCIAL REPORT", 20, 20)

    doc.setFontSize(18)
    doc.setTextColor(0, 0, 0)
    doc.text(`Company: ${company}`, 20, 40)
    doc.text(`Report Type: ${reportType}`, 20, 50)
    doc.text(`Generated on: ${new Date().toLocaleDateString()}`, 20, 60)

    let y = 80
    const pageHeight = doc.internal.pageSize.height

    const parseAndPrintText = (text, startX, startY) => {
      const words = text.split(/(\*.*?\*)/)
      words.forEach((word) => {
        if (word.startsWith("*") && word.endsWith("*")) {
          doc.setFont("helvetica", "bold")
          word = word.replace(/\*/g, "")
        } else {
          doc.setFont("helvetica", "normal")
        }
        doc.text(word, startX, startY)
        startX += doc.getTextWidth(word) + 2
      })
    }

    const lines = reportContent.split("\n")
    lines.forEach((line) => {
      if (y > pageHeight - 20) {
        doc.addPage()
        y = 20
        doc.text("FINANCIAL REPORT", 20, 20)
      }
      parseAndPrintText(line, 20, y)
      y += 7
    })

    return doc
  }

  const downloadPDF = () => {
    if (pdf) {
      pdf.save(`${company}-financial-report.pdf`)
    }
  }

  const downloadDOCX = () => {
    if (!report) return

    const doc = new Document({
      sections: [
        {
          properties: {},
          children: [
            new Paragraph({
              children: [new TextRun({ text: "FINANCIAL REPORT", bold: true, size: 32 })],
            }),
            new Paragraph({
              children: [new TextRun({ text: `Company: ${company}`, bold: true })],
            }),
            new Paragraph({
              children: [new TextRun({ text: `Report Type: ${reportType}`, bold: true })],
            }),
            new Paragraph({
              children: [new TextRun({ text: `Generated on: ${new Date().toLocaleDateString()}`, bold: true })],
            }),
            ...report.split("\n").map(
              (line) =>
                new Paragraph({
                  children: [new TextRun({ text: line.replace(/\*/g, ""), bold: line.startsWith("*") })],
                }),
            ),
          ],
        },
      ],
    })

    Packer.toBlob(doc).then((blob) => {
      saveAs(blob, `${company}-financial-report.docx`)
    })
  }

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100 pt-20">
      <div className="max-w-4xl mx-auto p-6">
        <div className="bg-gray-800 rounded-lg shadow-xl p-8">
          <h1 className="text-3xl font-bold text-blue-400 text-center mb-8">📊 Financial Report Generator</h1>

          <div className="space-y-6">
            <div>
              <label htmlFor="company" className="block text-sm font-medium text-gray-400 mb-2">
                Company Name
              </label>
              <input
                id="company"
                type="text"
                placeholder="Enter company name"
                value={company}
                onChange={(e) => setCompany(e.target.value)}
                className="w-full px-4 py-3 text-lg bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white"
              />
            </div>

            <div>
              <label htmlFor="reportType" className="block text-sm font-medium text-gray-400 mb-2">
                Report Type
              </label>
              <select
                id="reportType"
                value={reportType}
                onChange={(e) => setReportType(e.target.value)}
                className="w-full px-4 py-3 text-lg bg-gray-700 border border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-white"
              >
                <option value="Quarterly">Quarterly Report</option>
                <option value="Annual">Annual Report</option>
              </select>
            </div>
            <Loader loadingStates={loadingStates} loading={loading} duration={2000} />
            <button onClick={() => { 
                generateReport(); 
                setLoading(true); 
              }}
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-bold text-lg hover:bg-blue-700 transition-colors disabled:bg-blue-800 disabled:text-gray-300"
            >
              {loading ? "Generating..." : "Generate Report"}
            </button>
            {loading && (
        <button
          className="fixed top-4 right-4 text-black dark:text-white z-[120]"
          onClick={() => setLoading(false)}
        >
          <IconSquareRoundedX className="h-10 w-10" />
        </button>
      )}

            {report && (
              <div className="space-y-4 mt-8">
                <button
                  onClick={downloadPDF}
                  className="w-full bg-green-600 text-white py-3 px-4 rounded-lg font-bold text-lg hover:bg-green-700 transition-colors"
                >
                  Download PDF
                </button>
                <button
                  onClick={downloadDOCX}
                  className="w-full bg-purple-600 text-white py-3 px-4 rounded-lg font-bold text-lg hover:bg-purple-700 transition-colors"
                >
                  Download DOCX
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}