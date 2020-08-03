import argparse
import subprocess
import json
import math


def parse_args():
    description = """Run lighthouse several times"""

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        "url", metavar="URL", help="URL",
    )

    parser.add_argument(
        "-n", dest="n", default=3, help="Times to run Lighthouse",
    )

    return parser.parse_args()


def run_lighthouse(url):
    command = ["lighthouse", url, "--output=json", "--quiet"]
    output = subprocess.check_output(" ".join(command), shell=True)

    data = json.loads(output.decode("utf-8"))

    return round(float(data["categories"]["performance"]["score"]) * 100)


def compute_statistics(performance):
    sorted_performance = sorted(performance)

    return (
        sorted_performance[0],
        sorted_performance[math.floor(len(sorted_performance) / 2)],
        sorted_performance[-1],
    )


def main():
    args = parse_args()

    performance = [run_lighthouse(args.url) for i in range(0, int(args.n))]

    print(performance)

    min_performance, median_performance, max_performance = compute_statistics(
        performance
    )

    print(f"Min:    {min_performance}")
    print(f"Max:    {max_performance}")
    print(f"Median: {median_performance}")


if __name__ == "__main__":
    main()
