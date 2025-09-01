// Gemini Integration for Claude Flow
// This allows the hive-mind to use Gemini for specific tasks

const geminiTasks = {
  uiDesign: {
    prompt: "Create beautiful UI component",
    model: "gemini-2.5-flash",
    changeMode: true
  },
  colorScheme: {
    prompt: "Generate professional color palette",
    model: "gemini-2.5-flash"
  },
  animation: {
    prompt: "Design smooth animation patterns",
    model: "gemini-2.5-flash"
  }
};

// Export for Claude Flow integration
module.exports = { geminiTasks };
