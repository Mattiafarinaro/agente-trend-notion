import argparse
import time

from tasks.scheduled_tasks import WeeklyReportWorkflow


def main():
    parser = argparse.ArgumentParser(description="Run the weekly AI trend report workflow.")
    parser.add_argument("--topic", default="AI trends 2024", help="Topic to monitor")
    parser.add_argument("--schedule", action="store_true", help="Schedule the workflow weekly")
    parser.add_argument("--run-once", action="store_true", help="Run the workflow once immediately")
    args = parser.parse_args()

    workflow = WeeklyReportWorkflow()

    if args.run_once or not args.schedule:
        result = workflow.execute(args.topic)
        print("Weekly report result:")
        print(result)

    if args.schedule:
        scheduler = workflow.schedule_weekly(args.topic)
        print(f"Scheduled weekly report for topic: {args.topic}")
        try:
            while True:
                time.sleep(60)
        except KeyboardInterrupt:
            scheduler.shutdown()
            print("Scheduler stopped.")


if __name__ == "__main__":
    main()
