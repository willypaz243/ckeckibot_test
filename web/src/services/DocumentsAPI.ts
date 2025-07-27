// src/types/DocumentService.ts
class DocumentService {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  // Upload a document
  async uploadDocument(
    file: File
  ): Promise<{ success: boolean; filename: string }> {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(`${this.baseUrl}/api/documents/upload`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Failed to upload document: ${response.statusText}`);
    }

    return await response.json();
  }

  // List documents
  async listDocuments(): Promise<{ documents: string[] }> {
    const response = await fetch(`${this.baseUrl}/api/documents/list`, {
      method: "GET",
    });

    if (!response.ok) {
      throw new Error(`Failed to list documents: ${response.statusText}`);
    }

    return await response.json();
  }

  // Delete a document
  async deleteDocument(filename: string): Promise<{ success: boolean }> {
    const response = await fetch(`${this.baseUrl}/api/documents/${filename}`, {
      method: "DELETE",
    });

    if (!response.ok) {
      throw new Error(`Failed to delete document: ${response.statusText}`);
    }

    return await response.json();
  }
}

export default DocumentService;
