#!/bin/bash

echo "🔍 Goose API Key Integration Diagnostic"
echo "========================================"
echo ""

# Check if centralized API keys exist
echo "1. Checking centralized API keys file..."
if [ -f "$HOME/.config/api-keys/.env.api-keys" ]; then
    echo "   ✅ Found: ~/.config/api-keys/.env.api-keys"
    
    # Source the file and check keys
    source "$HOME/.config/api-keys/.env.api-keys"
    
    echo ""
    echo "2. Verifying API keys are loaded:"
    
    # Check each key
    for key in ANTHROPIC_API_KEY OPENAI_API_KEY OPENROUTER_API_KEY GITHUB_TOKEN GOOGLE_API_KEY; do
        if [ -n "${!key}" ]; then
            # Show first 10 chars of key for verification (safely)
            echo "   ✅ $key: ${!key:0:10}..."
        else
            echo "   ❌ $key: NOT SET"
        fi
    done
else
    echo "   ❌ NOT FOUND: ~/.config/api-keys/.env.api-keys"
fi

echo ""
echo "3. Checking Goose configuration..."

# Check config.yaml
if [ -f "$HOME/.config/goose/config.yaml" ]; then
    echo "   ✅ config.yaml exists"
    
    # Check if load-api-keys.sh is referenced
    if grep -q "load-api-keys.sh" "$HOME/.config/goose/config.yaml"; then
        echo "   ✅ config.yaml uses API key loader wrapper"
    else
        echo "   ⚠️  config.yaml doesn't use API key loader"
    fi
else
    echo "   ❌ config.yaml not found"
fi

# Check wrapper scripts
echo ""
echo "4. Checking wrapper scripts..."

if [ -f "$HOME/.config/goose/load-api-keys.sh" ]; then
    echo "   ✅ load-api-keys.sh exists"
    if [ -x "$HOME/.config/goose/load-api-keys.sh" ]; then
        echo "   ✅ load-api-keys.sh is executable"
    else
        echo "   ❌ load-api-keys.sh is not executable"
    fi
else
    echo "   ❌ load-api-keys.sh not found"
fi

if [ -f "$HOME/bin/goose-smart" ]; then
    echo "   ✅ goose-smart launcher exists"
    if [ -x "$HOME/bin/goose-smart" ]; then
        echo "   ✅ goose-smart is executable"
    else
        echo "   ❌ goose-smart is not executable"
    fi
else
    echo "   ❌ goose-smart launcher not found"
fi

echo ""
echo "5. Testing API key loading..."

# Test the wrapper
if [ -x "$HOME/.config/goose/load-api-keys.sh" ]; then
    echo "   Testing load-api-keys.sh wrapper..."
    
    # Run a simple test command through the wrapper
    OUTPUT=$("$HOME/.config/goose/load-api-keys.sh" bash -c 'echo "ANTHROPIC_API_KEY: ${ANTHROPIC_API_KEY:0:10}..."')
    
    if echo "$OUTPUT" | grep -q "sk-ant"; then
        echo "   ✅ Wrapper successfully loads API keys"
    else
        echo "   ❌ Wrapper failed to load API keys"
        echo "   Output: $OUTPUT"
    fi
else
    echo "   ⚠️  Cannot test wrapper - not executable"
fi

echo ""
echo "6. Checking Hermit npx..."
HERMIT_NPX="/Users/danielconnolly/.config/goose/mcp-hermit/bin/npx"
if [ -f "$HERMIT_NPX" ]; then
    echo "   ✅ Hermit npx found"
    if [ -x "$HERMIT_NPX" ]; then
        echo "   ✅ Hermit npx is executable"
        VERSION=$("$HERMIT_NPX" --version 2>&1)
        echo "   ✅ Version: $VERSION"
    else
        echo "   ❌ Hermit npx is not executable"
    fi
else
    echo "   ❌ Hermit npx not found at expected location"
fi

echo ""
echo "========================================"
echo "📋 Summary & Recommendations:"
echo ""

# Source keys for final test
source "$HOME/.config/api-keys/.env.api-keys" 2>/dev/null

if [ -n "$ANTHROPIC_API_KEY" ] && [ -x "$HOME/bin/goose-smart" ] && [ -x "$HOME/.config/goose/load-api-keys.sh" ]; then
    echo "✅ Everything looks good! Your elegant solution is properly configured."
    echo ""
    echo "To use Goose with your centralized API keys:"
    echo "  1. Use the 'goose' alias (which runs goose-smart)"
    echo "  2. Or run: ~/bin/goose-smart session start"
    echo ""
    echo "The MCP servers will automatically inherit your API keys."
else
    echo "⚠️  Some components need attention:"
    
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "  - API keys not loading from centralized location"
    fi
    if [ ! -x "$HOME/bin/goose-smart" ]; then
        echo "  - goose-smart launcher needs to be executable"
    fi
    if [ ! -x "$HOME/.config/goose/load-api-keys.sh" ]; then
        echo "  - load-api-keys.sh wrapper needs to be executable"
    fi
fi

echo ""
echo "🔧 Quick fixes:"
echo "  chmod +x ~/bin/goose-smart"
echo "  chmod +x ~/.config/goose/load-api-keys.sh"
echo "  source ~/.zshrc  # Reload your shell configuration"
