#!/usr/bin/env python3
"""
Integration Test - Verify GPU Knowledge Works in Orchestration Repo

Run this to verify everything is set up correctly.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_import():
    """Test that modules can be imported"""
    print("Testing imports...")
    try:
        from gpu_knowledge import AgentKnowledgeInterface, SharedGPUKnowledgeBase
        print("✅ GPU knowledge modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False


def test_knowledge_base_load():
    """Test that knowledge base loads"""
    print("\nTesting knowledge base loading...")
    try:
        from gpu_knowledge import SharedGPUKnowledgeBase

        kb = SharedGPUKnowledgeBase()
        pkl_path = Path(__file__).parent.parent / "gpu_knowledge" / "gpu_knowledge_from_pdf.pkl"

        if not pkl_path.exists():
            print(f"❌ Knowledge base file not found: {pkl_path}")
            return False

        kb.load_knowledge_base(str(pkl_path))
        print("✅ Knowledge base loaded successfully")
        return True
    except Exception as e:
        print(f"❌ Knowledge base loading failed: {e}")
        return False


def test_agent_query():
    """Test that agent can query knowledge"""
    print("\nTesting agent knowledge queries...")
    try:
        from gpu_knowledge import AgentKnowledgeInterface

        agent = AgentKnowledgeInterface(agent_id=1)

        # Test query 1: Architecture (returns list from PDF knowledge)
        arch = agent.ask("gpu_architecture_fundamentals")
        if arch is None:
            print("❌ Architecture query returned None")
            return False
        # PDF knowledge returns list, extract first element
        if isinstance(arch, list) and len(arch) > 0:
            arch = arch[0]
        if not isinstance(arch, dict):
            print(f"❌ Architecture query returned unexpected type: {type(arch)}")
            return False
        print("✅ Architecture knowledge query successful")

        # Test query 2: Performance
        perf = agent.ask("hopper_sota_matmul")
        if perf is None:
            print("❌ Performance query returned None")
            return False
        if isinstance(perf, list) and len(perf) > 0:
            perf = perf[0]
        if not isinstance(perf, dict):
            print(f"❌ Performance query returned unexpected type: {type(perf)}")
            return False
        print("✅ Performance knowledge query successful")

        # Test query 3: Memory
        memory = agent.ask("memory_subsystem_deep_dive")
        if memory is None:
            print("❌ Memory query returned None")
            return False
        if isinstance(memory, list) and len(memory) > 0:
            memory = memory[0]
        if not isinstance(memory, dict):
            print(f"❌ Memory query returned unexpected type: {type(memory)}")
            return False
        print("✅ Memory knowledge query successful")

        return True
    except Exception as e:
        print(f"❌ Agent query failed: {e}")
        return False


def test_statistics():
    """Test knowledge usage statistics"""
    print("\nTesting knowledge statistics...")
    try:
        from gpu_knowledge import SharedGPUKnowledgeBase

        kb = SharedGPUKnowledgeBase()
        stats = kb.get_agent_statistics()

        if not isinstance(stats, dict):
            print("❌ Statistics returned invalid format")
            return False

        print(f"✅ Statistics retrieved:")
        print(f"   Total queries: {stats.get('total_queries', 0)}")
        print(f"   Active agents: {stats.get('unique_agents', 0)}")
        print(f"   Knowledge categories: {stats.get('knowledge_categories', 0)}")

        return True
    except Exception as e:
        print(f"❌ Statistics test failed: {e}")
        return False


def test_example_use_case():
    """Test a realistic use case"""
    print("\nTesting realistic use case...")
    try:
        from gpu_knowledge import AgentKnowledgeInterface

        # Create agent
        agent = AgentKnowledgeInterface(agent_id=1)

        # Simulate optimization task
        tma = agent.ask("tma_tensor_memory_accelerator")
        if not tma:
            print("❌ TMA query failed")
            return False
        if isinstance(tma, list) and len(tma) > 0:
            tma = tma[0]

        swizzle = agent.ask("swizzling_deep_dive")
        if not swizzle:
            print("❌ Swizzle query failed")
            return False
        if isinstance(swizzle, list) and len(swizzle) > 0:
            swizzle = swizzle[0]

        hopper = agent.ask("hopper_sota_matmul")
        if not hopper:
            print("❌ Hopper query failed")
            return False
        if isinstance(hopper, list) and len(hopper) > 0:
            hopper = hopper[0]

        print("✅ Realistic optimization workflow successful")
        print("   Agent queried TMA, swizzling, and Hopper SOTA knowledge")

        return True
    except Exception as e:
        print(f"❌ Use case test failed: {e}")
        return False


def run_all_tests():
    """Run all integration tests"""
    print("="*70)
    print("GPU KNOWLEDGE INTEGRATION TESTS")
    print("="*70)
    print()

    tests = [
        ("Import Test", test_import),
        ("Knowledge Base Load", test_knowledge_base_load),
        ("Agent Query", test_agent_query),
        ("Statistics", test_statistics),
        ("Use Case", test_example_use_case),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"❌ {name} crashed: {e}")
            results.append((name, False))

    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {name}")

    print()
    print(f"Results: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n🎉 ALL TESTS PASSED! GPU knowledge is ready to use!")
        print("="*70)
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED. Please check the errors above.")
        print("="*70)
        return 1


if __name__ == "__main__":
    sys.exit(run_all_tests())
