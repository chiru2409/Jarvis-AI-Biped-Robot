# System Architecture

## Overview

Jarvis is an ESP32-S3 powered AI biped robot that combines:

- Voice Interaction
- Memory
- Web Search
- MCP Tools
- Real-Time Information Retrieval

## Architecture

User
↓
Microphone
↓
ESP32-S3
↓
Xiaozhi / Tenclass
↓
Language Model
↓
MCP Server
├── Web Search
├── AI News
├── Robotics News
├── Weather
├── Memory
└── Project Assistant
↓
Speaker
