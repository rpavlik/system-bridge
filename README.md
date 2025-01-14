# System Bridge

[![CodeQL](https://github.com/timmo001/system-bridge/actions/workflows/codeql.yml/badge.svg)](https://github.com/timmo001/system-bridge/actions/workflows/codeql.yml)
[![Build](https://github.com/timmo001/system-bridge/actions/workflows/build.yml/badge.svg)](https://github.com/timmo001/system-bridge/actions/workflows/build.yml)
[![Deploy](https://github.com/timmo001/system-bridge/actions/workflows/deploy.yml/badge.svg)](https://github.com/timmo001/system-bridge/actions/workflows/deploy.yml)
[![Lint](https://github.com/timmo001/system-bridge/actions/workflows/lint.yml/badge.svg)](https://github.com/timmo001/system-bridge/actions/workflows/lint.yml)

A bridge for your systems.

![Logo](./resources/system-bridge-rect.png)

## Features

- System Information - Access your system's information via the data modules using the API/WebSocket.
- Open files and URLs - Automate your system by opening a URL/path via the API/WebSocket.
- Send Notifications - Send system notifications via the API/WebSocket.
- Compatible with Windows and Linux.
- Integrated with [Home Assistant](https://www.home-assistant.io/integrations/system_bridge).

<!--
Android Companion App - You can find the Android companion app on the [Play Store](https://play.google.com/store/apps/details?id=dev.timmo.systembridge). The source for this app can be found on [GitHub](https://github.com/timmo001/system-bridge-android-companion).
-->

## Documentation

### Installation

You can find installation instructions [here](https://system-bridge.timmo.dev/docs/install).

### Running

You can find instructions to run the application [here](https://system-bridge.timmo.dev/docs/running).

### Data Modules

You can find documentation data modules that can be accessed via the API/WebSocket [here](https://system-bridge.timmo.dev/docs/modules).

### CLI

You can find documentation for the CLI [here](https://system-bridge.timmo.dev/docs/cli).

### API

You can find documentation for the WebSocket [here](https://system-bridge.timmo.dev/docs/websocket).

### WebSocket

You can find documentation for the WebSocket [here](https://system-bridge.timmo.dev/docs/websocket).

### Packages

### `systembridgebackend`

The main application which contains the API/WebSocket and data modules. This package requires the `systembridgeshared` package.

### `systembridgecli`

The command line interface for the application. Here you can get the `api-key` and update settings and get data.

### `systembridgeconnector`

Allows other applications to connect to the backend. For example, in the [Home Assistant](https://www.home-assistant.io/integrations/system_bridge) integration.

### `systembridgefrontend`

The frontend for the application. This is used by the `systembridgegui` module to show settings etc.

### `systembridgegui`

The GUI for the application. This shows a system tray icon and allows you to interact with the application.

### `systembridgeshared`

Shared package required by the `systembridgebackend`, `systembridgecli` and `systembridgegui` packages.

### `systembridgewindowssensors`

Specifically for windows, adds sensors to get windows system information.

### Developing

You can install each python module using pip:

```bash
python -m pip install .
```

inside each directory with a setup.py file.

You can also install all current dev releases using the following command:

```bash
python -m pip install --upgrade --pre systembridgeshared systembridgebackend systembridgecli systembridgeconnector systembridgefrontend systembridgegui systembridgewindowssensors
```

#### Frontend

To develop the frontend, enter into the `frontend` directory and use `yarn` to install the dependencies:

```bash
cd frontend
yarn install
```

Then start the development server:

```bash
yarn start:dev
```

Once you have finished, you can build and export the frontend then install the python package by running:

```bash
yarn build
yarn export
python -m pip install .
```

#### Windows Sensors

Open the .NET solution in the `windowssensors` directory, make your changes and build the solution.

Then install the package by running:

```bash
python -m pip install .
```

## Support my work

If you like my work, and would like to send me a tip/donation, please use the
links below:

[![Sponsor Timmo][sponsor-badge]][sponsor]

[![Buy me a coffee][buymeacoffee-shield]][buymeacoffee]

[buymeacoffee-shield]: https://www.buymeacoffee.com/assets/img/guidelines/download-assets-sm-2.svg
[buymeacoffee]: https://www.buymeacoffee.com/timmo
[sponsor-badge]: https://raw.githubusercontent.com/timmo001/home-panel/master/documentation/resources/sponsor.png
[sponsor]: https://github.com/sponsors/timmo001?o=esc
