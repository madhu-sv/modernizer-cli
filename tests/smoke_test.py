import os
import shutil
from pathlib import Path
from typer.testing import CliRunner
from modernizer.main import app

runner = CliRunner()
TEST_DIR = Path("smoke_test_env")

def setup_test_env():
    if TEST_DIR.exists(): shutil.rmtree(TEST_DIR)
    TEST_DIR.mkdir()
    
    # 1. Create Dummy POM
    (TEST_DIR / "pom.xml").write_text("<project></project>")
    
    # 2. Create Legacy File
    java_file = TEST_DIR / "LegacyService.java"
    java_file.write_text("""
package com.example;
import io.vertx.core.AbstractVerticle;
import io.vertx.core.Promise;

public class LegacyService extends AbstractVerticle {
    public void start(Promise<Void> startFuture) {
        System.out.println("Start");
        startFuture.complete();
    }
}
    """)
    return java_file

def test_full_migration():
    print("🔥 Starting Smoke Test...")
    java_file = setup_test_env()
    
    # Run the CLI against the test file
    result = runner.invoke(app, ["migrate", str(java_file), "--auto-approve"])
    
    # Verify CLI Output
    if result.exit_code != 0:
        print(f"❌ CLI Failed:\n{result.stdout}")
        return

    # Verify File Content
    content = java_file.read_text()
    
    print("\n--- Migrated Code ---")
    print(content)
    print("---------------------")

    # Assertions
    if "@Service" in content and "Mono" in content:
        print("✅ SUCCESS: Code contains Spring Boot & Reactor patterns.")
    else:
        print("❌ FAILURE: Code was not correctly refactored.")

if __name__ == "__main__":
    test_full_migration()