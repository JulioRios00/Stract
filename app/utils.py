import services
import csv


def generate_platform_ads_csv_file(platform):
    filename = f"{platform}_ads.csv"

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
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

        accounts = services.get_accounts(platform)
        if "accounts" in accounts:
            for account in accounts["accounts"]:
                insights = services.get_insights(platform, account)
                if "insights" in insights:
                    for insight in insights["insights"]:
                        spend_field = (
                            "spend" if platform == "meta_ads" else "cost"
                        )
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
    return filename


def generate_general_csv_file():
    platforms_data = services.get_platform()
    platforms = [p["value"] for p in platforms_data["platforms"]]

    filename = "platform_summary.csv"

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
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

            if "accounts" in accounts:
                for account in accounts["accounts"]:
                    insights = services.get_insights(platform, account)
                    if "insights" in insights:
                        total_clicks = sum(
                            int(insight.get("clicks", 0))
                            for insight in insights["insights"]
                        )
                        spend_field = (
                            "spend" if platform == "meta_ads" else "cost"
                        )
                        total_spend = sum(
                            float(insight.get(spend_field, 0))
                            for insight in insights["insights"]
                        )
                        writer.writerow(
                            [
                                platform,
                                account["name"],
                                total_clicks,
                                total_spend
                            ]
                        )

    return filename
