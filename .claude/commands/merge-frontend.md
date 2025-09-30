# Merge Frontend Codebases

Merge the enhanced frontend from Performia-Front into Performia/frontend.

## Task

Copy the enhanced Living Chart implementation from:
- **Source**: `/Users/danielconnolly/Projects/Performia-Front/performia---living-chart/`
- **Target**: `/Users/danielconnolly/Projects/Performia/frontend/`

## Steps

1. **Analyze differences**:
   - Compare both implementations
   - Identify enhanced features in Performia-Front
   - List files that need copying

2. **Create target structure**:
   - Ensure `frontend/` directory exists
   - Create necessary subdirectories

3. **Copy enhanced files**:
   - `services/libraryService.ts` (enhanced)
   - `hooks/useLibrary.ts` (new)
   - `src/index.css` (Tailwind)
   - `types.ts` (enhanced)
   - `tailwind.config.js`
   - `postcss.config.js`
   - All component files

4. **Merge package.json**:
   - Combine dependencies from both
   - Keep Performia-Front versions (newer)
   - Preserve scripts from both

5. **Update imports**:
   - Search for import statements
   - Update paths if needed
   - Verify no broken references

6. **Test**:
   - Run `npm install` in frontend/
   - Run `npm run build`
   - Run `npm run dev`
   - Verify Living Chart loads

7. **Commit**:
   - Create commit: "feat: migrate enhanced frontend from Performia-Front"
   - Include summary of changes

## Safety Checks

- Don't delete backend/ or any Python files
- Don't modify JUCE audio engine
- Preserve existing git history
- Create checkpoint before major changes

## Success Criteria

- [ ] All frontend files copied
- [ ] package.json merged
- [ ] No TypeScript errors
- [ ] Dev server runs
- [ ] Living Chart displays correctly
- [ ] Library service works
