#!/bin/bash

# Test Workflow for PerformiaKnob
echo "🧪 Testing PerformiaKnob Component"
echo "==================================="

# Phase 1: Visual validation
echo ""
echo "👁️ PHASE 1: Visual Validation"
echo "-----------------------------"
echo "Ask Gemini to validate the implementation:"
echo 'gemini:ask-gemini "Review this JUCE knob implementation and verify it matches the design spec" @src/components/basic/PerformiaKnob.cpp'

# Phase 2: Code review
echo ""
echo "📝 PHASE 2: Code Review"
echo "----------------------"
npx claude-flow@alpha swarm "Review PerformiaKnob for JUCE best practices and performance" \
  --agents reviewer,tester \
  --namespace performia-components

# Phase 3: Integration test
echo ""
echo "🔌 PHASE 3: Integration Test"
echo "----------------------------"
echo "Create test harness..."

cat > tests/components/TestPerformiaKnob.cpp << 'TEST'
#include "../../src/components/basic/PerformiaKnob.h"
#include <juce_core/juce_core.h>

class PerformiaKnobTest : public juce::UnitTest
{
public:
    PerformiaKnobTest() : UnitTest("PerformiaKnob") {}
    
    void runTest() override
    {
        beginTest("Creation");
        PerformiaKnob knob;
        expect(knob.getWidth() == 64);
        expect(knob.getHeight() == 64);
        
        beginTest("Value Range");
        knob.setRange(0.0, 100.0);
        knob.setValue(50.0);
        expectEquals(knob.getValue(), 50.0);
        
        beginTest("Visual Properties");
        expect(knob.getLookAndFeel() != nullptr);
    }
};

static PerformiaKnobTest performiaKnobTest;
TEST

echo "✅ Test harness created"
