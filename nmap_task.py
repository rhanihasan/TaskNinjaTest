import nmap
import argparse
import os

def run_nmap_scan(input_file, output_file):
    nm = nmap.PortScanner()
    output_data = ""

    # Ensure the input file exists
    if not os.path.exists(input_file):
        print(f"❌ Error: Input file {input_file} not found!")
        return

    with open(input_file, "r") as nmap_input, open(output_file, "w") as nmap_output:
        for line in nmap_input:
            try:
                # Ignore empty lines and lines that do not contain "IP:"
                if not line.strip() or "CVE" in line or "IP:" not in line:
                    print(f"❌ Skipping invalid line: {line.strip()}")
                    continue

                # Extract IP and Port correctly
                parts = line.split(",")
                ip = parts[0].split(":")[1].strip()  # Extract IP
                port = parts[1].split(":")[1].strip()  # Extract Port
                
                print(f"🔎 Scanning {ip} on port {port}...")

                # Run Nmap scan
                scan_results = nm.scan(ip, arguments=f"-p{port} -sV -T4 --open -Pn -sC --script vulners")
                nmap_output.write(f"Results for {ip}:{port}\n")
                output_data += f"Results for {ip}:{port}\n"

                for protocol in nm[ip].all_protocols():
                    for p in nm[ip][protocol].keys():
                        state = nm[ip][protocol][p]["state"]
                        service = nm[ip][protocol][p]['name']
                        product = nm[ip][protocol][p].get('product', 'Unknown')

                        result_entry = f"  Port: {p}/{protocol}, State: {state}, Service: {service}, Product: {product}\n"
                        print(result_entry.strip())
                        nmap_output.write(result_entry)
                        output_data += result_entry

                        # Include CVE results from Vulners script
                        script_results = nm[ip][protocol][p].get('script', {})
                        if script_results:
                            for script_name, output in script_results.items():
                                if script_name == "vulners":
                                    print(f"  [CVE Detected] {output}")
                                    nmap_output.write(f"  [CVE Detected] {output}\n")
                                    output_data += f"  [CVE Detected] {output}\n"

                nmap_output.write("-" * 30 + "\n")
                output_data += "-" * 30 + "\n"

            except ValueError:
                print(f"❌ Skipping invalid line: {line.strip()}")
            except Exception as e:
                error_msg = f"❌ Failed to scan {line.strip()} - {e}\n"
                print(error_msg.strip())
                nmap_output.write(error_msg)

    print(f"✅ Nmap scan completed. Results saved in {output_file}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nmap Scan Script with CVE Detection")
    parser.add_argument("input_file", help="Path to input file (e.g., /hive/out/shodan_results.txt)")
    parser.add_argument("output_file", help="Path to save Nmap scan results")
    args = parser.parse_args()

    run_nmap_scan(args.input_file, args.output_file)
