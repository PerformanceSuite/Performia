#!/bin/bash

# Performia UI Clean - Quick Start for Claude Code
echo "🎨 Performia UI Clean - Quick Start"
echo "==================================="
echo ""

# Check session status
echo "📊 Session Status:"
python3 session.py status
echo ""

# Check Claude Flow status
echo "🐝 Claude Flow Status:"
npx claude-flow@alpha hive-mind status 2>/dev/null || echo "   Hive-mind not initialized yet"
echo ""

# Show current phase progress
echo "📈 Progress:"
echo "   Phase 1: Foundation       [ ] 0%"
echo "   Phase 2: Components       [ ] 0%"
echo "   Phase 3: Studio Mode      [ ] 0%"
echo "   Phase 4: Live Mode        [ ] 0%"
echo "   Phase 5: Backend          [ ] 0%"
echo "   Phase 6: Extended Modes   [ ] 0%"
echo "   Phase 7: Polish           [ ] 0%"
echo ""

echo "📚 Key Documents:"
echo "   • CLAUDE.md - Your guide for Claude Code"
echo "   • docs/requirements/PERFORMIA_COMPLETE_PRD.md - Complete requirements"
echo "   • docs/PERFORMIA_IMPLEMENTATION_STRATEGY.md - Development plan"
echo ""

echo "🚀 Quick Commands:"
echo "   Continue session:  python3 session.py continue"
echo "   Create checkpoint: python3 session.py checkpoint 'message'"
echo "   Start hive-mind:   npx claude-flow@alpha hive-mind wizard"
echo ""

echo "💡 Next Step:"
echo "   1. Open CLAUDE.md and review the slash commands"
echo "   2. Start with Phase 1: Create main window with navigation"
echo "   3. Use: npx claude-flow@alpha swarm 'Create JUCE main window' --claude"
echo ""
echo "Ready to begin development!"