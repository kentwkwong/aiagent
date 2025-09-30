import React, { useState } from "react";
import axios from "../api/axios";

interface AIResponse {
  intent: string;
  answer: string;
  error?: string;
}

const AskAIPage: React.FC = () => {
  const [email, setEmail] = useState("user@example.com");
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState<AIResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    if (!email || !question) {
      alert("Please enter both email and question");
      return;
    }

    setLoading(true);
    setResponse(null);

    try {
      const res = await axios.post(
        "/ai/ask",
        { email, question },
        { withCredentials: true }
      );
      setResponse(res.data);
      setQuestion(""); // clear input
    } catch (err) {
      console.error("Error asking AI:", err);
      setResponse({ intent: "", answer: "", error: "Failed to ask AI" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto mt-10 p-4 border rounded shadow">
      <h1 className="text-2xl font-bold mb-4">Ask AI</h1>

      <div className="mb-4">
        <label className="block mb-1 font-semibold">Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          placeholder="Enter your email"
          className="border px-3 py-2 rounded w-full"
        />
      </div>

      <div className="mb-4">
        <label className="block mb-1 font-semibold">Question:</label>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Type your question here"
          className="border px-3 py-2 rounded w-full"
          onKeyDown={(e) => e.key === "Enter" && handleSubmit()}
        />
      </div>

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
      >
        {loading ? "Submitting..." : "Submit"}
      </button>

      {response && (
        <div className="mt-6 p-4 border rounded bg-gray-50">
          {response.error ? (
            <p className="text-red-500">{response.error}</p>
          ) : (
            <>
              <p>
                <span className="font-semibold">Intent:</span> {response.intent}
              </p>
              <p className="mt-2">
                <span className="font-semibold">Answer:</span> {response.answer}
              </p>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default AskAIPage;
