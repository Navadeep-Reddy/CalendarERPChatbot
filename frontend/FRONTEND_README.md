# 🎨 ERP Calendar Chatbot - Frontend

A modern, professional React frontend for the ERP Calendar Chatbot, built with Vite, React 19, Shadcn/UI, and Tailwind CSS v4.

## ✨ Features

-   🤖 **Real-time Chat Interface** - Smooth, responsive chat experience
-   🎯 **RAG-powered Responses** - Shows source documents from retrieval
-   🎨 **Beautiful UI** - Professional design with Shadcn/UI components
-   🌙 **Dark Mode Ready** - Supports light and dark themes
-   📱 **Responsive Design** - Works on all screen sizes
-   ⚡ **Fast Performance** - Built with Vite for lightning-fast development
-   🔄 **Auto-scroll** - Messages automatically scroll into view
-   💬 **Message Types** - User, bot, and error messages with distinct styling
-   🔌 **Connection Status** - Real-time backend connection indicator
-   📄 **Source Documents** - View RAG retrieval sources for each response

## 🏗️ Architecture

### Component Structure

```
src/
├── components/
│   ├── ChatMessage.jsx       # Individual message component
│   ├── ChatInput.jsx          # Message input with send button
│   ├── ChatContainer.jsx      # Messages list with scroll
│   ├── Header.jsx             # App header with status
│   ├── SourceDocument.jsx     # Source document display
│   └── ui/                    # Shadcn UI components
│       ├── avatar.jsx
│       ├── badge.jsx
│       ├── button.jsx
│       ├── card.jsx
│       ├── input.jsx
│       └── scroll-area.jsx
├── hooks/
│   └── useChat.js             # Chat state management hook
├── services/
│   └── api.js                 # Backend API integration
├── lib/
│   └── utils.js               # Utility functions
├── App.jsx                    # Main application
└── main.jsx                   # Entry point
```

### State Management

The application uses a custom `useChat` hook that handles:

-   Message history
-   Backend connection status
-   Loading states
-   Error handling
-   System information

### API Integration

The `api.js` service layer provides:

-   `checkHealth()` - Backend health check
-   `getSystemInfo()` - System configuration
-   `sendMessage(message)` - Send chat messages
-   `initializeDatabase()` - Admin function

## 🚀 Getting Started

### Prerequisites

-   Node.js 18+
-   pnpm (or npm/yarn)
-   Backend server running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
pnpm install

# Copy environment file
cp .env.example .env

# Start development server
pnpm dev
```

The application will be available at `http://localhost:5173`

### Environment Variables

Create a `.env` file:

```env
VITE_API_URL=http://localhost:8000
```

## 📦 Technology Stack

| Technology   | Version | Purpose             |
| ------------ | ------- | ------------------- |
| React        | 19.0.0  | UI framework        |
| Vite         | 6.1.0   | Build tool          |
| Tailwind CSS | 4.0.6   | Styling             |
| Shadcn/UI    | Latest  | Component library   |
| Lucide React | 0.475.0 | Icons               |
| Radix UI     | Latest  | Headless components |

## 🎨 UI Components

### ChatMessage

Displays individual messages with:

-   User/bot/error avatars
-   Message bubbles with appropriate styling
-   Timestamps
-   Source document references (for bot messages)

### ChatInput

Input field with:

-   Send button
-   Loading states
-   Keyboard shortcuts (Enter to send)
-   Disabled state when disconnected

### ChatContainer

Message list with:

-   Auto-scroll to latest message
-   Empty state with example queries
-   Loading animation
-   Smooth message transitions

### Header

Top bar showing:

-   App branding
-   Connection status badge
-   System info (model, document count)
-   Clear chat button

### SourceDocument

Displays RAG sources with:

-   Document type icon
-   Page number
-   Content preview
-   Source file name

## 🔧 Development

### Available Scripts

```bash
# Start development server
pnpm dev

# Build for production
pnpm build

# Preview production build
pnpm preview

# Lint code
pnpm lint
```

### Adding Shadcn Components

```bash
# Add a new component
pnpm dlx shadcn@latest add <component-name>
```

## 🎯 Usage Examples

### Basic Chat Flow

1. User types a message
2. `ChatInput` captures input and calls `sendUserMessage()`
3. `useChat` hook adds user message to state
4. API call to backend via `sendMessage()`
5. Bot response added to state
6. `ChatMessage` renders response with sources

### Error Handling

-   Connection errors show banner at top
-   Message errors show inline with retry button
-   Loading states prevent duplicate submissions

## 🌐 API Endpoints Used

| Endpoint      | Method | Purpose                 |
| ------------- | ------ | ----------------------- |
| `/health`     | GET    | Check backend status    |
| `/info`       | GET    | Get system information  |
| `/chat`       | POST   | Send message to chatbot |
| `/initialize` | POST   | Initialize database     |

## 🎨 Styling

### Theme

The app uses Tailwind CSS v4 with Shadcn theming:

-   Custom CSS variables for colors
-   Dark mode support via `.dark` class
-   Emerald green accent color for branding
-   Professional zinc color palette

### Responsive Design

-   Mobile-first approach
-   Breakpoints: `sm`, `md`, `lg`, `xl`
-   Flexible layouts with Flexbox/Grid
-   Touch-friendly interactive elements

## 🔒 Security

-   Environment variables for API URLs
-   Input validation before sending
-   Error messages don't expose sensitive data
-   CORS handled by backend

## 📊 Performance

-   Vite HMR for instant updates
-   Lazy loading for components (optional)
-   Optimized re-renders with React 19
-   Efficient state updates
-   Auto-scroll with `useEffect` optimization

## 🐛 Troubleshooting

### Backend Connection Failed

1. Ensure backend is running: `cd backend && python -m uvicorn app.main:app --reload`
2. Check API URL in `.env`
3. Verify CORS settings in backend

### Messages Not Appearing

1. Check browser console for errors
2. Verify network tab for API responses
3. Check backend logs

### Styling Issues

1. Clear browser cache
2. Rebuild: `pnpm build`
3. Check Tailwind compilation

## 🚀 Deployment

### Build

```bash
# Create production build
pnpm build

# Output in `dist/` folder
```

### Deploy to Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

### Environment Variables in Production

Set `VITE_API_URL` to your production backend URL.

## 📝 Future Enhancements

-   [ ] Message persistence (localStorage)
-   [ ] Export chat history
-   [ ] Voice input
-   [ ] File uploads
-   [ ] Multi-language support
-   [ ] User authentication
-   [ ] Chat history sidebar
-   [ ] Markdown rendering in messages
-   [ ] Code syntax highlighting
-   [ ] Typing indicators

## 🤝 Contributing

This is part of the Calendar ERP Chatbot project. See main README for contribution guidelines.

## 📄 License

See main project LICENSE file.

---

**Built with ❤️ using React, Vite, Shadcn/UI, and Tailwind CSS**
