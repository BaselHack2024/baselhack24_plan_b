import React from "react";
import { createStyles, makeStyles } from "@mui/styles";
import Avatar from "@mui/material/Avatar";

const useStyles = makeStyles((theme) =>
  createStyles({
    messageRow: {
      display: "flex",
    },
    messageRowRight: {
      display: "flex",
      justifyContent: "flex-end",
    },
    messageBlue: {
      position: "relative",
      marginLeft: "20px",
      marginBottom: "15px",
      padding: "10px",
      backgroundColor: "#E8E8EA",
      width: "60%",
      textAlign: "left",
      font: "400 .9em 'Open Sans', sans-serif",
      border: "1px solid #E8E8EA",
      borderRadius: "10px",
      "&:after": {
        content: "''",
        position: "absolute",
        width: "0",
        height: "0",
        borderTop: "15px solid #E8E8EA",
        borderLeft: "15px solid transparent",
        borderRight: "15px solid transparent",
        top: "0",
        left: "-15px",
      },
      "&:before": {
        content: "''",
        position: "absolute",
        width: "0",
        height: "0",
        borderTop: "17px solid #E8E8EA",
        borderLeft: "16px solid transparent",
        borderRight: "16px solid transparent",
        top: "-1px",
        left: "-17px",
      },
    },
    messageOrange: {
      color: "white",
      position: "relative",
      marginRight: "20px",
      marginBottom: "15px",
      padding: "10px",
      backgroundColor: "#497efb",
      width: "60%",
      textAlign: "left",
      font: "400 .9em 'Open Sans', sans-serif",
      border: "1px solid #497efb",
      borderRadius: "10px",
      "&:after": {
        content: "''",
        position: "absolute",
        width: "0",
        height: "0",
        borderTop: "15px solid #497efb",
        borderLeft: "15px solid transparent",
        borderRight: "15px solid transparent",
        top: "0",
        right: "-15px",
      },
      "&:before": {
        content: "''",
        position: "absolute",
        width: "0",
        height: "0",
        borderTop: "17px solid #497efb",
        borderLeft: "16px solid transparent",
        borderRight: "16px solid transparent",
        top: "-1px",
        right: "-17px",
      },
    },

    messageContent: {
      padding: 0,
      margin: 0,
    },
    messageTimeStampRight: {
      position: "absolute",
      fontSize: ".85em",
      fontWeight: "300",
      marginTop: "10px",
      bottom: "-3px",
      right: "5px",
    },

    displayName: {
      marginLeft: "20px",
    },
  })
);

export const MessageLeft = (props) => {
  const message = props.message ? props.message : "no message";
  const classes = useStyles();
  return (
    <>
      <div className={classes.messageRow}>
        <div className={classes.messageBlue}>
          <p className={classes.messageContent}>{message}</p>
        </div>
      </div>
    </>
  );
};

export const MessageRight = (props) => {
  const classes = useStyles();
  const message = props.message ? props.message : "no message";
  return (
    <div className={classes.messageRowRight}>
      <div className={classes.messageOrange}>
        <p className={classes.messageContent}>{message}</p>
      </div>
    </div>
  );
};

export const MessageLeftWithImage = (props) => {
  const objectUrl = URL.createObjectURL(props.image);
  const classes = useStyles();
  const message = props.message ? props.message : "no message";
  return (
    <>
      <div className={classes.messageRow}>
        <div className={classes.messageBlue}>
          <img src={objectUrl} style={{ width: "100%", marginBottom: "5px" }} />
          <p className={classes.messageContent}>{message}</p>
        </div>
      </div>
    </>
  );
};
