import React, { useState } from "react";
import {
  Box,
  Button,
  TextField,
  List,
  ListItem,
  ListItemText,
  IconButton,
  Typography,
  CircularProgress,
} from "@mui/material";
import { Delete, Upload } from "@mui/icons-material";

export interface FileItem {
  name: string;
  loading?: boolean;
}

interface FileListProps {
  files: FileItem[];
  onAddFile: (file: File) => void;
  onDeleteFile: (name: string) => void;
}

const FileList: React.FC<FileListProps> = ({
  files,
  onAddFile,
  onDeleteFile,
}) => {
  const [isUploadOpen, setIsUploadOpen] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setSelectedFile(e.target.files[0]);
    }
  };

  const handleUpload = () => {
    if (selectedFile) {
      onAddFile(selectedFile);
      setSelectedFile(null);
      setIsUploadOpen(false);
    }
  };

  return (
    <Box>
      <Typography variant="h6" gutterBottom>
        Archivos Subidos
      </Typography>
      <List>
        {files.length === 0 ? (
          <Typography color="text.secondary">
            No hay archivos subidos.
          </Typography>
        ) : (
          files.map((file, index) => (
            <ListItem
              key={index}
              sx={{
                display: "flex",
                justifyContent: "space-between",
                alignItems: "center",
              }}
            >
              {file.loading && <CircularProgress size={20} />}

              <ListItemText primary={file.name} />

              {!file.loading && (
                <Box>
                  <IconButton
                    color="error"
                    onClick={() => onDeleteFile(file.name)}
                    aria-label="Eliminar archivo"
                  >
                    <Delete />
                  </IconButton>
                </Box>
              )}
            </ListItem>
          ))
        )}
      </List>
      <Box mt={2}>
        <Button
          variant="outlined"
          color="primary"
          onClick={() => setIsUploadOpen(true)}
          startIcon={<Upload />}
        >
          Añadir Archivo
        </Button>
        {isUploadOpen && (
          <Box mt={2}>
            <TextField
              type="file"
              onChange={handleFileChange}
              inputProps={{ accept: "text/csv, application/json" }}
            />
            <Button
              variant="contained"
              color="primary"
              onClick={handleUpload}
              disabled={!selectedFile}
              sx={{ mt: 1 }}
            >
              Subir
            </Button>
          </Box>
        )}
      </Box>
    </Box>
  );
};

export default FileList;
