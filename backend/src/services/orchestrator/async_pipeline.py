"""Async orchestrator for parallel audio analysis pipeline."""
import asyncio
import logging
import time
from pathlib import Path
from typing import Dict, List, Optional
import json

logging.basicConfig(level=logging.INFO)


class AsyncPipeline:
    """Orchestrates audio analysis services in parallel where possible."""

    def __init__(self, output_dir: str):
        """
        Initialize pipeline.

        Args:
            output_dir: Directory for intermediate outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger(__name__)

    async def run_service(
        self,
        service_name: str,
        script_path: str,
        job_id: str,
        input_file: str,
        dependencies: Optional[List[str]] = None
    ) -> Dict:
        """
        Run a single service asynchronously.

        Args:
            service_name: Name of service
            script_path: Path to service main.py
            job_id: Job identifier
            input_file: Input audio file path
            dependencies: List of service names this depends on

        Returns:
            Service output dict
        """
        start_time = time.time()
        self.logger.info(f"Starting {service_name}...")

        # Build command
        cmd = [
            "python3",
            script_path,
            "--id", job_id,
            "--infile", input_file,
            "--out", str(self.output_dir)
        ]

        # Set PYTHONPATH to include src directory
        import os
        env = os.environ.copy()
        backend_root = Path(__file__).parent.parent.parent.parent
        env['PYTHONPATH'] = str(backend_root / 'src')

        # Run subprocess
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env=env
        )

        stdout, stderr = await process.communicate()

        elapsed = time.time() - start_time

        if process.returncode != 0:
            error_msg = stderr.decode() if stderr else "Unknown error"
            self.logger.error(f"{service_name} failed: {error_msg}")
            raise RuntimeError(f"{service_name} failed: {error_msg}")

        # Parse output
        output = json.loads(stdout.decode())
        self.logger.info(f"{service_name} completed in {elapsed:.1f}s")

        return {
            "service": service_name,
            "elapsed": elapsed,
            "output": output
        }

    async def run_parallel_services(
        self,
        services: List[Dict],
        job_id: str,
        input_file: str
    ) -> Dict[str, Dict]:
        """
        Run multiple services in parallel.

        Args:
            services: List of service configs with name, script_path, dependencies
            job_id: Job identifier
            input_file: Input audio file

        Returns:
            Dict mapping service name to results
        """
        results = {}
        completed = set()

        # Build dependency graph
        dependency_map = {s["name"]: s.get("dependencies", []) for s in services}

        while len(completed) < len(services):
            # Find services ready to run
            ready = []
            for service in services:
                name = service["name"]
                if name not in completed:
                    deps = dependency_map.get(name, [])
                    if all(d in completed for d in deps):
                        ready.append(service)

            if not ready:
                pending = [s["name"] for s in services if s["name"] not in completed]
                raise RuntimeError(f"Circular dependency detected. Pending: {pending}")

            # Run ready services in parallel
            self.logger.info(f"Running {len(ready)} services in parallel: {[s['name'] for s in ready]}")

            tasks = [
                self.run_service(
                    service["name"],
                    service["script_path"],
                    job_id,
                    input_file,
                    service.get("dependencies")
                )
                for service in ready
            ]

            batch_results = await asyncio.gather(*tasks, return_exceptions=True)

            # Process results
            for i, result in enumerate(batch_results):
                service_name = ready[i]["name"]

                if isinstance(result, Exception):
                    self.logger.error(f"{service_name} failed: {result}")
                    raise result

                results[service_name] = result
                completed.add(service_name)

        return results

    async def run_full_pipeline(
        self,
        job_id: str,
        input_file: str,
        services_config: Optional[List[Dict]] = None
    ) -> Dict:
        """
        Run complete analysis pipeline.

        Args:
            job_id: Job identifier
            input_file: Input audio file path
            services_config: Optional custom service configuration

        Returns:
            Complete pipeline results
        """
        if services_config is None:
            # Default pipeline configuration
            services_config = [
                {
                    "name": "separation",
                    "script_path": "backend/src/services/separation/main.py",
                    "dependencies": []
                },
                {
                    "name": "asr",
                    "script_path": "backend/src/services/asr/main.py",
                    "dependencies": ["separation"]
                },
                {
                    "name": "beats_key",
                    "script_path": "backend/src/services/beats_key/main.py",
                    "dependencies": []
                },
                {
                    "name": "chords",
                    "script_path": "backend/src/services/chords/main.py",
                    "dependencies": ["separation"]
                },
                {
                    "name": "melody_bass",
                    "script_path": "backend/src/services/melody_bass/main.py",
                    "dependencies": ["separation"]
                },
                {
                    "name": "structure",
                    "script_path": "backend/src/services/structure/main.py",
                    "dependencies": ["beats_key", "chords"]
                },
                {
                    "name": "packager",
                    "script_path": "backend/src/services/packager/main.py",
                    "dependencies": ["asr", "beats_key", "chords", "melody_bass", "structure"]
                }
            ]

        pipeline_start = time.time()
        self.logger.info(f"Starting pipeline for job {job_id}")

        results = await self.run_parallel_services(services_config, job_id, input_file)

        total_elapsed = time.time() - pipeline_start
        service_times = {name: res["elapsed"] for name, res in results.items()}

        self.logger.info(f"Pipeline completed in {total_elapsed:.1f}s")
        self.logger.info(f"Service times: {service_times}")

        return {
            "job_id": job_id,
            "total_elapsed": total_elapsed,
            "service_times": service_times,
            "results": {name: res["output"] for name, res in results.items()}
        }


async def main():
    """CLI entry point for async pipeline."""
    import argparse

    parser = argparse.ArgumentParser(description="Async Audio Analysis Pipeline")
    parser.add_argument("--id", required=True, help="Job ID")
    parser.add_argument("--infile", required=True, help="Input audio file")
    parser.add_argument("--out", required=True, help="Output directory")
    args = parser.parse_args()

    pipeline = AsyncPipeline(args.out)
    results = await pipeline.run_full_pipeline(args.id, args.infile)

    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    asyncio.run(main())