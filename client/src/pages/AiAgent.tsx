import React, { useState } from "react";
import axios from "../api/axios";
import IntentList from "../components/IntentList";
import QnADisplay from "../components/QnADisplay";

interface Message {
  question: string;
  answer: string;
  intent: string;
  timestamp: string;
}

type IntentData = Record<string, Message[]>;

const IntentPage: React.FC = () => {
  const [email, setEmail] = useState("user@example.com");
  const [data, setData] = useState<IntentData>({});
  const [selectedIntent, setSelectedIntent] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchMessages = async () => {
    if (!email) return alert("Please enter an email");
    setLoading(true);
    try {
      const res = await axios.get(`/ai/history?email=${email}`, {
        withCredentials: true,
      });
      const history: Message[] = res.data.history || [];

      // 🔄 Group by intent
      const grouped: IntentData = history.reduce((acc, msg) => {
        if (!acc[msg.intent]) acc[msg.intent] = [];
        acc[msg.intent].push(msg);
        return acc;
      }, {} as IntentData);

      setData(grouped);
      setSelectedIntent(null);
    } catch (err) {
      console.error("Error fetching messages:", err);
      alert("Failed to fetch messages. Check console for details.");
    } finally {
      setLoading(false);
    }
  };

  const intents = Object.keys(data);

  return (
    <div className="flex flex-col h-screen">
      {/* Email input and fetch button */}
      <div className="p-4 border-b flex gap-2">
        <input
          type="email"
          placeholder="Enter your email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          className="border px-3 py-2 rounded w-64"
        />
        <button
          onClick={fetchMessages}
          disabled={loading}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
        >
          {loading ? "Loading..." : "Fetch Data"}
        </button>
      </div>

      {/* Split layout */}
      <div className="flex flex-1">
        <IntentList
          intents={intents}
          onSelect={setSelectedIntent}
          selectedIntent={selectedIntent}
        />
        <QnADisplay
          messages={selectedIntent ? data[selectedIntent] || [] : []}
        />
      </div>
    </div>
  );
};

export default IntentPage;
