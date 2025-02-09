import React, { ChangeEvent, ReactElement, useState } from "react";
import {
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  TextField,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import { useRouter } from "next/router";
import axios, { AxiosResponse } from "axios";

import { Bridge } from "../../assets/entities/bridge.entity";
import { Information } from "assets/entities/information.entity";

export interface EditBridge {
  edit: boolean;
  bridge: Partial<Bridge>;
}

interface TestingMessage {
  text: string;
  error: boolean;
}

interface BridgeEditProps {
  bridgeEdit: EditBridge;
  handleClose: () => void;
}

function BridgeEditComponent(props: BridgeEditProps): ReactElement {
  const [bridge, setBridge] = useState<Partial<Bridge>>(
    props.bridgeEdit.bridge
  );
  const [testingMessage, setTestingMessage] = useState<TestingMessage>({
    text: "",
    error: false,
  });

  const query = useRouter().query;

  const handleTextChanged =
    (name: string) => (event: ChangeEvent<HTMLInputElement>) => {
      setBridge({ ...bridge, [name]: event.target.value });
    };

  function handleClose(): void {
    setTestingMessage({ text: "", error: false });
    props.handleClose();
  }

  async function handleDelete(): Promise<void> {
    const response = await axios.delete(
      `http://${
        query.apiHost || typeof window !== "undefined"
          ? window.location.hostname
          : "localhost"
      }:${query.apiPort || 9170}/bridges/${bridge.key}`,
      { headers: { "api-key": query.apiKey as string } }
    );
    if (response && response.status < 400) props.handleClose();
    else setTestingMessage({ text: "Failed to delete bridge", error: true });
  }

  async function handleSave() {
    const information = await handleTestBridge();
    if (information && information.uuid) {
      const bridgeData = {
        ...bridge,
        key: information.uuid,
      };
      const url = `http://${
        query.apiHost || typeof window !== "undefined"
          ? window.location.hostname
          : "localhost"
      }:${query.apiPort || 9170}/bridges`;
      console.log("Save:", { url, bridgeData });
      let response: AxiosResponse<Partial<Bridge>, any>;
      try {
        response = props.bridgeEdit.edit
          ? await axios.put<Partial<Bridge>>(
              `${url}/${bridge.key}`,
              bridgeData,
              {
                headers: { "api-key": query.apiKey as string },
              }
            )
          : await axios.post<Partial<Bridge>>(url, bridgeData, {
              headers: { "api-key": query.apiKey as string },
            });
        if (response && response.status < 400) props.handleClose();
        else setTestingMessage({ text: "Failed to save bridge", error: true });
      } catch (e) {
        console.error(e);
      }
    }
  }

  async function handleTestBridge(): Promise<Information | null> {
    setTestingMessage({ text: "Testing bridge..", error: false });
    if (bridge?.apiKey)
      try {
        const response = await axios.get<Information>(
          `http://${bridge.host}:${bridge.port}/information`,
          {
            headers: { "api-key": bridge.apiKey },
          }
        );
        if (response && response.status < 400) {
          console.log("Information:", response.data);
          setTestingMessage({
            text: "Successfully connected to bridge.",
            error: false,
          });
          return response.data;
        }
        setTestingMessage({
          text: `Error testing bridge: ${response.status} - ${response.data}`,
          error: true,
        });
      } catch (e: any) {
        console.error("Error:", e);
        setTestingMessage({
          text: `Error testing bridge: ${e.message}`,
          error: true,
        });
      }
    return null;
  }

  const theme = useTheme();
  const fullScreen = useMediaQuery(theme.breakpoints.down("lg"));

  return (
    <Dialog
      aria-labelledby="form-dialog-title"
      fullScreen={fullScreen}
      maxWidth="md"
      open
    >
      <DialogTitle id="form-dialog-title">
        {props.bridgeEdit.edit ? "Edit" : ""} {bridge.name}
      </DialogTitle>
      <DialogContent>
        <TextField
          autoFocus
          fullWidth
          id="name"
          label="Name"
          onChange={handleTextChanged("name")}
          type="text"
          value={bridge.name || ""}
          variant="outlined"
          sx={{ margin: theme.spacing(1, 0) }}
        />

        <TextField
          fullWidth
          id="host"
          label="Host"
          onChange={handleTextChanged("host")}
          type="text"
          value={bridge.host || ""}
          variant="outlined"
          sx={{ margin: theme.spacing(1, 0) }}
        />

        <TextField
          fullWidth
          id="port"
          label="Port"
          onChange={handleTextChanged("port")}
          type="number"
          value={bridge.port || 9170}
          variant="outlined"
          sx={{ margin: theme.spacing(1, 0) }}
        />

        <TextField
          fullWidth
          id="apiKey"
          label="API Key"
          onChange={handleTextChanged("apiKey")}
          type="text"
          value={bridge.apiKey || ""}
          variant="outlined"
          sx={{ margin: theme.spacing(1, 0) }}
        />
      </DialogContent>
      <DialogActions>
        <Button
          onClick={handleDelete}
          color="inherit"
          variant="contained"
          sx={{ margin: theme.spacing(1, 0) }}
        >
          Delete
        </Button>
        <Typography
          color={testingMessage.error ? "error" : "textPrimary"}
          variant="subtitle2"
          sx={{
            margin: theme.spacing(0, 1),
            flex: 1,
            textAlign: "right",
          }}
        >
          {testingMessage.text}
        </Typography>
        <Button autoFocus onClick={handleClose} variant="contained">
          Cancel
        </Button>
        <Button onClick={handleSave} color="primary" variant="contained">
          Save
        </Button>
      </DialogActions>
    </Dialog>
  );
}

export default BridgeEditComponent;
