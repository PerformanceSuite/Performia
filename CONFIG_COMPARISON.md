# Configuration File Comparison

This document compares configuration files between the main Performia repository and the Performia-front repository.

## Python Dependencies (requirements.txt)

### Main Repository Only
```txt
fastmcp>=0.3.0
pydantic>=2.0.0
sqlite3
asyncio
anthropic>=0.25.0
openai>=1.0.0
langchain>=0.1.0
mcp>=1.0.0
uvloop>=0.19.0
numpy>=1.24.0
pandas>=2.0.0
plotly>=5.0.0
```

Key Components:
1. AI/ML Dependencies:
   - anthropic
   - openai
   - langchain

2. Data Processing:
   - numpy
   - pandas
   - plotly

3. Performance:
   - uvloop
   - fastmcp

4. Core Requirements:
   - pydantic
   - sqlite3
   - asyncio

## JavaScript/TypeScript Dependencies (package.json)

### Main Repository (performia---living-chart/package.json)
```json
{
  "name": "performia---living-chart",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^19.1.1",
    "react-dom": "^19.1.1",
    "immer": "^10.1.3"
  },
  "devDependencies": {
    "@types/node": "^22.14.0",
    "@vitejs/plugin-react": "^5.0.0",
    "typescript": "~5.8.2",
    "vite": "^6.2.0"
  }
}
```

### Frontend Repository (performia---living-chart/package.json)
```json
{
  "name": "performia---living-chart",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "immer": "^10.1.3",
    "react": "^19.1.1",
    "react-dom": "^19.1.1"
  },
  "devDependencies": {
    "@tailwindcss/postcss": "^4.1.13",
    "@types/node": "^22.14.0",
    "@vitejs/plugin-react": "^5.0.0",
    "autoprefixer": "^10.4.21",
    "postcss": "^8.5.6",
    "tailwindcss": "^4.1.13",
    "typescript": "~5.8.2",
    "vite": "^6.2.0"
  }
}
```

### Package.json Differences

#### Common Dependencies
- Core React: react, react-dom
- State Management: immer
- Build Tools: vite, typescript
- Type Definitions: @types/node

#### Frontend-only Dependencies
1. Styling:
   - tailwindcss
   - postcss
   - autoprefixer
   - @tailwindcss/postcss

#### Version Alignment
- Both use same versions for:
  - React (^19.1.1)
  - TypeScript (~5.8.2)
  - Vite (^6.2.0)
  - immer (^10.1.3)

## Build Configuration

### TypeScript (tsconfig.json)
Both repositories share similar base TypeScript configurations, with the frontend repository having additional options for stricter type checking and module resolution.

### Vite (vite.config.ts)
Frontend repository includes additional configuration for:
- PostCSS processing
- Tailwind CSS integration
- Development server customization

## Development Environment

### Main Repository
- Focused on Python development
- Includes JUCE build configuration
- Has CI/CD workflow configuration
- Kubernetes deployment configuration

### Frontend Repository
- JavaScript/TypeScript focused
- Enhanced styling pipeline
- Development tools configuration
- AI assistance configuration

## Integration Points

### Main Repository
- Voice engine configuration
- Pipeline service configuration
- API endpoint configuration
- OSC communication setup

### Frontend Repository
- UI component configuration
- Library service setup
- Development tooling
- AI assistant integration

## Recommendations for Consolidation

1. Dependencies:
   - Merge styling dependencies into main repo
   - Maintain version alignment
   - Keep development tools separated

2. Build Configuration:
   - Integrate PostCSS/Tailwind setup
   - Maintain separate build pipelines
   - Share common TypeScript config

3. Development Environment:
   - Keep language-specific tools separate
   - Share development utilities where possible
   - Maintain distinct CI/CD configurations
