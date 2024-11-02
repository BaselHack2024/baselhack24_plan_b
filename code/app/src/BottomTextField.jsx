import React, { useState, useEffect } from "react";
import Paper from "@mui/material/Paper";
import InputBase from "@mui/material/InputBase";
import Divider from "@mui/material/Divider";
import IconButton from "@mui/material/IconButton";
import ArrowUpwardRoundedIcon from "@mui/icons-material/ArrowUpwardRounded";
import SpeedDial from "@mui/material/SpeedDial";
import SpeedDialIcon from "@mui/material/SpeedDialIcon";
import SpeedDialAction from "@mui/material/SpeedDialAction";
import FolderCopyRoundedIcon from "@mui/icons-material/FolderCopyRounded";
import CameraAltRoundedIcon from "@mui/icons-material/CameraAltRounded";
import UploadAndDisplayImages from "./UploadAndDisplayImages";
import { createProcessId, uploadPicturesToProcess } from "./utils/api-service";

const actions = [
  {
    icon: <FolderCopyRoundedIcon />,
    name: "Folder",
    operation: "select-image-from-file",
  },
  {
    icon: <CameraAltRoundedIcon />,
    name: "Camera",
    operation: "camera",
  },
];

function BottomTextField() {
  const [isModalOpen, setModalOpen] = useState(false);
  const [processId, setProcessId] = useState("");

  const handleDialClick = (e, operation) => {
    e.preventDefault();
    if (operation === "camera") {
      console.log("camera");
    } else if (operation === "select-image-from-file") {
      setModalOpen(true);
    }
  };

  const handleCloseUploadDialog = (images) => {
    if (images) {
      setModalOpen(false);
      uploadPicturesToProcess(images, processId).then(response => {
        console.log(response);
      })
    }
  }

  useEffect(() => {
    createProcessId().then(id => {
      console.log(id)
      setProcessId(id);
    })
  }, []);

  return (
    <Paper
      component="form"
      sx={{
        position: "fixed",
        p: "4px 4px",
        display: "flex",
        alignItems: "center",
        bottom: 0,
        left: 0,
        right: 0,
      }}
    >
      <InputBase
        sx={{ ml: 8, flex: 1 }}
        placeholder="Add pictures"
        inputProps={{ "aria-label": "text field" }}
      />
      <SpeedDial
        ariaLabel="speed dial"
        sx={{
          position: "absolute",
          bottom: 6,
          left: 1,
        }}
        FabProps={{ size: "small" }}
        icon={<SpeedDialIcon />}
      >
        {actions.map((action) => (
          <SpeedDialAction
            key={action.name}
            icon={action.icon}
            tooltipTitle={action.name}
            onClick={(e) => handleDialClick(e, action.operation)}
          />
        ))}
      </SpeedDial>
      <Divider sx={{ height: 28, m: 0.5 }} orientation="vertical" />
      <IconButton color="primary" sx={{ p: "10px" }} aria-label="submit">
        <ArrowUpwardRoundedIcon />
      </IconButton>
      <UploadAndDisplayImages
        open={isModalOpen}
        onClose={(images) => handleCloseUploadDialog(images)}
      />
    </Paper>
  );
}

export default BottomTextField;
