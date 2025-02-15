import csv
from io import StringIO
import services
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def get_platforms_data(platform):
    accounts = services.get_accounts(platform)

    csv_output = StringIO()
    writer = csv.writer(csv_output)
    writer.writerow(
        [
            "Platform",
            "Account Name",
            "Ad Name",
            "Impressions",
            "Clicks",
            "Spend"
        ]
    )

    if "accounts" in accounts:
        for account in accounts["accounts"]:
            insights = services.get_insights(platform, account)
            if "insights" in insights:
                for insight in insights["insights"]:
                    spend_field = "spend" if platform == "meta_ads" else "cost"
                    writer.writerow(
                        [
                            platform,
                            account["name"],
                            insight.get("ad_name", ""),
                            insight.get("imporessions", 0),
                            insight.get("clicks", 0),
                            insight.get(spend_field, 0),
                        ]
                    )

    return csv_output.getvalue()


def get_platforms_data_summary(platform):
    accounts = services.get_accounts(platform)

    summary = {}
    csv_output = StringIO()
    writer = csv.writer(csv_output)
    writer.writerow(
        [
            "Platform",
            "Account Name",
            "Total Impressions",
            "Total Clicks",
            "Total Spend"
            ]
    )

    if "accounts" in accounts:
        for account in accounts["accounts"]:
            account_name = account["name"]
            if account_name not in summary:
                summary[account_name] = {
                    "Impressions": 0,
                    "Clicks": 0,
                    "Spend": 0
                    }

            insights = services.get_insights(platform, account)
            if "insights" in insights:
                for insight in insights["insights"]:
                    spend_field = "spend" if platform == "meta_ads" else "cost"
                    summary[account_name]["Impressions"] += int(
                        insight.get("impressions", 0)
                    )
                    summary[account_name]["Clicks"] += int(
                        insight.get("clicks", 0)
                    )
                    summary[account_name]["Spend"] += float(
                        insight.get(spend_field, 0)
                    )

    for account_name, metrics in summary.items():
        writer.writerow(
            [
                platform,
                account_name,
                metrics["Impressions"],
                metrics["Clicks"],
                metrics["Spend"],
            ]
        )

    return csv_output.getvalue()


def get_general_report():
    platforms = services.get_platform()

    csv_output = StringIO()
    writer = csv.writer(csv_output)
    writer.writerow(["Platform", "Ad name", "Clicks", "Spend"])

    for platform in platforms:
        accounts = services.get_accounts(platform)
        fields = services.get_fields(platform)

        if isinstance(accounts, list):
            for account in accounts:
                insights = services.get_insights(
                    platform,
                    account["name"],
                    fields
                    )
                for insight in insights:
                    writer.writerow(
                        [
                            platform,
                            insight["name"],
                            insight["clicks"],
                            insight["spend"]]
                    )

    return csv_output.getvalue()


def get_general_summary():
    platforms_data = services.get_platform()
    platforms = [p["value"] for p in platforms_data["platforms"]]

    summary = {}
    csv_output = StringIO()
    writer = csv.writer(csv_output)
    writer.writerow(
        [
            "Platform",
            "Account Name",
            "Total Clicks",
            "Total Spend"
            ]
        )

    for platform in platforms:
        accounts = services.get_accounts(platform)

        if platform not in summary:
            summary[platform] = {}

        if "accounts" in accounts:
            for account in accounts["accounts"]:
                account_name = account["name"]
                if account_name not in summary[platform]:
                    summary[platform][account_name] = {
                        "Clicks": 0,
                        "Spend": 0
                    }

                insights = services.get_insights(platform, account)
                if "insights" in insights:
                    for insight in insights["insights"]:
                        summary[platform][account_name]["Clicks"] += int(
                            insight.get("clicks", 0)
                        )
                        spend_field = (
                            "spend" if platform == "meta_ads" else "cost"
                        )
                        summary[platform][account_name]["Spend"] += float(
                            insight.get(spend_field, 0)
                        )

    for platform, accounts_data in summary.items():
        for account_name, metrics in accounts_data.items():
            writer.writerow(
                [platform, account_name, metrics["Clicks"], metrics["Spend"]]
            )

    return csv_output.getvalue()
