class ChatbotAPI {
  private baseUrl: string;

  // Constructor that receives the baseUrl as a parameter
  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  public async sendMessage(message: string): Promise<string> {
    const response = await fetch(`${this.baseUrl}/api/chatbot/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ content: message }),
    });

    if (!response.ok) {
      throw new Error("Error al enviar el mensaje al chatbot");
    }

    const data = await response.json();
    return data.content || "No se recibió una respuesta del chatbot";
  }

  public sendWebSocketMessage(
    message: string,
    onMessage: (text: string) => void,
    onError: (error: Event) => void
  ): void {
    const wsUrl = `${this.baseUrl}/api/chatbot/ws`;
    const socket = new WebSocket(wsUrl);

    socket.onopen = () => {
      socket.send(message);
    };

    socket.onmessage = (event) => {
      onMessage(event.data);
    };

    socket.onclose = () => {
      // Optional: trigger a completion callback
    };

    socket.onerror = (error) => {
      console.error("WebSocket Error:", error);
      onError(error);
    };
  }
}

export { ChatbotAPI };
