import React from "react";
import ReactMarkdown from "react-markdown";

interface Message {
  question: string;
  answer: string;
  timestamp: string;
}

interface QnADisplayProps {
  messages: Message[];
}

const QnADisplay: React.FC<QnADisplayProps> = ({ messages }) => {
  return (
    <div className="flex-1 p-4">
      {messages.map((msg, i) => (
        <div key={i} className="border rounded p-3 shadow-sm mb-4">
          <h2>Q: {msg.question}</h2>
          A:
          <ReactMarkdown
            components={{
              p: ({ node, ...props }) => (
                <p className="mt-2 text-gray-700" {...props} />
              ),
              ul: ({ node, ...props }) => (
                <ul className="list-disc pl-5 mt-2" {...props} />
              ),
              li: ({ node, ...props }) => <li className="mb-1" {...props} />,
              strong: ({ node, ...props }) => (
                <strong className="font-bold" {...props} />
              ),
            }}
          >
            {msg.answer}
          </ReactMarkdown>
          <p className="mt-2 text-xs text-gray-500">
            📅 {new Date(msg.timestamp).toLocaleString()}
          </p>
        </div>
      ))}
    </div>
  );
};

export default QnADisplay;
