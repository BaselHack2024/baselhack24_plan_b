import CloseIcon from "@mui/icons-material/Close";
import Button from "@mui/material/Button";
import Dialog from "@mui/material/Dialog";
import DialogActions from "@mui/material/DialogActions";
import DialogContent from "@mui/material/DialogContent";
import DialogTitle from "@mui/material/DialogTitle";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/material/styles";
import UploadFileIcon from "@mui/icons-material/UploadFile";
import { useState } from "react";

const BootstrapDialog = styled(Dialog)(({ theme }) => ({
  "& .MuiDialogContent-root": {
    padding: theme.spacing(2),
  },
  "& .MuiDialogActions-root": {
    padding: theme.spacing(1),
  },
}));

const UploadAndDisplayImages = ({ open, onClose }) => {
  const [selectedImages, setSelectedImages] = useState([]);

  const handleImageChange = (event) => {
    const files = Array.from(event.target.files);

    if (selectedImages.length + files.length > 10) {
      alert("You can upload a maximum of 10 images.");
      return;
    }

    setSelectedImages((prevImages) => [...prevImages, ...files]);
  };

  const handleRemoveImage = (index) => {
    setSelectedImages((prevImages) => prevImages.filter((_, i) => i !== index));
  };

  return (
    <BootstrapDialog
      onClose={() => onClose(null)}
      open={open}
      aria-labelledby="customized-dialog-title"
    >
      <DialogTitle sx={{ m: 0, p: 2 }} id="customized-dialog-title">
        Upload and Display Images
        <IconButton
          aria-label="close"
          onClick={() => onClose([])}
          sx={{
            position: "absolute",
            right: 8,
            top: 8,
            color: (theme) => theme.palette.grey[500],
          }}
        >
          <CloseIcon />
        </IconButton>
      </DialogTitle>
      <DialogContent dividers>
        <Typography variant="body2" gutterBottom>
          Select up to 10 images to upload and display.
        </Typography>
        <div style={{ display: "flex", flexWrap: "wrap" }}>
          {selectedImages.map((image, index) => (
            <div key={index} style={{ margin: "10px" }}>
              <img
                alt="manual step"
                height={"60px"}
                src={URL.createObjectURL(image)}
              />
              <br />
              <button onClick={() => handleRemoveImage(index)}>Remove</button>
            </div>
          ))}
        </div>
        <Button
          component="label"
          variant="outlined"
          startIcon={<UploadFileIcon />}
          sx={{ marginRight: "1rem" }}
        >
          Upload Images
          <input
            type="file"
            hidden
            name="images"
            multiple
            onChange={handleImageChange}
          />
        </Button>
      </DialogContent>
      <DialogActions>
        <Button variant="contained" onClick={() => onClose(selectedImages)}>
          Send images
        </Button>
      </DialogActions>
    </BootstrapDialog>
  );
};

export default UploadAndDisplayImages;
