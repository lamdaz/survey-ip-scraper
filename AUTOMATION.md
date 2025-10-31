# 🤖 Automated IP Scraping with GitHub Actions

This repository is configured to automatically scrape IP addresses every 5 minutes using GitHub Actions and update the results in the repository.

## ⚡ How It Works

The automation workflow:
1. **Runs every 5 minutes** (via GitHub Actions cron schedule)
2. **Reads IPs** from `data/ips_to_scrape.txt`
3. **Scrapes data** for each IP (geolocation, ISP, ASN, etc.)
4. **Generates results** and saves to `data/latest_results.csv`
5. **Creates backups** with timestamps (`data/results_YYYYMMDD_HHMMSS.csv`)
6. **Updates statistics** in README.md
7. **Commits changes** back to the repository automatically

## 📝 Configuration

### Adding IPs to Scrape

Edit the file `data/ips_to_scrape.txt`:

```bash
# Add your IPs here, one per line
8.8.8.8
1.1.1.1
208.67.222.222
# Add more IPs...
```

### Changing the Schedule

Edit `.github/workflows/auto-scrape.yml` to change the cron schedule:

```yaml
on:
  schedule:
    # Current: Every 5 minutes
    - cron: '*/5 * * * *'
    
    # Examples:
    # Every 10 minutes: '*/10 * * * *'
    # Every hour: '0 * * * *'
    # Every 6 hours: '0 */6 * * *'
    # Daily at midnight: '0 0 * * *'
```

## 🎯 Workflow Triggers

The automation runs on:

1. **Schedule**: Every 5 minutes automatically
2. **Manual Trigger**: Via GitHub Actions UI
3. **File Change**: When `data/ips_to_scrape.txt` is updated

### Manual Trigger

To trigger manually:
1. Go to: https://github.com/lamdaz/survey-ip-scraper/actions
2. Click "Auto IP Scraper"
3. Click "Run workflow"
4. Select branch (main)
5. Click "Run workflow"

## 📊 Output Files

The workflow generates several files:

### Main Results
- **`data/latest_results.csv`** - Most recent scan results
- **`data/summary.json`** - Statistical summary

### Backups
- **`data/results_YYYYMMDD_HHMMSS.csv`** - Timestamped backups
- Kept in repository for historical tracking

### Updated Files
- **`README.md`** - Automatically updated with latest statistics

## 📈 Viewing Results

### In Repository
Browse to the `data/` folder to see all results:
- https://github.com/lamdaz/survey-ip-scraper/tree/main/data

### Latest Results
View the most recent scan:
- https://github.com/lamdaz/survey-ip-scraper/blob/main/data/latest_results.csv

### Statistics
Check the README for auto-updated stats:
- https://github.com/lamdaz/survey-ip-scraper#-latest-scan-results

### Action Logs
View execution logs:
- https://github.com/lamdaz/survey-ip-scraper/actions

## 🔧 Advanced Configuration

### Rate Limiting

Adjust the API request rate in `.github/workflows/auto-scrape.yml`:

```yaml
- name: Run IP scraper
  run: |
    python -m survey_ip.cli \
      --input data/ips_to_scrape.txt \
      --output data/latest_results.csv \
      --rate 0.5  # Change this (requests per second)
```

### Disable RDAP Lookups (Faster)

Add `--no-rdap` flag for faster execution:

```yaml
python -m survey_ip.cli \
  --input data/ips_to_scrape.txt \
  --output data/latest_results.csv \
  --no-rdap
```

### Retention of Artifacts

Change how long scan artifacts are kept:

```yaml
- name: Create artifact
  uses: actions/upload-artifact@v3
  with:
    name: ip-scan-results
    retention-days: 30  # Change this (1-90 days)
```

## 🚨 Important Notes

### GitHub Actions Minutes

- Free tier: 2,000 minutes/month for public repos
- Running every 5 minutes: ~10 seconds per run = ~8 hours/month
- **Well within free limits!**

### API Rate Limits

- **ip-api.com**: 45 requests/minute (free tier)
- Workflow uses 0.5 req/sec = 30 req/min (safe)
- For more IPs, consider upgrading or reducing frequency

### Repository Size

- Backup files accumulate over time
- Consider periodic cleanup:
  ```bash
  # Keep only last 100 backups
  cd data
  ls -t results_*.csv | tail -n +101 | xargs rm -f
  ```

## 🛠️ Troubleshooting

### Workflow Not Running

Check:
1. Actions are enabled: Settings → Actions → Allow all actions
2. Workflow file is in correct location: `.github/workflows/auto-scrape.yml`
3. Cron syntax is valid: Use https://crontab.guru

### Permission Errors

Ensure workflow has write permissions:
- Settings → Actions → General → Workflow permissions
- Select "Read and write permissions"

### Rate Limit Errors

If you see rate limit errors:
1. Reduce the scraping frequency
2. Reduce the `--rate` parameter
3. Decrease number of IPs in `data/ips_to_scrape.txt`

### No Changes Committed

This is normal if:
- IPs haven't changed location/ISP
- Data is identical to previous scan
- Workflow skips commit when no changes detected

## 📋 Example Workflow Run

Typical execution:
```
🚀 Starting IP scraping process...
Processing IPs: 100%|████████████| 6/6 [00:12<00:00,  2.00s/it]
✓ Scraping completed
✓ Created backup: results_20250131_123456.csv
📊 Generating summary report...
✓ Processed 6 IP addresses
✓ Found 3 unique countries
✓ Found 4 unique ISPs
✓ Summary generated
✓ README updated with latest stats
✓ Changes pushed to repository
```

## 🎨 Customization Ideas

### Add Email Notifications

Add notification step in workflow:
```yaml
- name: Send notification
  if: failure()
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: IP Scraper Failed
    body: Workflow failed. Check logs.
```

### Create Charts

Generate visual charts from data:
```yaml
- name: Generate charts
  run: |
    pip install matplotlib pandas
    python scripts/create_charts.py
```

### Webhook Notifications

Send results to external service:
```yaml
- name: Send webhook
  run: |
    curl -X POST https://your-webhook.com/endpoint \
      -H "Content-Type: application/json" \
      -d @data/summary.json
```

## 📚 Resources

- [GitHub Actions Docs](https://docs.github.com/en/actions)
- [Cron Schedule Expression](https://crontab.guru)
- [IP-API Documentation](https://ip-api.com/docs)

## 🤝 Contributing

To improve the automation:
1. Fork the repository
2. Make your changes
3. Test with manual workflow trigger
4. Submit pull request

---

**Automated scanning is now active! 🎉**

Check the Actions tab to see it in action:
https://github.com/lamdaz/survey-ip-scraper/actions
