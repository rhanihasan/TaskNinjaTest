import subprocess
import argparse
import os

def run_nuclei_scan(input_file, output_file):
    output_data = ""

    # Ensure the input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file {input_file} not found!")
        return
    
    with open(input_file, "r") as nuclei_input, open(output_file, "w") as nuclei_output:
        for line in nuclei_input:
            try:
                target = line.strip()
                print(f"🚀 Running Nuclei scan on {target}...")

                # Run Nuclei scan
                result = subprocess.run(
                    ["nuclei", "-u", target, "-o", output_file],
                    capture_output=True,
                    text=True
                )

                if result.returncode == 0:
                    print(f"✅ Nuclei scan completed for {target}")
                else:
                    print(f"⚠️ Nuclei scan failed for {target}. Error: {result.stderr}")

                nuclei_output.write(result.stdout)
                output_data += result.stdout + "\n"

            except Exception as e:
                error_msg = f"❌ Failed to scan {target} - {e}\n"
                print(error_msg.strip())
                nuclei_output.write(error_msg)

    print(f"✅ Nuclei scan completed. Results saved in {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nuclei Scan Script")
    parser.add_argument("input_file", help="Path to input file (e.g., /hive/out/nmap_results.txt)")
    parser.add_argument("output_file", help="Path to save Nuclei scan results")
    args = parser.parse_args()

    run_nuclei_scan(args.input_file, args.output_file)
