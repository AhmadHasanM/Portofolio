"use client"

import { useState, useEffect } from "react"
import { Download, Eye, FileText, Trash2 } from "lucide-react";

export default function PptGenerator() {
  const [activeTab, setActiveTab] = useState("generate")
  const [company, setCompany] = useState("")
  const [context1, setContext1] = useState("")
  const [context2, setContext2] = useState("")
  const [context3, setContext3] = useState("")
  const [aiNews, setAiNews] = useState(false)
  const [companyInsight, setCompanyInsight] = useState(false)
  const [template, setTemplate] = useState("")
  const [slideCount, setSlideCount] = useState("3")
  const [history, setHistory] = useState<any[]>([])
  const [output, setOutput] = useState<any | null>(null)
  const [previewSlides, setPreviewSlides] = useState<string[]>([])
  const [modalOpen, setModalOpen] = useState(false)
  const [notification, setNotification] = useState<string | null>(null)
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);


  // 🔔 Popup Notification Component
  function PopupNotification({ message, onClose }: { message: string; onClose: () => void }) {
    return (
      <div className="fixed top-5 right-5 bg-gray-900 border border-gray-700 shadow-lg rounded-lg p-4 z-50">
        <p className="text-white">{message}</p>
        <button
          onClick={onClose}
          className="mt-2 text-sm text-red-400 hover:underline"
        >
          Close
        </button>
      </div>
    )
  }

  async function loadHistory() {
    try {
      const res = await fetch("http://localhost:5000/api/history")
      if (res.ok) {
        const data = await res.json()
        setHistory(data)
      }
    } catch (err) {
      console.error("Failed to load history:", err)
    }
  }

  async function generatePpt() {
    if (!company || !context1 || !context2 || !template) {
      alert("Isi minimal company, 2 context points, dan pilih template!")
      return
    }

    // 🔔 Show popup saat mulai generate
    setNotification(`Generating PPT for ${company}... ⏳`)

    try {
      const response = await fetch("http://localhost:5000/api/generate_ppt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          company,
          context1,
          context2,
          context3,
          aiNews,
          companyInsight,
          template,
          slideCount,
        }),
      })

      if (response.ok) {
        const data = await response.json()
        setOutput(data)
        loadHistory()
        setNotification(`PPT for ${company} generated successfully ✅`)
      } else {
        setNotification(`Failed to generate PPT for ${company} ❌`)
      }
    } catch (err) {
      console.error("Generate error:", err)
      setNotification(`Error generating PPT for ${company} ⚠️`)
    } finally {
      setTimeout(() => setNotification(null), 4000)
    }
  }

  async function openPreview(tpl: string) {
    try {
      const res = await fetch(`http://localhost:5000/api/template/${tpl}/slides`)
      if (!res.ok) {
        alert("Preview not available for this template")
        return
      }
      const data = await res.json()
      setPreviewSlides(data.slides)
      setModalOpen(true)
    } catch (err) {
      console.error("Preview failed:", err)
      alert("Failed to load preview")
    }
  }

  async function deleteHistory(id: string) {
    try {
      const res = await fetch(`http://localhost:5000/api/history/${id}`, {
        method: "DELETE",
      })
      if (res.ok) {
        setHistory(history.filter((h) => (h._id || h.id) !== id))
        setNotification("History deleted successfully ✅")
      } else {
        setNotification("Failed to delete history ❌")
      }
    } catch (err) {
      console.error("Delete error:", err)
      setNotification("Error deleting history ⚠️")
    } finally {
      setTimeout(() => setNotification(null), 3000)
    }
  }

  useEffect(() => {
    loadHistory()
  }, [])

  return (
    <div className="bg-gray-900 text-gray-100 min-h-screen">
      <div className="max-w-6xl mx-auto py-10 space-y-8">
        {/* Title */}
        <h1 className="text-4xl md:text-5xl font-extrabold text-center">
          <span className="text-white drop-shadow-lg">AI Presentation </span>
          <span className="bg-gradient-to-r from-green-400 via-green-500 to-green-600 bg-clip-text text-transparent">
            Generator
          </span>
        </h1>
        <p className="text-center text-gray-300 text-lg mt-2 tracking-wide">
          Create <span className="text-yellow-400 font-semibold">professional</span> presentations with{" "}
          <span className="text-green-400 font-semibold">AI assistance</span>
        </p>

        {/* Tabs */}
        <div className="flex justify-center space-x-8 border-b border-gray-700">
          <button
            onClick={() => setActiveTab("generate")}
            className={`
              relative py-2 px-4 font-semibold transition duration-300
              ${activeTab === "generate"
                ? "text-white border-b-4 border-green-500"
                : "text-gray-400 hover:text-yellow-400 hover:border-b-2 hover:border-yellow-500"}
            `}
          >
            Generate
          </button>
          <button
            onClick={() => setActiveTab("history")}
            className={`
              relative py-2 px-4 font-semibold transition duration-300
              ${activeTab === "history"
                ? "text-white border-b-4 border-green-500"
                : "text-gray-400 hover:text-yellow-400 hover:border-b-2 hover:border-yellow-500"}
            `}
          >
            History
          </button>
        </div>

        {/* Generate Tab */}
        {activeTab === "generate" && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Left: Form */}
            <div className="relative bg-gray-800 shadow-lg rounded-xl p-8 space-y-8 border border-gray-700 overflow-hidden">
              <div className="absolute inset-0 rounded-xl border-2 border-transparent bg-gradient-to-r from-black/20 via-green/10 to-black/20 pointer-events-none"></div>
              
              <div className="relative z-10 space-y-8">
                {/* Company */}
                <div>
                  <label className="block mb-2 text-sm font-bold tracking-wide text-white uppercase">
                    Company
                  </label>
                  <select
                    value={company}
                    onChange={(e) => setCompany(e.target.value)}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500 transition"
                  >
                    <option value="">Select a company</option>
                    <option value="OpenAI">OpenAI</option>
                    <option value="Google">Google</option>
                    <option value="Microsoft">Microsoft</option>
                    <option value="Tesla">Tesla</option>
                  </select>
                </div>

                {/* Context Points */}
                <div>
                  <label className="block mb-2 text-sm font-bold tracking-wide text-white uppercase">
                    Context Points
                  </label>
                  <textarea
                    rows={3}
                    placeholder="Context point 1 (min 20 words)"
                    value={context1}
                    onChange={(e) => setContext1(e.target.value)}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 mb-3 focus:outline-none focus:ring-2 focus:ring-green-500 placeholder-gray-400"
                  />
                  <textarea
                    rows={3}
                    placeholder="Context point 2 (min 20 words)"
                    value={context2}
                    onChange={(e) => setContext2(e.target.value)}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 mb-3 focus:outline-none focus:ring-2 focus:ring-green-500 placeholder-gray-400"
                  />
                  <textarea
                    rows={3}
                    placeholder="Context point 3 (optional)"
                    value={context3}
                    onChange={(e) => setContext3(e.target.value)}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500 placeholder-gray-400"
                  />
                </div>

                {/* Checkbox Options */}
                <div>
                  <label className="block mb-2 text-sm font-bold tracking-wide text-white uppercase">
                    Include Options
                  </label>
                  <div className="flex items-center space-x-6">
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={aiNews}
                        onChange={(e) => setAiNews(e.target.checked)}
                        className="accent-green-500 w-5 h-5"
                      />
                      <span className="text-gray-300">AI News</span>
                    </label>
                    <label className="flex items-center space-x-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={companyInsight}
                        onChange={(e) => setCompanyInsight(e.target.checked)}
                        className="accent-green-500 w-5 h-5"
                      />
                      <span className="text-gray-300">Company Insight</span>
                    </label>
                  </div>
                </div>

                {/* Template Selection */}
                <div>
                  <label className="block mb-2 text-sm font-bold tracking-wide text-white uppercase">
                    Presentation Style
                  </label>
                  <div className="grid grid-cols-2 gap-4">
                    {["classic", "general", "modern", "professional"].map((tpl) => (
                      <label key={tpl} className="cursor-pointer group">
                        <input
                          type="radio"
                          name="template"
                          value={tpl}
                          checked={template === tpl}
                          onChange={() => setTemplate(tpl)}
                          className="hidden peer"
                        />
                        <div className="p-3 bg-gray-700 rounded-lg border border-gray-600 group-hover:shadow-lg peer-checked:border-green-500 transition">
                          <img
                            src={`http://localhost:5000/static/templates/${tpl}.png`}
                            alt={tpl}
                            className="rounded mb-2 w-full h-24 object-cover"
                          />
                          <p className="font-medium text-center capitalize text-gray-200 group-hover:text-yellow-400">
                            {tpl}
                          </p>
                          <button
                            type="button"
                            onClick={() => openPreview(tpl)}
                            className="block mt-2 text-sm text-gray-400 hover:underline text-center w-full"
                          >
                            Preview Template
                          </button>
                        </div>
                      </label>
                    ))}
                  </div>
                </div>

                {/* Number of Slides */}
                <div>
                  <label className="block mb-2 text-sm font-bold tracking-wide text-white uppercase">
                    Number of Slides
                  </label>
                  <select
                    value={slideCount}
                    onChange={(e) => setSlideCount(e.target.value)}
                    className="w-full bg-gray-700 border border-gray-600 rounded-lg p-3 focus:outline-none focus:ring-2 focus:ring-green-500 transition"
                  >
                    {[3, 4, 5, 6, 7].map((n) => (
                      <option key={n} value={n}>
                        {n}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Generate Button */}
                <button
                  onClick={generatePpt}
                  className="w-full bg-gradient-to-r from-green-600 via-green-500 to-green-600 hover:from-green-800 hover:via-green-600 hover:to-green-800 text-white py-3 rounded-lg font-bold shadow-md transition"
                >
                  🚀 Generate PPT
                </button>
              </div>
            </div>

            {/* Right: Generated Presentation */}
            <div className="bg-gray-800 shadow-lg rounded-xl p-6 border border-dashed border-gray-600 flex flex-col">
              <h2 className="text-xl font-bold mb-4 text-center">Generated Presentation</h2>

              {!output ? (
                <div className="flex flex-col items-center justify-center flex-1 text-gray-400">
                  <a
                    className="bg-gradient-to-r from-yellow-500 to-yellow-700 text-white px-3 py-2 rounded-lg font-medium shadow-md transition"
                    title="Document"
                    >
                      <FileText size={40} />
                  </a>
                  <p className="font-medium">
                    Fill in the details and click "Generate Presentation"
                  </p>
                  <p className="text-sm text-gray-500 mt-1">
                    Your AI-generated presentation will appear here
                  </p>
                </div>
              ) : (
                <div className="space-y-3 overflow-y-auto pr-2 flex-1">
                  {output.slides?.map((slide: any, idx: number) => (
                    <div
                      key={idx}
                      className="bg-gray-700 rounded-lg p-4 text-left shadow"
                    >
                      <h3 className="font-semibold text-yellow-400 mb-2">
                        {slide.title || `Slide ${idx + 1}`}
                      </h3>
                      <p className="text-gray-200 text-sm whitespace-pre-line">
                        {slide.content}
                      </p>
                    </div>
                  ))}

                  {/* 👉 Tambahan Download Button */}
                  {output.download_url && (
                    <a
                      href={`http://localhost:5000${output.download_url}`}
                      className="block mt-4 bg-gradient-to-r from-yellow-600 via-yellow-500 to-yellow-600 hover:from-yellow-800 hover:via-yellow-600 hover:to-yellow-800 text-white px-4 py-2 rounded-lg font-medium text-center shadow-md transition"
                    >
                      📥 Download PPT
                    </a>
                  )}
                </div>
              )}
            </div>
          </div>
        )}

        {/* History Tab */}
        {activeTab === "history" && (
          <div className="relative bg-gray-800 shadow-lg rounded-xl p-6 space-y-6 border border-gray-700 overflow-hidden">
            <div className="absolute inset-0 rounded-xl border-2 border-transparent bg-gradient-to-r from-black/20 via-green/20 to-black/20 pointer-events-none"></div>

            <div className="relative z-10 space-y-6">
              <h2 className="text-2xl font-extrabold">History</h2>

              <div className="space-y-4 text-gray-300">
                {history.map((item) => {
                  const id = item.id
                  return (
                    <div
                      key={id}
                      className="flex justify-between items-center bg-gray-700/60 p-4 rounded-lg border border-gray-600 hover:border-green-500 transition shadow-sm hover:shadow-md"
                    >
                      <div>
                        <p className="font-semibold text-white text-lg">{item.company}</p>
                        <p className="text-sm text-gray-400">
                          {item.template} • {item.slideCount} slides
                        </p>
                        <p className="text-xs text-gray-500">
                          Created at: {item.created_at}
                        </p>
                        <span
                          className={`inline-block px-3 py-1 text-xs font-semibold rounded-full mt-2 ${
                            item.status === "completed"
                              ? "bg-green-600/80 text-white"
                              : item.status === "in_queue"
                              ? "bg-yellow-500/80 text-black"
                              : "bg-red-600/80 text-white"
                          }`}
                        >
                          {item.status === "completed"
                            ? `${item.company} • Success ✅`
                            : item.status === "in_queue"
                            ? `${item.company} • In Queue ⏳`
                            : `${item.company} • Failed ❌`}
                        </span>
                      </div>

                      <div className="flex space-x-3">
                        {item.status === "completed" && (
                          <>
                            {/* Download PPT */}
                            <a
                              href={`http://localhost:5000${item.download_url}`}
                              className="bg-gradient-to-r from-blue-500 to-blue-700 hover:from-blue-600 hover:to-blue-800 text-white px-4 py-2 rounded-lg font-medium shadow-md transition"
                              title="Download"
                            >
                              <Download size={18} />
                            </a>

                            {/* View PPT */}
                            <button
                              onClick={() =>
                                setPreviewUrl(`http://localhost:5000/api/convert_pdf/${item.filename}`)
                              }
                              className="bg-gradient-to-r from-purple-500 to-purple-700 hover:from-purple-600 hover:to-purple-800 text-white px-4 py-2 rounded-lg font-medium shadow-md transition"
                              title="View PPT"
                            >
                              <Eye size={18} />
                            </button>

                            {/* Convert to PDF */}
                            <a
                              href={`http://localhost:5000/api/convert_pdf/${item.filename}`}
                              className="bg-gradient-to-r from-yellow-500 to-yellow-700 hover:from-yellow-600 hover:to-yellow-800 text-white px-4 py-2 rounded-lg font-medium shadow-md transition"
                              title="Convert to PDF"
                            >
                              <FileText size={18} />
                            </a>
                          </>
                        )}

                        {/* Delete */}
                        <button
                          onClick={() => deleteHistory(id)}
                          className="bg-gradient-to-r from-red-500 to-red-700 hover:from-red-600 hover:to-red-800 text-white px-4 py-2 rounded-lg font-medium shadow-md transition"
                          title="Delete"
                        >
                          <Trash2 size={18} />
                        </button>
                      </div>
                    </div>
                  )
                })}
              </div>
            </div>
          </div>
        )}

        {/* Modal Preview */}
        {modalOpen && (
          <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50">
            <div className="bg-gray-900 rounded-lg w-4/5 h-4/5 relative p-4 overflow-y-auto">
              <button
                onClick={() => setModalOpen(false)}
                className="absolute top-2 right-2 text-white bg-red-600 px-3 py-1 rounded"
              >
                Close
              </button>
              <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mt-10">
                {previewSlides.map((url, idx) => (
                  <img
                    key={idx}
                    src={`http://localhost:5000${url}`}
                    alt={`Slide ${idx + 1}`}
                    className="rounded shadow border border-gray-700"
                  />
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Modal Preview PPT */}
        {previewUrl && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg w-3/4 h-3/4 relative shadow-lg">
              <button
                onClick={() => setPreviewUrl(null)}
                className="absolute top-2 right-2 bg-red-500 hover:bg-red-600 text-white rounded px-2 py-1"
              >
                ✕
              </button>
              <iframe
                src={previewUrl}
                className="w-full h-full rounded-lg"
              />
            </div>
          </div>
        )}

        {/* 🔔 Popup Notification */}
        {notification && (
          <PopupNotification message={notification} onClose={() => setNotification(null)} />
        )}
      </div>
    </div>
  )
}
