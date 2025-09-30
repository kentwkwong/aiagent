import React from "react";

interface IntentListProps {
  intents: string[];
  onSelect: (intent: string) => void;
  selectedIntent: string | null;
}

const IntentList: React.FC<IntentListProps> = ({
  intents,
  onSelect,
  selectedIntent,
}) => {
  return (
    <div className="p-4 border-r w-1/3">
      <h2 className="text-lg font-bold mb-3">Intents</h2>
      {intents.length === 0 ? (
        <p className="text-gray-500">No intents available</p>
      ) : (
        <div className="flex flex-col gap-2">
          {intents.map((intent) => (
            <button
              key={intent}
              onClick={() => onSelect(intent)}
              className={`px-3 py-2 rounded text-left ${
                selectedIntent === intent
                  ? "bg-blue-500 text-white"
                  : "bg-gray-100 hover:bg-gray-200"
              }`}
            >
              {intent}
            </button>
          ))}
        </div>
      )}
    </div>
  );
};

export default IntentList;
