import {
  Box,
  Button,
  Container,
  Paper,
  TextField,
  Typography,
} from "@mui/material";
import React, { useEffect, useMemo, useState } from "react";
import FileList, { type FileItem } from "./components/FileList";
import { API_URL } from "./constants";
import { ChatbotAPI } from "./services/ChatbotAPI";
import DocumentService from "./services/DocumentsAPI";
import ReactMarkdown from "react-markdown";

interface Message {
  sender: "user" | "bot";
  text: string;
}

function App() {
  const [isChatOpen, setIsChatOpen] = useState<boolean>(false);
  const [userMessage, setUserMessage] = useState<string>("");
  const [chatHistory, setChatHistory] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false); // Nuevo estado para controlar el loading del chatbot
  const [files, setFiles] = useState<FileItem[]>([]);

  const chatBot = useMemo(() => new ChatbotAPI(API_URL), []);
  const documentsService = useMemo(() => new DocumentService(API_URL), []);

  useEffect(() => {
    const fetchFiles = async () => {
      try {
        const fetchedFiles = await documentsService.listDocuments();
        setFiles(
          fetchedFiles.documents.map((filename) => ({ name: filename }))
        );
      } catch (error) {
        console.error("Error fetching files:", error);
      }
    };
    fetchFiles();
  }, [documentsService]);

  const toggleChat = () => {
    setIsChatOpen(!isChatOpen);
  };

  const sendMessage = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault(); // Prevenir el comportamiento predeterminado del formulario
    if (userMessage.trim() === "") return;

    // Marcar el estado de loading como true mientras se espera la respuesta del chatbot
    setLoading(true);

    // Add user message to chat history
    setChatHistory((prevHistory) => [
      ...prevHistory,
      { sender: "user", text: userMessage },
    ]);

    setUserMessage("");

    // Send via WebSocket and handle streaming
    chatBot.sendWebSocketMessage(
      userMessage.trim(),
      (responseText) => {
        setChatHistory((prevHistory) => {
          // Find the last bot message (assuming it's the last one)
          const lastBotIndex = prevHistory.length - 1;
          if (lastBotIndex >= 0 && prevHistory[lastBotIndex].sender === "bot") {
            // Update the existing bot message
            const updatedHistory = [...prevHistory];
            let lastMessage = updatedHistory[lastBotIndex].text + responseText;
            // remove <think> tags if they exist
            lastMessage = lastMessage
              .replace(/<think>/g, "")
              .replace(/<\/think>/g, "");
            updatedHistory[lastBotIndex] = {
              ...updatedHistory[lastBotIndex],
              text: lastMessage,
            };
            return updatedHistory;
          } else {
            // If no bot message yet, add a new one
            return [...prevHistory, { sender: "bot", text: responseText }];
          }
        });
        setLoading(false);
      },
      (error) => {
        setChatHistory((prevHistory) => [
          ...prevHistory,
          {
            sender: "bot",
            text: `Error: ${error || "An error occurred"}`,
          },
        ]);
        setLoading(false);
      }
    );
  };

  const formatMessage = (message: string): React.ReactNode => {
    if (message.startsWith("Error: ")) {
      return (
        <Box component="span" sx={{ color: "red", fontWeight: "bold" }}>
          {message}
        </Box>
      );
    }
    return <ReactMarkdown>{message}</ReactMarkdown>;
  };

  const handleAddFile = async (file: File) => {
    const newFile: FileItem = {
      name: "Subiendo archivo...",
      loading: true,
    };
    const currentFiles = [...files];
    setFiles([...currentFiles, newFile]);
    const { filename } = await documentsService.uploadDocument(file);
    setFiles([...currentFiles, { name: filename }]);
  };

  const handleDeleteFile = async (name: string) => {
    const currentFiles = [...files];
    const result = await documentsService.deleteDocument(name);
    if (result) {
      setFiles(currentFiles.filter((file) => file.name !== name));
    }
  };

  return (
    <Container maxWidth="sm">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h3" gutterBottom>
          Bienvenido al Chatbot de LLMs
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Este servicio le permite interactuar con un chatbot impulsado por
          modelos de lenguaje grandes (LLMs).
        </Typography>
      </Box>

      <FileList
        files={files}
        onAddFile={handleAddFile}
        onDeleteFile={handleDeleteFile}
      />

      {/* Botón de chat en la esquina inferior derecha */}
      <Box
        sx={{
          position: "fixed",
          bottom: 16,
          right: 16,
          zIndex: 1000,
        }}
      >
        <Button
          variant="contained"
          color="primary"
          onClick={toggleChat}
          sx={{ p: 2, borderRadius: "50%", width: 64, height: 64 }}
        >
          💬
        </Button>
      </Box>

      {isChatOpen && (
        <Paper
          elevation={3}
          sx={{
            position: "fixed",
            bottom: 90,
            right: 16,
            width: 350,
            maxHeight: "80vh",
            overflowY: "auto",
            borderRadius: 2,
            p: 2,
            backgroundColor: "#f5f5f5", // Cambia el color de fondo
          }}
        >
          <Box sx={{ mb: 2 }}>
            <Typography variant="h6" gutterBottom>
              Chatbot
            </Typography>
          </Box>
          <Box sx={{ maxHeight: "60vh", overflowY: "auto" }}>
            {chatHistory.map((msg, index) => (
              <Box
                key={index}
                sx={{
                  mb: 1,
                  p: 2, // Ajusta el padding para que se vea mejor
                  borderRadius: 3, // Redondear más los bordes
                  backgroundColor:
                    msg.sender === "user" ? "#e3f2fd" : "#ffffff", // Cambia el color de fondo según quien lo envió
                }}
              >
                {formatMessage(msg.text)}
              </Box>
            ))}
          </Box>
          <Box sx={{ mt: 2 }}>
            <form onSubmit={sendMessage}>
              {" "}
              {/* Añadir el formulario */}
              <TextField
                autoComplete="off"
                multiline
                fullWidth
                value={userMessage}
                onChange={(e) => setUserMessage(e.target.value)}
                placeholder="Escribe tu mensaje..."
                sx={{ mb: 1 }}
                InputProps={{
                  style: {
                    borderRadius: 20,
                    padding: "8px 16px",
                    overflowY: "auto",
                  }, // Ajusta el estilo del campo de texto con scroll
                }}
              />
              <Button
                fullWidth
                type="submit"
                variant="contained"
                color="primary"
                disabled={userMessage.trim() === "" || loading} // Desactivar botón cuando la caja de texto está vacía o el chatbot está cargando
                sx={{ borderRadius: 20, padding: "8px 16px" }} // Ajusta el estilo del botón
              >
                Enviar
              </Button>
            </form>
          </Box>
        </Paper>
      )}
    </Container>
  );
}

export default App;
