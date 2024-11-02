import React, { useState, useEffect, useRef } from "react";
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
import {
  createProcessId,
  uploadPicturesToProcess,
  startProcess,
  checkResult,
} from "./utils/api-service";
import { MessageLeft, MessageRight, MessageLeftWithImage } from "./Message";
import Box from "@mui/material/Box";
import timeout from "./utils/sleep";
import AudioForResult from "./assets/mariachi.mp3";
import { CircularProgress } from "@mui/material";


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
  const [messages, setMessages] = useState([]);
  const messagesRef = useRef(messages);
  const [disableInputs, setDisableInput] = useState(false);
  const [loading, setLoading] = useState(false);
  const [uploadedImages, setUploadedImages] = useState([]);

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
      setUploadedImages(images);
      uploadPicturesToProcess(images, processId).then((response) => {
        console.log(response);
        const messagesCopy = Object.assign([], messages);
        for (const item of response) {
          console.log(item);
          if (item.state === "success") {
            messagesCopy.push({
              type: "left",
              message: `Successfully uploaded ${item.image.name}!`,
            });
          } else {
            messagesCopy.push({
              type: "left",
              message: `Error while uploading ${item.image.name}...`,
            });
          }
        }
        setMessages(messagesCopy);
      });
    }
  };

  const submitToApi = async () => {
    setDisableInput(true);
    const messagesCopy = Object.assign([], messages);
    messagesCopy.push({
      type: "left",
      message: `Please create instructions for me`,
    });
    messagesCopy.push({
      type: "right",
      message: `Thank you for the input, I am working on it!`,
    });
    setMessages(messagesCopy);
    setLoading(true);

    await startProcess(processId);

    const interval = setInterval(async () => {
      const response = await checkResult(processId);
      console.log(response);
      if (typeof response === "object") {
        clearInterval(interval);
        handleAnalysisResponse(response);
      }
    }, 2000);
  };

  const handleAnalysisResponse = async (response) => {
    console.log(response);
    const messagesCopy = Object.assign([], messagesRef.current);

    messagesCopy.push({
      type: "right",
      message: `Hey I am finsished with writing the manual for ${response.object}!`,
    });
    const audio = new Audio(AudioForResult);
    await audio.play();

    await timeout(1000);

    response.steps.forEach((step, index) => {
      messagesCopy.push({
        type: "right-picture",
        message: `Step ${step.step}, ${step.instruction}`,
        image: uploadedImages[index],
      });
    });

    setMessages(messagesCopy);
    setLoading(false);
  };

  useEffect(() => {
    createProcessId().then((id) => {
      console.log(id);
      setProcessId(id);
    });
  }, []);

  useEffect(() => {
    messagesRef.current = messages;
  }, [messages]);

  return (
    <div>
      <Paper
        sx={{
          position: "fixed",
          p: "4px 4px",
          display: "flex",
          flexDirection: "column",
          maxHeight: "85vh",
          overflowY: "auto",
          top: 75,
          left: 0,
          right: 0,
        }}
      >
        {messages.map((message) => (
          <React.Fragment key={message.message}>
            {message.type === "left" && (
              <>
                <MessageRight message={message.message} />
              </>
            )}
            {message.type === "right" && (
              <>
                <MessageLeft message={message.message} />
              </>
            )}
            {message.type === "right-picture" && (
              <>
                <MessageLeftWithImage
                  message={message.message}
                  image={message.image}
                />
              </>
            )}
          </React.Fragment>
        ))}
        {loading && (
          <>
            <Box sx={{ width: "calc(100% - 20px)", marginLeft: "20px" }}>
              <CircularProgress />
            </Box>
          </>
        )}
      </Paper>
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
          FabProps={{
            size: "small",
            sx: {
              bgcolor: "#223E44",
              "&:hover": {
                bgcolor: "#223E44",
              },
            },
          }}
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
        <IconButton
          color="primary"
          sx={{ p: "10px" }}
          aria-label="submit"
          onClick={submitToApi}
          disabled={disableInputs}
        >
          <ArrowUpwardRoundedIcon />
        </IconButton>
        <UploadAndDisplayImages
          open={isModalOpen}
          onClose={(images) => handleCloseUploadDialog(images)}
        />
      </Paper>
    </div>
  );
}

export default BottomTextField;
