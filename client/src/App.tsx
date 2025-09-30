import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
// import Login from "./pages/Login";
import ProtectedRoute from "./components/ProtectedRoute";
import AiAgent from "./pages/AiAgent";
import AskAIPage from "./pages/AskAiPage";
const App: React.FC = () => {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<AskAIPage />} />
        <Route path="/aiagent" element={<AiAgent />} />
        <Route path="/askaipage" element={<AskAIPage />} />
        <Route
          path="/aiagentbah"
          element={
            <ProtectedRoute>
              <AiAgent />
            </ProtectedRoute>
          }
        />
      </Routes>
    </BrowserRouter>
  );
};

export default App;
