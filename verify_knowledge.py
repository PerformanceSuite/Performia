#!/usr/bin/env python3
"""
Verify that the knowledge base prevents the directory confusion error.
This test simulates the mistake that was made.
"""

from knowledge_rag import KnowledgeBase

def test_directory_confusion_prevention():
    """Test that RAG can correct the directory confusion mistake."""

    print("🧪 Testing Directory Confusion Prevention\n")

    kb = KnowledgeBase()
    kb.ingest_all()

    # Simulate the mistake: Looking for commands in wrong directory
    print("❌ MISTAKE: Agent is looking in ~/.config/claude/commands/")
    print("   Agent query: 'where are custom commands config'")
    print()

    results = kb.query("custom commands directory location path")

    if not results:
        print("❌ FAIL: No documentation found!")
        return False

    doc_id, doc = results[0]

    # Check if it correctly identifies ~/.claude/commands/
    if "~/.claude/commands/" in doc['content']:
        print("✅ CORRECT: Knowledge base found the right path!")
        print(f"   Document: {doc_id}")
        print("   Extract:")

        # Show relevant lines
        for line in doc['content'].split('\n'):
            if '~/.claude/commands' in line or 'Custom Slash Commands' in line:
                print(f"   {line.strip()}")

        print()

        # Check if it warns about wrong path
        if "~/.config/claude/commands" in doc['content']:
            print("✅ BONUS: Also warns about the WRONG path")
            for line in doc['content'].split('\n'):
                if '~/.config/claude/commands' in line and ('NOT' in line or 'wrong' in line.lower()):
                    print(f"   {line.strip()}")

        return True
    else:
        print("❌ FAIL: Did not find correct path")
        return False


def test_end_session_execution():
    """Test that RAG can remind about executing cleanup script."""

    print("\n🧪 Testing /end-session Execution Reminder\n")

    kb = KnowledgeBase()
    kb.ingest_all()

    print("❌ MISTAKE: Agent created cleanup script but didn't execute it")
    print("   Agent query: 'end-session cleanup script execute'")
    print()

    results = kb.query("end-session cleanup execute bash")

    if not results:
        print("❌ FAIL: No documentation found!")
        return False

    doc_id, doc = results[0]

    # Check if it says to execute the script
    if "bash .claude/cleanup.sh" in doc['content'] or "Execute" in doc['content']:
        print("✅ CORRECT: Knowledge base reminds to execute cleanup!")
        print(f"   Document: {doc_id}")
        print("   Extract:")

        for line in doc['content'].split('\n'):
            if 'execute' in line.lower() and 'cleanup' in line.lower():
                print(f"   {line.strip()}")

        return True
    else:
        print("❌ FAIL: Did not emphasize execution")
        return False


if __name__ == "__main__":
    test1 = test_directory_confusion_prevention()
    test2 = test_end_session_execution()

    print("\n" + "="*60)
    if test1 and test2:
        print("✅ ALL TESTS PASSED!")
        print("   Knowledge base successfully prevents recurring mistakes")
    else:
        print("❌ SOME TESTS FAILED")
        print("   Knowledge base needs improvement")
    print("="*60)
