import shodan
import argparse
import os

def request_search_from_shodan(api_key, search, output_file=None):
    api = shodan.Shodan(api_key)

    page = 1
    output_data = ""

    with open("shodan_results.txt", "w") as shodan_results, \
         open("nmap_input.txt", "w") as nmap_file, \
         open("nuclei_input.txt", "w") as nuclei_file:

        while True:
            try:
                print(f"Searching for '{search}' on page {page}...")
                shodan_search_results = api.search(search, page=page)

                if page == 1:
                    print(f"Total Search results: {shodan_search_results['total']}")

                for match in shodan_search_results["matches"]:
                    ip = match.get('ip_str', 'N/A')
                    port = match.get('port', 'N/A')
                    vulns = match.get('vulns', [])

                    result_entry = f"IP: {ip}, Port: {port}\n"

                    print(f"IP Address: {ip}")
                    print(f"Open Ports: {port}")
                    shodan_results.write(result_entry)
                    nmap_file.write(f"{ip}:{port}\n")

                    if vulns:
                        print("Vulnerabilities:")
                        for vuln in vulns:
                            print(f" -- {vuln}")
                            result_entry += f" -- CVE {vuln}\n"
                    else:
                        print("No Vulnerabilities Found.")

                    print("-" * 30 + '\n')
                    shodan_results.write('-' * 30 + '\n')

                    output_data += result_entry  # Corrected

                if len(shodan_search_results["matches"]) < 100:
                    print("The results are under 100; stopping.")
                    break

                page += 1

            except shodan.APIError as apierror:
                print(f"Error: {apierror}")
                break
            except Exception as exceptions:
                print(f"Unexpected error occurred: {exceptions}")
                break

    # ✅ Ensure the output directory exists before writing the file
    if output_file:
        output_dir = os.path.dirname(output_file)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(output_file, "w") as f:
            f.write(output_data)
        print(f"Saved results to {output_file}")
    else:
        print(output_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Shodan Query Script")
    parser.add_argument("-a", "--api_key", required=True, help="Your Shodan API key")
    parser.add_argument("-d", "--domain", required=True, help="The target domain or IP to search")
    parser.add_argument("output_file", nargs="?", help="Optional output file to store results")
    args = parser.parse_args()

    request_search_from_shodan(args.api_key, args.domain, args.output_file)
